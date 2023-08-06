import time
import logging
import json
from subprocess import CalledProcessError
import warnings

from redis import StrictRedis
import numpy as np
import pyproj
import shapely
import sqlalchemy
from plio.io.io_gdal import GeoDataset


from autocnet.cg import cg as compgeom
from autocnet.graph.node import NetworkNode
from autocnet.io.db.model import Images, Measures, Overlay, Points, JsonEncoder
from autocnet.spatial import isis
from autocnet.matcher.cpu_extractor import extract_most_interesting
from autocnet.transformation.spatial import reproject, og2oc, oc2og
from autocnet.transformation import roi

from plurmy import Slurm

# set up the logger file
log = logging.getLogger(__name__)

def place_points_in_overlaps(size_threshold=0.0007,
                             distribute_points_kwargs={},
                             cam_type='csm',
                             point_type=2,
                             ncg=None):
    """
    Place points in all of the overlap geometries by back-projecing using
    sensor models.

    Parameters
    ----------
    nodes : dict-link
            A dict like object with a shared key with the intersection
            field of the database Overlay table and a cg node object
            as the value. This could be a NetworkCandidateGraph or some
            other dict-like object.

    Session : obj
              The session object from the NetworkCandidateGraph

    size_threshold : float
                     overlaps with area <= this threshold are ignored
    cam_type : str
               Either 'csm' (default) or 'isis'. The type of sensor model to use.

    point_type : int
                 Either 2 (free;default) or 3 (constrained). Point type 3 should be used for
                 ground.
    """
    if not ncg.Session:
        raise BrokenPipeError('This func requires a database session from a NetworkCandidateGraph.')

    for overlap in Overlay.overlapping_larger_than(size_threshold, ncg.Session):
        if overlap.intersections == None:
            continue
        place_points_in_overlap(overlap,
                                cam_type=cam_type,
                                distribute_points_kwargs=distribute_points_kwargs,
                                point_type=point_type,
                                ncg=ncg)

def place_points_in_overlap(overlap,
                            identifier="autocnet",
                            cam_type="csm",
                            size=71,
                            distribute_points_kwargs={},
                            point_type=2,
                            ncg=None,
                            use_cache=False,
                            **kwargs):
    """
    Place points into an overlap geometry by back-projecting using sensor models.
    The DEM specified in the config file will be used to calculate point elevations.

    Parameters
    ----------
    overlap : obj
              An autocnet.io.db.model Overlay model instance.

    identifier: str
                The tag used to distinguish points laid down by this function.

    cam_type : str
               options: {"csm", "isis"}
               Pick what kind of camera model implementation to use.

    size : int
           The amount of pixel around a points initial location to search for an
           interesting feature to which to shift the point.

    distribute_points_kwargs: dict
                              kwargs to pass to autocnet.cg.cg.distribute_points_in_geom

    point_type: int
                The type of point being placed. Default is pointtype=2, corresponding to
                free points.

    ncg: obj
         An autocnet.graph.network NetworkCandidateGraph instance representing the network
         to apply this function to

    use_cache : bool
                If False (default) this func opens a database session and writes points
                and measures directly to the respective tables. If True, this method writes
                messages to the point_insert (defined in ncg.config) redis queue for
                asynchronous (higher performance) inserts.

    Returns
    -------
    points : list of Points
        The list of points seeded in the overlap

    See Also
    --------
    autocnet.io.db.model.Overlay: for associated properties of the Overlay object

    autocnet.cg.cg.distribute_points_in_geom: for the possible arguments to pass through using disribute_points_kwargs.

    autocnet.model.io.db.PointType: for the point type options.

    autocnet.graph.network.NetworkCandidateGraph: for associated properties and functionalities of the NetworkCandidateGraph class
    """
    t1 = time.time()
    if not ncg.Session:
        raise BrokenPipeError('This func requires a database session from a NetworkCandidateGraph.')

    # Determine what sensor type to use
    avail_cams = {"isis", "csm"}
    cam_type = cam_type.lower()
    if cam_type not in cam_type:
        raise Exception(f'{cam_type} is not one of valid camera: {avail_cams}')

    points = []
    semi_major = ncg.config['spatial']['semimajor_rad']
    semi_minor = ncg.config['spatial']['semiminor_rad']

    ta = time.time()
    # Determine the point distribution in the overlap geom
    geom = overlap.geom
    valid = compgeom.distribute_points_in_geom(geom, **distribute_points_kwargs, **kwargs)
    if not valid.any():
        warnings.warn(f'Failed to distribute points in overlap {overlap.id}')
        return []

    log.info(f'Have {len(valid)} potential points to place in overlap {overlap.id}.')
    tb = time.time()
    log.info(f'Point distribution took {tb-ta} seconds.')
    # Setup the node objects that are covered by the geom
    nodes = []
    with ncg.session_scope() as session:
        for id in overlap.intersections:
            res = session.query(Images).filter(Images.id == id).one()
            nn = NetworkNode(node_id=id, image_path=res.path)
            nn.parent = ncg
            nodes.append(nn)
    tc = time.time()
    log.info(f'Took {tc-tb} seconds to instantiate {len(nodes)} images.')


    log.info(f'Attempting to place measures in {len(nodes)} images.')
    for v in valid:
        log.debug(f'Valid point: {v}')
        lon = v[0]
        lat = v[1]

        # Calculate the height, the distance (in meters) above or
        # below the aeroid (meters above or below the BCBF spheroid).
        height = ncg.dem.get_height(lat, lon)

        # Need to get the first node and then convert from lat/lon to image space
        for reference_index, node in enumerate(nodes):
            log.debug(f'Starting with reference_index: {reference_index}')
            # reference_index is the index into the list of measures for the image that is not shifted and is set at the
            # reference against which all other images are registered.
            if cam_type == "isis":
                try:
                    sample, line = isis.ground_to_image(node["image_path"], lon, lat)
                except CalledProcessError as e:
                    if 'Requested position does not project in camera model' in e.stderr:
                        log.exception(f'point ({lon}, {lat}) does not project to reference image {node["image_path"]}')
                        continue
            if cam_type == "csm":
                import csmapi
                lon_og, lat_og = oc2og(lon, lat, semi_major, semi_minor)
                x, y, z = reproject([lon_og, lat_og, height],
                                    semi_major, semi_minor,
                                    'latlon', 'geocent')
                # The CSM conversion makes the LLA/ECEF conversion explicit
                gnd = csmapi.EcefCoord(x, y, z)
                image_coord = node.camera.groundToImage(gnd)
                sample, line = image_coord.samp, image_coord.line

            # Extract ORB features in a sub-image around the desired point
            image_roi = roi.Roi(node.geodata, sample, line, size_x=size, size_y=size)
            if image_roi.variance == 0:
                log.warning(f'Failed to find interesting features in image {node.image_name}.')
                continue
            # Extract the most interesting feature in the search window
            image_roi.clip()
            interesting = extract_most_interesting(image_roi.clipped_array)
            if interesting is not None:
                # We have found an interesting feature and have identified the reference point.
                break
        log.debug(f'Current reference index: {reference_index}.')
        if interesting is None:
            log.warning('Unable to find an interesting point, falling back to the a priori pointing')
            newsample = sample
            newline = line
        else:
            # kps are in the image space with upper left origin and the roi
            # could be the requested size or smaller if near an image boundary.
            # So use the roi upper left_x and top_y for the actual origin.
            left_x, _, top_y, _ = image_roi.image_extent
            newsample = left_x + interesting.x
            newline = top_y + interesting.y

        # Get the updated lat/lon from the feature in the node
        if cam_type == "isis":
            try:
                p = isis.point_info(node["image_path"], newsample, newline, point_type="image")
            except CalledProcessError as e:
                if 'Requested position does not project in camera model' in e.stderr:
                    log.exception(node["image_path"])
                    log.exception(f'interesting point ({newsample}, {newline}) does not project back to ground')
                    continue
            try:
                x, y, z = p["BodyFixedCoordinate"].value
            except:
                x, y, z = ["BodyFixedCoordinate"]

            if getattr(p["BodyFixedCoordinate"], "units", "None").lower() == "km":
                x = x * 1000
                y = y * 1000
                z = z * 1000
        elif cam_type == "csm":
            import csmapi

            image_coord = csmapi.ImageCoord(newline, newsample)
            pcoord = node.camera.imageToGround(image_coord)
            # Get the BCEF coordinate from the lon, lat
            updated_lon_og, updated_lat_og, _ = reproject([pcoord.x, pcoord.y, pcoord.z],
                                                           semi_major, semi_minor, 'geocent', 'latlon')
            updated_lon, updated_lat = og2oc(updated_lon_og, updated_lat_og, semi_major, semi_minor)

            updated_height = ncg.dem.get_height(updated_lat, updated_lon)


            # Get the BCEF coordinate from the lon, lat
            x, y, z = reproject([updated_lon_og, updated_lat_og, updated_height],
                                semi_major, semi_minor, 'latlon', 'geocent')

        # If the updated point is outside of the overlap, then revert back to the
        # original point and hope the matcher can handle it when sub-pixel registering
        updated_lon_og, updated_lat_og, updated_height = reproject([x, y, z], semi_major, semi_minor,
                                                             'geocent', 'latlon')
        updated_lon, updated_lat = og2oc(updated_lon_og, updated_lat_og, semi_major, semi_minor)

        if not geom.contains(shapely.geometry.Point(updated_lon, updated_lat)):
            lon_og, lat_og = oc2og(lon, lat, semi_major, semi_minor)
            x, y, z = reproject([lon_og, lat_og, height],
                                semi_major, semi_minor, 'latlon', 'geocent')
            updated_lon_og, updated_lat_og, updated_height = reproject([x, y, z], semi_major, semi_minor,
                                                                 'geocent', 'latlon')
            updated_lon, updated_lat = og2oc(updated_lon_og, updated_lat_og, semi_major, semi_minor)

        point_geom = shapely.geometry.Point(x, y, z)
        log.debug(f'Creating point with reference_index: {reference_index}')
        point = Points(identifier=identifier,
                       overlapid=overlap.id,
                       apriori=point_geom,
                       adjusted=point_geom,
                       pointtype=point_type, # Would be 3 or 4 for ground
                       cam_type=cam_type,
                       reference_index=reference_index)


        for current_index, node in enumerate(nodes):
            if cam_type == "csm":
                # Compute ground point to back project into measures
                gnd = csmapi.EcefCoord(x, y, z)
                image_coord = node.camera.groundToImage(gnd)
                sample, line = image_coord.samp, image_coord.line
            if cam_type == "isis":
                # If this try/except fails, then the reference_index could be wrong because the length
                # of the measures list is different than the length of the nodes list that was used
                # to find the most interesting feature.
                try:
                    sample, line = isis.ground_to_image(node["image_path"], updated_lon, updated_lat)
                #except CalledProcessError as e:
                except:  # CalledProcessError is not catching the ValueError that this try/except is attempting to handle.
                    log.exception(f'interesting point ({updated_lon},{updated_lat}) does not project to image {node["image_path"]}')
                    # If the current_index is greater than the reference_index, the change in list size does
                    # not impact the positional index of the reference. If current_index is less than the
                    # reference_index, then the reference_index needs to de-increment by one for each time
                    # a measure fails to be placed.
                    if current_index < reference_index:
                        reference_index -= 1
                    log.debug('Reference de-incremented.')
                    continue

            point.measures.append(Measures(sample=sample,
                                           line=line,
                                           apriorisample=sample,
                                           aprioriline=line,
                                           imageid=node['node_id'],
                                           serial=node.isis_serial,
                                           measuretype=3,
                                           choosername='place_points_in_overlap'))
        log.debug(f'Current reference index in code: {reference_index}.')
        log.debug(f'Current reference index on point: {point.reference_index}')
        if len(point.measures) >= 2:
            points.append(point)
    log.info(f'Able to place {len(points)} points.')

    if not points: return

    # Insert the points into the database asynchronously (via redis) or synchronously via the ncg
    if use_cache:
        pipeline = ncg.redis_queue.pipeline()
        msgs = [json.dumps(point.to_dict(_hide=[]), cls=JsonEncoder) for point in points]
        pipeline.rpush(ncg.point_insert_queue, *msgs)
        pipeline.execute()
        # Push
        log.info('Using the cache')
        # ncg.redis_queue.rpush(ncg.point_insert_queue, *[json.dumps(point.to_dict(_hide=[]), cls=JsonEncoder) for point in points])
        ncg.redis_queue.incr(ncg.point_insert_counter, amount=len(points))
    else:
        with ncg.session_scope() as session:
            for point in points:
                session.add(point)
    t2 = time.time()
    log.info(f'Total processing time was {t2-t1} seconds.')

    return

def place_points_in_image(image,
                          identifier="autocnet",
                          cam_type="csm",
                          size=71,
                          distribute_points_kwargs={},
                          ncg=None,
                          **kwargs):
    """
    Place points into an image and then attempt to place measures
    into all overlapping images. This function is funcitonally identical
    to place_point_in_overlap except it works on individual images.

    Parameters
    ----------
    image : obj
            An autocnet Images model object

    identifier: str
                The tag used to distiguish points laid down by this function.

    cam_type : str
               options: {"csm", "isis"}
               Pick what kind of camera model implementation to use

    size : int
           The size of the window used to extractor features to find an
           interesting feature to which the point is shifted.

    distribute_points_kwargs: dict
                              kwargs to pass to autocnet.cg.cg.distribute_points_in_geom

    ncg: obj
         An autocnet.graph.network NetworkCandidateGraph instance representing the network
         to apply this function to

    See Also
    --------
    autocnet.cg.cg.distribute_points_in_geom: for the possible arguments to pass through using disribute_points_kwargs.
    autocnet.graph.network.NetworkCandidateGraph: for associated properties and functionalities of the NetworkCandidateGraph class
    """
    # Arg checking
    if not ncg.Session:
        raise BrokenPipeError('This func requires a database session from a NetworkCandidateGraph.')

    # Determine what sensor type to use
    avail_cams = {"isis", "csm"}
    cam_type = cam_type.lower()
    if cam_type not in cam_type:
        raise Exception(f'{cam_type} is not one of valid camera: {avail_cams}')

    points = []
    semi_major = ncg.config['spatial']['semimajor_rad']
    semi_minor = ncg.config['spatial']['semiminor_rad']

    # Logic
    geom = image.geom
    # Put down a grid of points over the image; the density is intentionally high
    valid = compgeom.distribute_points_in_geom(geom, **distribute_points_kwargs)
    log.info(f'Have {len(valid)} potential points to place.')
    for v in valid:
        lon = v[0]
        lat = v[1]
        point_geometry = f'SRID=104971;POINT({v[0]} {v[1]})'

        # Calculate the height, the distance (in meters) above or
        # below the aeroid (meters above or below the BCBF spheroid).
        height = ncg.dem.get_height(lat, lon)

        with ncg.session_scope() as session:
            intersecting_images = session.query(Images.id, Images.path).filter(Images.geom.ST_Intersects(point_geometry)).all()
            node_res= [i for i in intersecting_images]
            nodes = []

            for nid, image_path  in node_res:
                # Setup the node objects that are covered by the geom
                nn = NetworkNode(node_id=nid, image_path=image_path)
                nn.parent = ncg
                nodes.append(nn)

        # Need to get the first node and then convert from lat/lon to image space
        node = nodes[0]
        if cam_type == "isis":
            try:
                sample, line = isis.ground_to_image(node["image_path"], lon, lat)
            except CalledProcessError as e:
                if 'Requested position does not project in camera model' in e.stderr:
                    log.exception(f'point ({lon}, {lat}) does not project to reference image {node["image_path"]}')
                    continue
        if cam_type == "csm":
            lon_og, lat_og = oc2og(lon, lat, semi_major, semi_minor)
            x, y, z = reproject([lon_og, lat_og, height],
                                semi_major, semi_minor,
                                'latlon', 'geocent')
            # The CSM conversion makes the LLA/ECEF conversion explicit
            gnd = csmapi.EcefCoord(x, y, z)
            image_coord = node.camera.groundToImage(gnd)
            sample, line = image_coord.samp, image_coord.line

        # Extract ORB features in a sub-image around the desired point
        image_roi = roi.Roi(node.geodata, sample, line, size_x=size, size_y=size)
        image_roi.clip()
        try:
            interesting = extract_most_interesting(image.clipped_array)
        except:
            continue

        # kps are in the image space with upper left origin and the roi
        # could be the requested size or smaller if near an image boundary.
        # So use the roi upper left_x and top_y for the actual origin.
        left_x, _, top_y, _ = image_roi.image_extent
        newsample = left_x + interesting.x
        newline = top_y + interesting.y

        # Get the updated lat/lon from the feature in the node
        if cam_type == "isis":
            try:
                p = isis.point_info(node["image_path"], newsample, newline, point_type="image")
            except CalledProcessError as e:
                if 'Requested position does not project in camera model' in e.stderr:
                    log.exception(node["image_path"])
                    log.exception(f'interesting point ({newsample}, {newline}) does not project back to ground')
                    continue
            try:
                x, y, z = p["BodyFixedCoordinate"].value
            except:
                x, y, z = ["BodyFixedCoordinate"]

            if getattr(p["BodyFixedCoordinate"], "units", "None").lower() == "km":
                x = x * 1000
                y = y * 1000
                z = z * 1000
        elif cam_type == "csm":
            image_coord = csmapi.ImageCoord(newline, newsample)
            pcoord = node.camera.imageToGround(image_coord)
            # Get the BCEF coordinate from the lon, lat
            updated_lon_og, updated_lat_og, _ = reproject([pcoord.x, pcoord.y, pcoord.z],
                                                           semi_major, semi_minor, 'geocent', 'latlon')
            updated_lon, updated_lat = og2oc(updated_lon_og, updated_lat_og, semi_major, semi_minor)

            updated_height = ncg.dem.get_height(updated_lat, updated_lon)


            # Get the BCEF coordinate from the lon, lat
            x, y, z = reproject([updated_lon_og, updated_lat_og, updated_height],
                                semi_major, semi_minor, 'latlon', 'geocent')

        # If the updated point is outside of the overlap, then revert back to the
        # original point and hope the matcher can handle it when sub-pixel registering
        updated_lon_og, updated_lat_og, updated_height = reproject([x, y, z], semi_major, semi_minor,
                                                             'geocent', 'latlon')
        updated_lon, updated_lat = og2oc(updated_lon_og, updated_lat_og, semi_major, semi_minor)

        if not geom.contains(shapely.geometry.Point(updated_lon, updated_lat)):
            lon_og, lat_og = oc2og(lon, lat, semi_major, semi_minor)
            x, y, z = reproject([lon_og, lat_og, height],
                                semi_major, semi_minor, 'latlon', 'geocent')
            updated_lon_og, updated_lat_og, updated_height = reproject([x, y, z], semi_major, semi_minor,
                                                                 'geocent', 'latlon')
            updated_lon, updated_lat = og2oc(updated_lon_og, updated_lat_og, semi_major, semi_minor)

        point_geom = shapely.geometry.Point(x, y, z)

        # Insert a spatial query to find which overlap this is in.
        with ncg.session_scope() as session:
            oid = session.query(Overlay.id).filter(Overlay.geom.ST_Contains(point_geometry)).one()[0]

        point = Points(identifier=identifier,
                       overlapid=oid,
                       apriori=point_geom,
                       adjusted=point_geom,
                       pointtype=2, # Would be 3 or 4 for ground
                       cam_type=cam_type)

        for node in nodes:
            if cam_type == "csm":
                image_coord = node.camera.groundToImage(gnd)
                sample, line = image_coord.samp, image_coord.line
            if cam_type == "isis":
                try:
                    sample, line = isis.ground_to_image(node["image_path"], updated_lon, updated_lat)
                except CalledProcessError as e:
                    if 'Requested position does not project in camera model' in e.stderr:
                        log.exception(f'interesting point ({lon},{lat}) does not project to image {node["image_path"]}')

            point.measures.append(Measures(sample=sample,
                                           line=line,
                                           apriorisample=sample,
                                           aprioriline=line,
                                           imageid=node['node_id'],
                                           serial=node.isis_serial,
                                           measuretype=3,
                                           choosername='place_points_in_image'))

        if len(point.measures) >= 2:
            points.append(point)
    log.info(f'Able to place {len(points)} points.')
    Points.bulkadd(points, ncg.Session)

def add_measures_to_point(pointid, cam_type='isis', ncg=None, Session=None):
    if not ncg.Session:
        raise BrokenPipeError('This func requires a database session from a NetworkCandidateGraph.')

    if isinstance(pointid, Points):
        pointid = pointid.id


    with ncg.session_scope() as session:
        point = session.query(Points).filter(Points.id == pointid).one()
        point_lon = point.geom.x
        point_lat = point.geom.y

        reference_index = point.reference_index
        reference_measure = point.measures[reference_index]
        reference_image_id = reference_measure.imageid

        images = session.query(Images).filter(Images.geom.ST_Intersects(point._geom)).all()
        log.info(f'Placing measures into {len(images)-1} images.')
        for image in images:
            if image.id == reference_image_id:
                continue  # This is the reference image, so pass on adding a new measure

            if cam_type == "isis":
                try:
                    sample, line = isis.ground_to_image(image.path, point_lon, point_lat)
                except CalledProcessError as e:
                    if 'Requested position does not project in camera model' in e.stderr:
                        log.exception(f'interesting point ({point_lon},{point_lat}) does not project to image {image.name}')

            point.measures.append(Measures(sample=sample,
                                           line=line,
                                           apriorisample=sample,
                                           aprioriline=line,
                                           imageid=image.id,
                                           serial=image.serial,
                                           measuretype=3,
                                           choosername='add_measures_to_point'))
            i = 0
            for m in point.measures:
                if m.measuretype == 2 or m.measuretype == 3:
                    i += 1
            if i >= 2:
                point.ignore = False
