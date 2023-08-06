from math import isclose, ceil
import random
import warnings

import pandas as pd
import numpy as np
import networkx as nx
import geopandas as gpd
import ogr
import logging

from skimage import transform as tf
from scipy.spatial import Voronoi, Delaunay, ConvexHull
import shapely.geometry
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.affinity import scale
from shapely import wkt, geometry

from autocnet.utils import utils
from autocnet.cg import cg

from shapely.ops import cascaded_union, polygonize

# set up the logger file
log = logging.getLogger(__name__)

def two_point_extrapolate(x, xs, ys):
    """

    Parameters
    ----------
    x : float
             point where you want corresponding y value

    xs : ndarray
             (1, 2) array of point x coordinates

    ys : ndarray
             (1, 2) array of point x coordinates

    Returns
    -------
    y : float
            extrapolated value associated with x

    """

    m = (ys[1]-ys[0])/(xs[1]-xs[0])
    y = ys[0] + m*(x-xs[0])

    return x, y

def convex_hull_ratio(points, ideal_area):
    """

    Parameters
    ----------
    points : ndarray
             (n, 2) array of point coordinates

    ideal_area : float
                 The total area that could be covered

    Returns
    -------
    ratio : float
            The ratio convex hull volume / ideal_area

    """
    hull = ConvexHull(points)
    return hull.volume / ideal_area


def convex_hull(points):

    """

    Parameters
    ----------
    points : ndarray
             (n, 2) array of point coordinates

    Returns
    -------
    hull : 2-D convex hull
            Provides a convex hull that is used
            to determine coverage

    """

    if isinstance(points, pd.DataFrame) :
        points = pd.DataFrame(points).values

    hull = ConvexHull(points)
    return hull


def geom_mask(keypoints, geom): # ADDED
    """
    Masks any points that are outside of the bounds of the given
    geometry.

    Parameters
    ----------
    keypoints : dataframe
                      A pandas dataframe of points to mask

    geom : object
                Shapely geometry object to use as a mask
    """

    def _in_mbr(r, mbr):
        if (mbr[0] <= r.x <= mbr[2]) and (mbr[1] <= r.y <= mbr[3]):
            return True
        else:
            return False

    mbr = geom.bounds
    initial_mask = keypoints.apply(_in_mbr, axis=1, args=(mbr,))

    return initial_mask


def two_poly_overlap(poly1, poly2):
    """

    Parameters
    ----------
    poly1 : ogr polygon
            Any polygon that shares some kind of overlap
            with poly2

    poly2 : ogr polygon
            Any polygon that shares some kind of overlap
            with poly1

    Returns
    -------
    overlap_percn : float
                    The percentage of image overlap

    overlap_area : float
                   The total area of overalap

    """
    overlap_area_polygon = poly2.Intersection(poly1)
    overlap_area = overlap_area_polygon.GetArea()
    area1 = poly1.GetArea()
    area2 = poly2.GetArea()

    overlap_percn = (overlap_area / (area1 + area2 - overlap_area)) * 100
    return overlap_percn, overlap_area, overlap_area_polygon


def get_area(poly1, poly2):
    """

    Parameters
    ----------
    poly1 : ogr polygon
            General ogr polygon

    poly2 : ogr polygon
            General ogr polygon

    Returns
    -------
    intersection_area : float
                        returns the intersection area
                        of two polygons

    """
    intersection_area = poly1.Intersection(poly2).GetArea()
    return intersection_area


def compute_voronoi(keypoints, intersection=None, geometry=False, s=30): # ADDED
        """
        Creates a voronoi diagram for all edges in a graph, and assigns a given
        weight to each edge. This is based around voronoi polygons generated
        by scipy's voronoi method, to determine if an image has significant coverage.

        Parameters
        ----------
        graph : object
               A networkx graph object

        clean_keys : list
                     Of strings used to apply masks to omit correspondences

        s : int
            Offset for the corners of the image
        """
        vor_keypoints = []

        keypoints.apply(lambda x: vor_keypoints.append((x['x'], x['y'])), axis = 1)

        if intersection is None:
            keypoint_bounds = Polygon(vor_keypoints).bounds
            intersection = shapely.geometry.box(keypoint_bounds[0], keypoint_bounds[1],
                                                    keypoint_bounds[2], keypoint_bounds[3])

        scaled_coords = np.array(scale(intersection, s, s).exterior.coords)

        vor_keypoints = np.vstack((vor_keypoints, scaled_coords))
        vor = Voronoi(vor_keypoints)
        # Might move the code below to its own method depending on feedback
        if geometry:
            voronoi_df = gpd.GeoDataFrame(data = keypoints, columns=['x', 'y', 'weight', 'geometry'])
        else:
            voronoi_df = gpd.GeoDataFrame(data = keypoints, columns=['x', 'y', 'weight'])

        i = 0
        vor_points = np.asarray(vor.points)
        for region in vor.regions:
            region_point = vor_points[np.argwhere(vor.point_region==i)]

            if not -1 in region:
                polygon_points = [vor.vertices[i] for i in region]

                if len(polygon_points) != 0:
                    polygon = Polygon(polygon_points)

                    intersection_poly = polygon.intersection(intersection)

                    voronoi_df.loc[(voronoi_df["x"] == region_point[0][0][0]) &
                                   (voronoi_df["y"] == region_point[0][0][1]),
                                   'weight'] = intersection_poly.area
                    if geometry:
                        voronoi_df.loc[(voronoi_df["x"] == region_point[0][0][0]) &
                                       (voronoi_df["y"] == region_point[0][0][1]),
                                       'geometry'] = intersection_poly
            i += 1

        return voronoi_df

def single_centroid(geom):
    """
    For a geom, return the centroid

    Parameters
    ----------
    geom : shapely.geom object

    Returns
    -------

     : list
            in the form [(x,y)]
    """
    x, y = geom.centroid.xy
    return [(x[0],y[0])]

def nearest(pt, search):
    """
    Fine the index of nearest (Euclidean) point in a list
    of points.

    Parameters
    ----------
    pt : ndarray
         (2,1) array
    search : ndarray
             (n,2) array of points to search within. The
             returned index is the closet point in this set
             to the search

    Returns
    -------
     : int
       The index to the nearest point.
    """
    return np.argmin(np.sum((search - pt)**2, axis=1))

def create_points_along_line(p1, p2, npts):
    """
    Compute a set of nodes equally spaced between
    two points, not including the end points.

    Parameters
    ----------
    p1 : iterable
         in the form (x,y)

    p2 : iterable
         in the form(x,y)

    npts : int
           The number of nodes to be returned

    Returns
    -------
     : ndarray
       (n,2) array of nodes
    """
    # npts +2 since the endpoints are included in linspace
    # but this func clips them
    return np.linspace(p1, p2, npts+2)[1:-1]

def xy_in_polygon(x,y, geom):
    """
    Returns true is an x,y pair is contained within
    the geom.

    Parameters
    ----------
    x : Number
        The x coordinate

    y : Number
        The y coordinate

    Returns
    -------
     : bool
       True if the point is contained within the geom.
    """
    return geom.contains(Point(x, y))

def generate_random(number, polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    i = 0
    while len(points) < number and i < 1000:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append([pnt.x, pnt.y])
        i += 1
    return np.asarray(points)

def distribute_points_classic(geom, nspts, ewpts, use_mrr=True, **kwargs):
    """
    This is a decision tree that attempts to perform a
    very simplistic approximation of the shape
    of the geometry and then place some number of
    north/south and east/west points into the geometry.

    Parameters
    ----------
    geom : shapely.geom
           A shapely geometry object

    nspts : int
            The number of points to attempt to place
            in the N/S (up/down) direction

    ewpts : int
            The number of points to attempt to place
            in the E/W (right/left) direction
    
    use_mrr : boolean
              If True (default) compute the minimum rotated rectangle bounding
              the geometry

    Returns
    -------
    valid : list
            of point coordinates in the form [(x1,y1), (x2,y2), ..., (xn, yn)]
    """
    original_geom = geom
    if use_mrr:
        geom = geom.minimum_rotated_rectangle
        
    geom_coords = np.column_stack(geom.exterior.xy)
    coords = np.array(list(zip(*geom.envelope.exterior.xy))[:-1])

    ll = coords[0]
    lr = coords[1]
    ur = coords[2]
    ul = coords[3]

    # Find the points nearest the ul and ur
    ul_actual = geom_coords[nearest(ul, geom_coords)]
    ur_actual = geom_coords[nearest(ur, geom_coords)]
    newtop = create_points_along_line(ul_actual, ur_actual, ewpts)

    # Find the points nearest the ll and lr
    ll_actual = geom_coords[nearest(ll, geom_coords)]
    lr_actual = geom_coords[nearest(lr, geom_coords)]
    newbot = create_points_along_line(ll_actual, lr_actual, ewpts)

    points = []
    for i in range(len(newtop)):
        top = newtop[i]
        bot = newbot[i]

        line_of_points = create_points_along_line(top, bot, nspts)
        points.append(line_of_points)

    if len(points) < 1:
        return []

    points = np.vstack(points)
    # Perform a spatial intersection check to eject points that are not valid
    valid = [p for p in points if xy_in_polygon(p[0], p[1], original_geom)]
    # The standard method failed. Attempt random placement within the geometry
    if not valid:
        valid = generate_random(ewpts * nspts, original_geom)
    return valid

def distribute_points_new(geom, nspts, ewpts, Session):
    """
    This is a decision tree that attempts to perform a
    very simplistic approximation of the shape
    of the geometry and then place some number of
    north/south and east/west points into the geometry.
    This function works best on bulky geometries, such as
    a combination of all network image footprints.

    Parameters
    ----------
    geom : shapely.geom
           A shapely geometry object which is a union of
           all of the image footprints in the network
           that is being grounded.

    nspts : int
            The number of points to attempt to place
            in the N/S (up/down) direction

    ewpts : int
            The number of points to attempt to place
            in the E/W (right/left) direction

    Returns
    -------
    valid : list
            of point coordinates in the form [(x1,y1), (x2,y2), ..., (xn, yn)]
    """
    coords = np.array(list(zip(*geom.envelope.exterior.xy))[:-1])

    ll = coords[0]
    lr = coords[1]
    ur = coords[2]
    ul = coords[3]

    rr_coords = np.array(list(zip(*geom.minimum_rotated_rectangle.exterior.xy))[:-1])
    w = min([i[0] for i in rr_coords])
    s = min([i[1] for i in rr_coords])
    swid = nearest([w, s], rr_coords)
    rr_coords = np.vstack([rr_coords[swid:], rr_coords[0:swid]]) # reorder to match envelope/coords order

    x = np.linspace(ul[0], ur[0], ewpts+2)[1:-1]
    y = np.linspace(ul[1], ll[1], nspts+2)[1:-1]

    grid = np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])

    if len(grid) < 1:
        return []

    affine = tf.estimate_transform('affine', coords, rr_coords)
    rr_grid = affine(grid)

    # Perform a spatial intersection check to eject points that are not valid
    valid = [p for p in rr_grid if xy_in_polygon(p[0], p[1], geom)]
    return valid

def distribute_points_in_geom(geom, method="classic",
                              nspts_func=lambda x: ceil(round(x,1)*10),
                              ewpts_func=lambda x: ceil(round(x,1)*5),
                              Session=None,
                              **kwargs):
    """
    Given a geometry, attempt a basic classification of the shape.
    RIght now, this simply attempts to determine if the bounding box
    is generally N/S or generally E/W trending. Once the determination
    is made, the algorithm places points in the geometry and returns
    a list of valid (intersecting) points.

    The kwargs for this algorithm take a function that expects a number
    as an input and returns an integer number of points to place. The
    input number is the distance between the top/bottom or left/right
    sides of the geometry.

    This algorithm does not know anything about the units being used
    so the caller is responsible for acocunting for units (if appropriate)
    in the passed funcs.

    Parameters
    ----------
    geom : shapely.geom object
           The geometry object

    nspts_func : obj
                 Function taking a Number and returning an int

    ewpts_func : obj
                 Function taking a Number and returning an int

    Returns
    -------
    valid : np.ndarray
            of valid points in the form (x,y) or (lon,lat)

    """

    point_funcs = {
        "classic" :  distribute_points_classic,
        "new" : distribute_points_new
    }

    point_distribution_func = point_funcs[method]

    coords = list(zip(*geom.envelope.exterior.xy))
   

    # This logic is kwarg swapping - need to trace this logic.
    short = np.inf
    long = -np.inf
    shortid = 0
    longid = 0
    for i, p in enumerate(coords[:-1]):
        d = np.sqrt((coords[i+1][0] - p[0])**2+(coords[i+1][1]-p[1])**2)
        if d < short:
            short = d
            shortid = i
        if d > long:
            long = d
            longid = i
    ratio = short/long
    
    ns = False
    ew = False
    valid = []
    
    # The polygons should be encoded with a lower left origin in counter-clockwise direction.
    # Therefore, if the 'bottom' is the short edge it should be id 0 and modulo 2 == 0.
    if shortid % 2 == 0:
        # Also if the geom is a perfect square
        ns = True
    elif longid % 2 == 0:
        ew = True

    # Decision Tree
    if ratio < 0.1 and geom.area < 0.01:
        # Class: Slivers - ignore.
        return np.array([])
    elif geom.area <= 0.004 and ratio >= 0.25:
        # Single point at the centroid
        valid = single_centroid(geom)
    elif ns==True:
        # Class, north/south poly, multi-point
        nspts = nspts_func(long)
        ewpts = ewpts_func(short)
        if nspts == 1 and ewpts == 1:
            valid = single_centroid(geom)
        else:
            valid = point_distribution_func(geom, nspts, ewpts, Session=Session, **kwargs)
    elif ew == True:
        # Since this is an LS, we should place these diagonally from the 'lower left' to the 'upper right'
        nspts = ewpts_func(short)
        ewpts = nspts_func(long)
        if nspts == 1 and ewpts == 1:
            valid = single_centroid(geom)
        else:
            valid = point_distribution_func(geom, nspts, ewpts, Session=Session, **kwargs)
    else:
        log.warning('WTF Willy')
    return np.array(valid)


def alpha_shape(points, alpha):
    """
    Compute a convex hull from a set of points.

    credit: https://gist.github.com/dwyerk/10561690

    Parameters
    ----------

    points : np.array
             points in the format [[x0,y0], [x1, y,1], ... [xn, yn]]

    alpha : float
            Higher alphas creater a tighter the boundery around input points, alphas approaching 0 create a convex hull.
            Best to keep in the range (0, 1]


    Returns
    -------

    convex_hull : shapely.geometry.Polygon
                  Shapely polygon of the convex hull

    """
    tri = Delaunay(points)
    triangles = points[tri.vertices]
    a = ((triangles[:,0,0] - triangles[:,1,0]) ** 2 + (triangles[:,0,1] - triangles[:,1,1]) ** 2) ** 0.5
    b = ((triangles[:,1,0] - triangles[:,2,0]) ** 2 + (triangles[:,1,1] - triangles[:,2,1]) ** 2) ** 0.5
    c = ((triangles[:,2,0] - triangles[:,0,0]) ** 2 + (triangles[:,2,1] - triangles[:,0,1]) ** 2) ** 0.5
    s = ( a + b + c ) / 2.0
    areas = (s*(s-a)*(s-b)*(s-c)) ** 0.5
    circums = a * b * c / (4.0 * areas)

    # avoid devide by zero
    thresh = 1.0/alpha if alpha is not 0 else circums.max()
    filtered = triangles[circums < thresh]

    edge1 = filtered[:,(0,1)]
    edge2 = filtered[:,(1,2)]
    edge3 = filtered[:,(2,0)]
    edge_points = np.unique(np.concatenate((edge1,edge2,edge3)), axis = 0).tolist()
    m = geometry.MultiLineString(edge_points)
    triangles = list(cg.polygonize(m))
    return cascaded_union(triangles)


def rasterize_polygon(shape, vertices, dtype=bool):
    """
    Simple tool to convert poly into a boolean numpy array.

    source: https://stackoverflow.com/questions/37117878/generating-a-filled-polygon-inside-a-numpy-array

    Parameters
    ----------

    shape : tuple
            size of the array in (y,x) format

    vertices : np.array, list
               array of vertices in [[x0, y0], [x1, y1]...] format

    dtype : type
            datatype of output mask

    Returns
    -------

    mask : np.array
           mask with filled polygon set to true

    """
    def check(p1, p2, base_array):
        idxs = np.indices(base_array.shape) # Create 3D array of indices

        p1 = p1.astype(float)
        p2 = p2.astype(float)

        # Calculate max column idx for each row idx based on interpolated line between two points
        if p1[0] == p2[0]:
            max_col_idx = (idxs[0] - p1[0]) * idxs.shape[1]
            sign = np.sign(p2[1] - p1[1])
        else:
            max_col_idx = (idxs[0] - p1[0]) / (p2[0] - p1[0]) * (p2[1] - p1[1]) + p1[1]
            sign = np.sign(p2[0] - p1[0])

        return idxs[1] * sign <= max_col_idx * sign

    base_array = np.zeros(shape, dtype=dtype)  # Initialize your array of zeros

    fill = np.ones(base_array.shape) * True  # Initialize boolean array defining shape fill

    # Create check array for each edge segment, combine into fill array
    for k in range(vertices.shape[0]):
        fill = np.all([fill, check(vertices[k-1], vertices[k], base_array)], axis=0)

    log.info(fill.any())
    # Set all values inside polygon to one
    base_array[fill] = 1
    return base_array
