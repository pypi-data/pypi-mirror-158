import numpy as np

import matplotlib
from matplotlib.path import Path
import cv2

from sklearn.cluster import  OPTICS
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

from skimage.feature import blob_log, blob_doh
from math import sqrt, atan2, pi
from hoggorm.mat_corr_coeff import RVcoeff
import math
import logging

import scipy
from scipy.spatial import cKDTree

from plio.io.io_gdal import GeoDataset

from shapely import wkt
from shapely.geometry import Point, MultiPoint, Polygon

import richdem as rd

import pandas as pd
import geopandas as gpd

try:
    import kalasiris as isis
except Exception as exception:
    from autocnet.utils.utils import FailedImport
    isis = FailedImport(exception)


from autocnet.utils.utils import bytescale
from autocnet.matcher.cpu_extractor import extract_features
from autocnet import cg

# set up the logger file
log = logging.getLogger(__name__)

def image_diff(arr1, arr2):
    """
    Diff two images but accounts for null pixels. Intended to be used with change 
    detection algorithms.  

    Parameters 
    ----------

    arr1 : np.ndarray
           2D numpy array containing the first image, must have the same shape as arr2

    arr2 : np.ndarray 
           2D numpy array containing the second image, must have the same shape as arr1

    Returns
    -------

    : np.ndarray 
      new diffed image 
    """
    arr1 = arr1.astype("float32")
    arr2 = arr2.astype("float32")
    arr1[arr1 == 0] = np.nan
    arr2[arr2 == 0] = np.nan

    isis_null = isis.specialpixels.Real.Null
    arr1[arr1 == isis_null] = np.nan
    arr2[arr2 == isis_null] = np.nan

    diff = arr1-arr2
    diff[np.isnan(diff)] = 0

    return diff


def image_ratio(arr1, arr2):
    """
    Gets the ratio of two images but accounts for null and zero pixels. Intended to be used with change 
    detection algorithms.  

    Parameters 
    ----------

    arr1 : np.ndarray
           2D numpy array containing the first image, must have the same shape as arr2

    arr2 : np.ndarray 
           2D numpy array containing the second image, must have the same shape as arr1

    Returns
    -------

    : np.ndarray 
      new image containing ratioed pixels
    """
    arr1 = arr1.astype("float32")
    arr2 = arr2.astype("float32")
    arr1[arr1 == 0] = np.nan
    arr2[arr2 == 0] = np.nan

    isis_null = isis.specialpixels.Real.Null
    arr1[arr1 == isis_null] = np.nan
    arr2[arr2 == isis_null] = np.nan

    ratio = arr1/arr2
    ratio[np.isnan(ratio)] = 0

    return ratio


def image_diff_sq(arr1, arr2):
     """
     Diff two images but accounts for null pixels then squares the result. Intended to be used with change 
     detection algorithms.  

     Parameters 
     ----------

     arr1 : np.ndarray
            2D numpy array containing the first image, must have the same shape as arr2

     arr2 : np.ndarray 
            2D numpy array containing the second image, must have the same shape as arr1

     Returns
     -------
     
     : np.ndarray 
       new image containing diffed pixels
     """
     return image_diff(arr1, arr2)**2


func_map = {
    "diff" : image_diff,
    "diff_sq": image_diff_sq,
    "ratio" : image_ratio
}


def okubogar_detector(image1, image2, nbins=50, extractor_method="orb", image_func=image_diff,
                      extractor_kwargs={"nfeatures": 2000, "scaleFactor": 1.1, "nlevels": 1}):
     """
     Simple change detection algorithm which produces an overlay image of change hotspots
     (i.e. a 2d histogram image of detected change density).

     Largely based on a method created by Chris Okubo and Brendon Bogar. Histogram step
     was added for readability.

     image1, image2 -> image subtraction/ratio -> feature extraction -> feature histogram

     TODO: Paper/abstract might exist, cite

     Parameters
     ----------

     image1 : np.array, plio.GeoDataset
             Image representing the "before" state of the ROI, can be a 2D numpy array or plio GeoDataset

     image2 : np.array, plio.GeoDataset
             Image representing the "after" state of the ROI, can be a 2D numpy array or plio GeoDataset

     image_func : callable
                  Function used to create a derived image from image1 and image2, which in turn is
                  the input for the feature extractor. The first two arguments are 2d numpy arrays, image1 and image2,
                  and must return a 2d numpy array. Default function returns a difference image.

                  Example func:

                  >>> from numpy import random
                  >>> image1, image2 = random.random((50,50)), random.random((50,50))
                  >>> def ratio(image1, image2):
                  >>>   # do stuff with image1 and image2
                  >>>   new_image = image1/image2
                  >>>   return new_image # must return a single variable, a 2D numpy array
                  >>> results = okubogar_detector(image1, image2, image_func=ratio)

                  Or, alternatively:

                  >>> from numpy import random
                  >>> image1, image2 = random.random((50,50)), random.random((50,50))
                  >>> results = okubogar_detector(image1, image2, image_func=lambda im1, im2: im1/im2)

     nbins : int
            number of bins to use in the 2d histogram

     extractor_method : {'orb', 'sift', 'fast', 'surf', 'vl_sift'}
               The detector method to be used.  Note that vl_sift requires that
               vlfeat and cyvlfeat dependencies be installed.

     extractor_kwargs : dict
                        A dictionary containing OpenCV SIFT parameters names and values.

     Returns
     -------
     : pd.DataFrame
       Dataframe containing polygon results as wkt

     : np.array
       Numpy array image, the image used to compute change

     See Also
     --------
     autocnet.matcher.cpu_extractor.extract_features : for description of information associated with the feature extractor

     """
     if isinstance(image1, GeoDataset):
         image1 = image1.read_array()

     if isinstance(image2, GeoDataset):
         image2 = image2.read_array()

     if isinstance(image_func, str):
         try:
             image_func = func_map[image_func]
         except KeyError as e:
             raise Exception(f"{image_func} is not a valid method, available image functions: {func_map.keys()}")

     image1[image1 == image1.min()] = 0
     image2[image2 == image2.min()] = 0
     arr1 = bytescale(image1)
     arr2 = bytescale(image2)

     bdiff = image_func(arr1, arr2)

     keys, descriptors = extract_features(bdiff, extractor_method, extractor_parameters=extractor_kwargs)
     x,y = keys["x"], keys["y"]

     heatmap, xedges, yedges = np.histogram2d(y, x, bins=nbins, range=[[0, bdiff.shape[0]], [0, bdiff.shape[1]]])
     heatmap = cv2.resize(heatmap, dsize=(bdiff.shape[1], bdiff.shape[0]), interpolation=cv2.INTER_NEAREST)

     #square image to improve signal to noise ratio
     heatmap = heatmap**2

     keys = gpd.GeoDataFrame(keys, geometry= gpd.points_from_xy(keys.x, keys.y))

     return keys, heatmap, bdiff


def okbm_detector(image1, image2, extractor_method="orb",  image_func=image_diff,
                 extractor_kwargs={"nfeatures": 2000, "scaleFactor": 1.1, "nlevels": 1},
                 cluster_kwargs={"min_samples": 10, "max_eps": 10, "eps": .5, "xi":.5}):
     """
     okobubogar modified detector, experimental feature based change detection algorithmthat expands on okobubogar to allow for
     programmatic change detection. Returns detected feature changes as weighted polygons.


     Parameters
     ----------

     image1 : GeoDataset
             Image representing the "before" state of the ROI, can be a 2D numpy array or plio GeoDataset

     image2 : GeoDataset
             Image representing the "after" state of the ROI, can be a 2D numpy array or plio GeoDataset

     image_func : callable
                  Function used to create a derived image from image1 and image2, which in turn is
                  the input for the feature extractor. The first two arguments are 2d numpy arrays, image1 and image2,
                  and must return a 2d numpy array. Default function returns a difference image.

                  Example func:

                  >>> from numpy import random
                  >>> image1, image2 = random.random((50,50)), random.random((50,50))
                  >>> def ratio(image1, image2):
                  >>>   # do stuff with image1 and image2
                  >>>   new_image = image1/image2
                  >>>   return new_image # must return a single variable, a 2D numpy array
                  >>> results = okbm_detector(image1, image2, image_func=ratio)

                  Or, alternatively:

                  >>> from numpy import random
                  >>> image1, image2 = random.random((50,50)), random.random((50,50))
                  >>> results = okbm_detector(image1, image2, image_func=lambda im1, im2: im1/im2)

     extractor_method : {'orb', 'sift', 'fast', 'surf', 'vl_sift'}
               The detector method to be used.  Note that vl_sift requires that
               vlfeat and cyvlfeat dependencies be installed.

     extractor_kwargs : dict
                        A dictionary containing OpenCV SIFT parameters names and values.

     cluster_kwargs : dict
                      A dictionary containing sklearn.cluster.OPTICS parameters

     Returns
     -------
     : pd.DataFrame
       Dataframe containing polygon results as wkt

     : np.array
       Numpy array image, the image used to compute change

     """
     keys, _, bdiff = okubogar_detector(image1, image2, 10, extractor_method, image_func, extractor_kwargs)

     x,y = keys['x'], keys['y']
     points = [Point(xval, yval) for xval,yval in zip(x,y)]

     optics = OPTICS(**cluster_kwargs).fit(list(zip(x,y)))

     classes = gpd.GeoDataFrame(columns=["label", "point"], geometry="point")
     classes["label"] = optics.labels_
     classes["point"] = points
     class_groups = classes.groupby("label").groups

     polys = []
     weights = []

     # array of x,y pairs
     xv, yv = np.mgrid[0:bdiff.shape[1], 0:bdiff.shape[0]]

     for label, indices in class_groups.items():
         if label == -1:
             continue

         points = classes.loc[indices]["point"]
         poly = MultiPoint(points.__array__()).convex_hull
         xmin, ymin, xmax, ymax = np.asarray(poly.bounds).astype("uint64")
         xv, yv = np.mgrid[xmin:xmax, ymin:ymax]
         xv = xv.flatten()
         yv = yv.flatten()

         points = np.vstack((xv,yv)).T.astype("uint64")

         mask = Path(np.asarray(poly.exterior.xy).T.astype("uint64")).contains_points(points).reshape(int(ymax-ymin), int(xmax-xmin))
         weight = bdiff[ymin:ymax,xmin:xmax].mean()

         polys.append(poly)
         weights.append(weight)

     results = gpd.GeoDataFrame(geometry=polys)
     results['weight'] = weights

     return results, bdiff


def blob_detector(image1, image2, sub_solar_azimuth, image_func=image_diff_sq,
                  subtractive=False,  min_sigma=.45, max_sigma=30, num_sigma=10,
                  threshold=.25, overlap=.5, log_scale=False, exclude_border=False,
                  n_neighbors=3, dist_upper_bound=5, angle_tolerance=3):
     """
     Blob based change detection.

     Creates a difference image and uses Laplacian of Gaussian (LoG) blob
     detection to find light / dark areas.  Creates a KDTree to find neighboring
     light / dark blobs, then filters based on colinearity of the light/dark pair
     with subsolar azimuth.

     Based on the method described in https://doi.org/10.1016/j.pss.2019.104733

     Parameters
     ----------

     image1 : GeoDataset
             Image representing the "before" state of the ROI, can be a 2D numpy array or plio GeoDataset

     image2 : GeoDataset
             Image representing the "after" state of the ROI, can be a 2D numpy array or plio GeoDataset


     sub_solar_azimuth : scalar or 2d np.array
                         Per-pixel subsolar azimuth or a single subsolar azimuth
                         value to be used for the entire image.

     image_func : callable
                  Function used to create a derived image from image1 and image2, which in turn is
                  the input for the feature extractor. The first two arguments are 2d numpy arrays, image1 and image2,
                  and must return a 2d numpy array. Default function returns a difference image.

                  Example func:

                  >>> from numpy import random
                  >>> image1, image2 = random.random((50,50)), random.random((50,50))
                  >>> def ratio(image1, image2):
                  >>>   # do stuff with image1 and image2
                  >>>   new_image = image1/image2
                  >>>   return new_image # must return a single variable, a 2D numpy array
                  >>> results = okbm_detector(image1, image2, image_func=ratio)

                  Or, alternatively:

                  >>> from numpy import random
                  >>> image1, image2 = random.random((50,50)), random.random((50,50))
                  >>> results = okbm_detector(image1, image2, image_func=lambda im1, im2: im1/im2)

     subtractive : Boolean
                   Find subtractive features instead of additive features.  In other
                   words, find locations in which a feature "used to be present"
                   but has since moved.

     min_sigma : scalar or sequence of scalars
                 The minimum standard deviation for Gaussian kernel. Keep this
                 low to detect smaller blobs. The standard deviations of the
                 Gaussian filter are given for each axis as a sequence, or as a
                 single number, in which case it is equal for all axes.


     max_sigma : scalar or sequence of scalars
                 The maximum standard deviation for Gaussian kernel. Keep this
                 high to detect larger blobs. The standard deviations of the
                 Gaussian filter are given for each axis as a sequence, or as a
                 single number, in which case it is equal for all axes.

     num_sigma : int
                 The number of intermediate values of standard deviations to
                 consider between min_sigma and max_sigma.

     threshold : float
                 The absolute lower bound for scale space maxima.
                 Local maxima smaller than thresh are ignored.
                 Reduce this to detect blobs with less intensities.

     overlap : float
               A value between 0 and 1. If the area of two blobs overlaps by a
               fraction greater than threshold, the smaller blob is eliminated.

     log_scale : bool
                 If set intermediate values of standard deviations are
                 interpolated using a logarithmic scale to the base 10. If not,
                 linear interpolation is used.

     exclude_border: tuple of ints, int, or False
                 If tuple of ints, the length of the tuple must match the input
                 array’s dimensionality. Each element of the tuple will exclude
                 peaks from within exclude_border-pixels of the border of the
                 image along that dimension. If nonzero int, exclude_border
                 excludes peaks from within exclude_border-pixels of the border
                 of the image. If zero or False, peaks are identified regardless
                 of their distance from the border.

     n_neighbors : int
                   Number of closest neighbors (blobs) to search.

     dist_upper_bound : int
                        The maximum distance between blobs to be considered
                        neighbors.

     angle_tolerance : int
                       The mismatch tolerance between the subsolar azimuth and
                       the angle between the direction vector w.r.t. the x axis.
                       For example, a subsolar azimuth of 85 degrees would
                       require an angle tolerance of 5 in order to consider
                       blobs with a 90 degree angle as candidates.

     Returns
     -------

     : pd.DataFrame
       A pandas dataframe containing a points of changed areas

     : np.ndarray
       A numpy array containing the image upon which the change detection
       algorithm operates, i.e. the image resulting from image_func.

     """

     def is_azimuth_colinear(pt1, pt2, subsolar_azimuth, tolerance, subtractive=False):
         """ Returns true if pt1, pt2, and subsolar azimuth are colinear within
             some tolerance.
         """
         x, y = (pt2[1]-pt1[1], pt2[0]-pt1[0])
         # Find angle of vector w.r.t. x axis
         angle = (atan2(y, x) * 180 / pi)%360
         # If finding subtractive changes, invert the angle.
         if subtractive:
             angle = (angle+180)%360
         return -tolerance <= subsolar_azimuth - angle <= tolerance

     if isinstance(image1, GeoDataset):
         image1 = image1.read_array()

     if isinstance(image2, GeoDataset):
         image2 = image2.read_array()

     if isinstance(image_func, str):
         try:
             image_func = func_map[image_func]
         except KeyError as e:
             raise Exception(f"{image_func} is not a valid method, available image functions: {func_map.keys()}")

     bdiff = image_func(image1,image2)
     bdiff = bytescale(bdiff)

     # Laplacian of Gaussian only finds light blobs on a dark image.  In order to
     #  find dark blobs on a light image, we invert.
     inv = bdiff.max()-bdiff

     # Laplacian of Gaussian of diff image (light on dark)
     blobs_log = blob_log(bdiff, min_sigma=min_sigma, max_sigma=max_sigma,
                          num_sigma=num_sigma, threshold=threshold, overlap=overlap,
                          log_scale=log_scale, exclude_border=exclude_border)
     # Laplacian of Gaussian on diff image (inverse -- dark on light)
     blobs_log_inv = blob_log(inv, min_sigma=min_sigma, max_sigma=max_sigma,
                              num_sigma=num_sigma, threshold=threshold, overlap=overlap,
                              log_scale=log_scale, exclude_border=exclude_border)

     # Compute radii in the 3rd column.  Radii are appx equal to sqrt2 * sigma
     blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
     blobs_log_inv[:, 2] = blobs_log_inv[:, 2] * sqrt(2)

     if not len(blobs_log) or not len(blobs_log_inv):
         raise Exception("No blobs detected")

     # Create a KDTree to facilitate nearest neighbor search
     tree = cKDTree(blobs_log)

     # Query the kdtree to find neighboring points
     _, idx_log = tree.query(blobs_log_inv, k=n_neighbors,
                                    distance_upper_bound=dist_upper_bound)

     # Points that have at least one neighbor within threshold distance.
     close_points = blobs_log_inv[[x[0] < len(blobs_log) for x in idx_log]]

     # Nearest neighbors
     neighbors = [blobs_log[j] for j in [i[i!=len(blobs_log)]for i in idx_log] if j.size > 0]

     polys = []
     for idx, pt1 in enumerate(close_points):
         for pt2 in neighbors[idx]:
             try:
                 azimuth = sub_solar_azimuth[int(pt1[0]), int(pt1[1])]
             except IndexError as e:
                 azimuth = sub_solar_azimuth
             if is_azimuth_colinear(pt1, pt2, azimuth, angle_tolerance, subtractive):
                 if subtractive:
                     polys.append(Point(pt1[1], pt1[0]))
                 else:
                     polys.append(Point(pt2[1], pt2[0]))

     changes = gpd.GeoDataFrame(geometry=polys)
     return changes, bdiff

def rv_detector(im1, im2, search_size, pattern_size=None, threshold=.999):
    """
    RV coefficient based change detection. This computes an RV coefficient on a sliding window 
    and correlates low scores below the input threshold to expected change.  
    
    **WARNING**: The time complexity for this is `1 + (search_size - pattern_size))^2` per overlapping pixel between im1 and im2. So larger the differemce between the search and pattern size, it causes compute time to increase exponentially. 

    Parameters
    ----------
    image1 : GeoDataset
        Image representing the "before" state of the ROI, can be a 2D numpy array or plio GeoDataset.

    image2 : GeoDataset
        Image representing the "after" state of the ROI, can be a 2D numpy array or plio GeoDataset.

    search_size : int
        The size of the search space surrounding each pixel.

    pattern_size : int
        The size of the window used to calculate the RV score.  This window slides through the search space.

    threshold : float
        The cutoff value for an RV value to be considered a change

    Returns 
    -------
    : pd.DataFrame
      A pandas dataframe containing a points of changed areas

    : np.ndarray
      A numpy array containing the RV values of each pixel.  Note that the array is
       padded by NaN values for 1/2 window size on each size
    """
    def get_window(arr, ulx, uly, size):
        return arr[ulx:ulx+size, uly:uly+size]

    if isinstance(im1, GeoDataset):
        im1 = im1.read_array()

    if isinstance(im2, GeoDataset):
        im2 = im2.read_array()

    if pattern_size is None:
        pattern_size = search_size

    if search_size < pattern_size:
        log.warning("Pattern size must be <= search size.  Setting pattern_size=search_size")
        search_size = pattern_size

    rv = np.empty(im1.shape)
    rv[:] = np.NaN
    for row in range(im1.shape[0] - search_size):
        for col in range(im1.shape[1] - search_size):
            best = -float("inf")
            # Windows are determined by ulx, uly, but rv corresponds to window's center
            center_x = col + (search_size//2)
            center_y = row + (search_size//2)
            for row_offset in range(search_size - pattern_size + 1):
                for col_offset in range(search_size - pattern_size + 1):
                    pattern_uly = row + row_offset
                    pattern_ulx = col + col_offset
                    best = max(best, abs(RVcoeff([get_window(im1, row, col, pattern_size), get_window(im2, pattern_uly, pattern_ulx, pattern_size)])[0,1]))
            rv[center_y, center_x] = best
    # Get x/y coordinates of points with correlation <= threshold
    filtered_rv = np.asarray(np.where(rv<=threshold)).T
    change_geometries = gpd.GeoDataFrame(geometry=[Point(x[1],x[0]) for x in filtered_rv])
    return change_geometries, rv

def compute_depression(input_dem, scale_factor=1, curvature_percentile=75, return_polygon=True, alpha=0.5):
    """
    Compute depressions and return a new image with largest depressions filled in.

    Parameters
    ----------

    input_dem : np.array, rd.rdarray
                2d array of elevation DNs, a DEM

    scale_factor : float
                   Value to scale the erotion of planform curvatures by

    curvature_percentile : float
                           what percentile of the curvature to keep, lower values
                           results in bigger blobs


    Returns
    -------
    dem : rd.rdarray
          Dem with filled depressions

    mask : np.array
           Change mask, true on pixels that have been changed


    """
    if isinstance(input_dem, np.ndarray):
        dem = rd.rdarray(input_dem.copy(), no_data=0)
    elif isinstance(input_dem, rd.rdarray):
        # take ownership of the reference
        dem = input_dem.copy()

    # create filled DEM
    demfilled = rd.FillDepressions(dem, epsilon=True, in_place=False, topology="D8")

    # Mask out filled areas
    mask = np.abs(dem-demfilled)
    thresh = np.percentile(mask, 95)
    mask[mask <= thresh] = False
    mask[mask > thresh] = True

    curvatures = rd.TerrainAttribute(dem, attrib='planform_curvature')
    curvatures = (curvatures - np.min(curvatures))/np.ptp(curvatures)
    curvatures[curvatures < np.percentile(curvatures, curvature_percentile)] = 0
    curvatures[mask.astype(bool)] = 0

    demfilled -= curvatures * scale_factor

    mask = (curvatures+mask).astype(bool)

    # Get 3rd nn distance
    coords = np.argwhere(mask)
    nbrs = NearestNeighbors(n_neighbors=3, algorithm='kd_tree').fit(coords)
    dists, _ = nbrs.kneighbors(coords)
    eps = np.percentile(dists, 95)

    # Cluster
    db = DBSCAN(eps=eps, min_samples=3).fit(coords)
    labels = db.labels_
    unique, counts = np.unique(labels, return_counts=True)

    # First count are outliers, ignore
    counts = counts[1:]
    unique = unique[1:]

    index = np.argwhere(counts == counts.max())
    group = unique[index][0][0]
    cluster = coords[labels == group]

    # mask out depression
    dmask = np.full(dem.shape, False)
    dmask[[*cluster.T]] = True

    dem[dmask] = 0
    demfilled[~dmask] = 0
    dem = dem+demfilled

    if return_polygon:
        concave_hull = cg.cg.alpha_shape(np.argwhere(dmask), alpha=alpha)
        return dem, concave_hull

    return dem, dmask


def generate_dem(alpha=1.0, size=800, scales=[160,80,32,16,8,4,2,1], scale_factor=5):
    """
    Produces a random DEM

    Parameters
    ----------

    alpha : float
            Controls height variation. Lower number makes a shallower and noisier DEM,
            higher values create smoother DEM with large peaks and valleys.
            Reccommended range = (0, 1.5]

    size : int
           size of DEM, output DEM is in the shape of (size, size)

    scale_factor : float
                   scalar to multiply the slope degridation by, higher values = more erotion.
                   Reccomended to increase proportionately with alpha
                   (higher alphas mean you might want higher scale_factor)

    Returns
    -------

    dem : np.array
          DEM array in the shape (size, size)

    """

    topo=np.zeros((2,2))+np.random.rand(2,2)*(200/(2.**alpha))

    for k in range(len(scales)):
        nn = size/scales[k]
        topo = scipy.misc.imresize(topo, (int(nn), int(nn)), "cubic", mode="F")
        topo = topo + np.random.rand(int(nn), int(nn))*(200/(nn**alpha))

    topo = rd.rdarray(topo, no_data=0)

    curvatures = rd.TerrainAttribute(topo, attrib='slope_riserun')
    curvatures = (curvatures - np.min(curvatures))/np.ptp(curvatures) * scale_factor
    return topo - curvatures


def hillshade(img, azi=255, alt=60, min_slope=20, max_slope=100, min_bright=0, grayscale=False):
    """
    hillshade a DEM, based on IDL code by Colin Dundas translated by Adam Paquette

    Parameters
    ----------

    img : np.array
          DEM to hillshade

    azi : float
          Sun azimuth in degrees

    alt: float
         base alt

    min_slope : float
                minimum slope value

    max_slope : float
                maximum slope value

    min_bright : float
                 minimum brightness

    grayscale : bool
                whether or not to produce grayscale image


    Returns
    -------

    dem : np.array
          hillshaded DEM

    """
    dem = np.array(np.flip(bytescale(img), axis = 0), dtype=int)
    emax = np.max(dem)
    emin = np.min(dem)

    indices = np.linspace(0, 255, 256) / 25.5

    red_array = [0,25,50,101,153,204,255,255,255,255,255,255]
    red_index = np.arange(len(red_array))
    red_vec = np.interp(indices, red_index, red_array)

    green_array = [42,101,153,204,237,255,255,238,204,153,102,42]
    green_index = np.arange(len(green_array))
    green_vec = np.interp(indices, green_index, green_array)

    blue_array = [255,255,255,255,255,255,204,153,101,50,25,0]
    blue_index = np.arange(len(blue_array))
    blue_vec = np.interp(indices, blue_index, blue_array)

    zz = (255.0/(emax-emin))*(dem-emin)
    zz = zz.astype(int)

    nx = (np.roll(dem, 1, axis = 1) - dem)
    ny = (np.roll(dem, 1, axis = 0) - dem)
    sz = np.shape(nx)
    nz = np.ones(sz)
    nl = np.sqrt(np.power(nx, 2.0) + np.power(ny, 2.0) + np.power(nz, 2.0))
    nx = nx/nl
    ny = ny/nl
    nz = nz/nl

    azi_rad = math.radians(azi)
    alt_rad = math.radians(alt)
    lx = math.sin(azi_rad)*math.cos(alt_rad)
    ly = math.cos(azi_rad)*math.cos(alt_rad)
    lz = math.sin(alt_rad)

    dprod = nx*lx + ny*ly + nz*lz

    if min_slope is not None:
        min_dprod = math.cos(math.radians(max_slope + 90.0 - alt))
    else:
        min_dprod = np.min(dprod)

    if max_slope is not None:
        max_dprod = math.cos(math.radians(90.0 - alt - max_slope))
    else:
        max_dprod = np.max(dprod)

    bright = ((dprod - min_dprod) + min_bright)/((max_dprod - min_dprod) + min_bright)

    if grayscale:
        arrforout = 255*bright
    else:
        qq = red_vec[zz]*bright
        rr = green_vec[zz]*bright
        ss = blue_vec[zz]*bright
        arrforout = np.dstack((qq, rr ,ss))

    arrforout = np.flip(arrforout.astype(int), axis = 0)
    arrfotout = bytescale(arrforout)
    arrforout.shape
    return arrforout


def generate_boulder(dem, radius, height=None, x=None, y=None):
    '''
    Generates a half dome with a given radius, at a given height,
    at a given x, y in 2D topology array

    Parameters
    ----------
    dem : 2d array
          2D array representing the topology of a surface where the value in the
          array is the height of the surface
    radius : float
             Radius of the half dome to generate
    height : float
             Height at which to generate the half dome. If none, the height is set
             to the value in the dem where the dome is being generated
    x : int
        X position in the array to place the center of the half dome. If none, a
        random position in the image is selected
    y : int
        Y position in the array to place the center of the half dome. If none, a
        random position in the image is selected
    Returns
    -------
    new_dem : 2D array
              Modified 2D array with the new "boulder" generated in it
    geom : Object
           Polgon object representing the generated boulder
    '''
    max_radii = 0
    points = []
    geom = None
    new_dem = np.copy(dem)
    x_range, y_range = dem.shape
    if not x:
        x = np.random.randint(0, x_range)
    if not y:
        y = np.random.randint(0, y_range)
    if not height:
        base_height = dem[y][x]
    else:
        base_height = height
    for x_coord in range(dem.shape[1]):
        for y_coord in range(dem.shape[0]):
            point_radius = math.sqrt(math.pow(x_coord - x, 2) + math.pow(y_coord - y, 2))
            if point_radius < radius:
                computed_height = ((1 - (math.sin(((math.pi*point_radius)/(2*radius)))) * radius) + radius) + base_height
                if computed_height >= dem[y_coord][x_coord]:
                    points.append((y_coord, x_coord))
                    new_dem[y_coord][x_coord] = computed_height
    if len(points) >= 3:
        geom = Polygon(points).convex_hull
    return new_dem, geom


def generate_boulder_field(dem, num_boulders, x_shift_min = 5, x_shift_max = 10,
                           y_shift_min = 5, y_shift_max = 10,
                           radius_min = 5, radius_max = 8,
                           height_min = None, height_max = None):
    '''
    Generates a number of boulders randomly across a given 2d array with
    specified aspects of all boulders placed around the image

    Parameters
    ----------

    dem : 2d array
          2D array representing the topology of a surface where the value in the
          array is the height of the surface

    num_boulders : int
                   Number of boulders to generate in the dem

    x_shift_min : int
                  Minimum amount of pixels to shift the center of the boulder in the x
                  direction

    x_shift_max : int
                  Maximum amount of pixels to shift the center of the boulder in the x
                  direction

    y_shift_min : int
                  Minimum amount of pixels to shift the center of the boulder in the y
                  direction

    y_shift_max : int
                  Maximum amount of pixels to shift the center of the boulder in the y
                  direction

    radius_min : int
                 Minimum possible radius when generating a boulder

    radius_max : int
                 Maximum possible radius when generating a boulder

    height_min : int
                 Minimum height that a boulder can be generated at

    height_max : int
                 Maximum height that a boulder can be generated at

    Returns
    -------

    before_dem : 2d array
                 Modified dem with boulders

    after_dem : 2d array
                Modified dem with the same boulders as the before_dem with boulders shifted
                in the x and y directions

    before_polys : list
                   A list of polygon objects representing the boulders

    after_polys : list
                  A list of polygon objects representing the shifted boulders
    '''
    before_dem = np.copy(dem)
    after_dem = np.copy(dem)
    before_polys = []
    after_polys = []
    x_shift = np.random.randint(x_shift_min, x_shift_max)
    y_shift = np.random.randint(y_shift_min, y_shift_max)
    for i in range(num_boulders):
        x_pos = np.random.randint(10, len(dem[0]))
        y_pos = np.random.randint(10, len(dem))
        radius = np.random.randint(radius_min, radius_max)
        if height_min == None or height_max == None:
            height = None
        else:
            height = np.random.randint(height_min, height_max)
        before_dem, before_geom = generate_boulder(before_dem, radius, height, x = x_pos, y = y_pos)
        after_dem, after_geom = generate_boulder(after_dem, radius, height, x = x_pos - x_shift, y = y_pos - y_shift)
        if before_geom:
            before_polys.append(before_geom)
        if after_geom:
            after_polys.append(after_geom)

    return before_dem, before_polys, after_dem, after_polys

def create_affine(x_scale, y_scale, x_shift, y_shift, rotation,
                  x_scale_delta, y_scale_delta, x_shift_delta, y_shift_delta, rotation_delta):

    """
    Generate an initial affine transformation matrix and generate a second
    transformation matrix based on deltas applied to the initial affine matrix

    x_scale : float
              Value to scale the image by in the x direction. Where 1 is no scale,
              > 1 is scaled up and < 1 is scaled down

    y_scale : float
              Value to scale the image by in the y direction. Where 1 is no scale,
              > 1 is scaled up and < 1 is scaled down

    x_shift : int
              Number of pixels to shift the image in the x direction

    y_shift : int
              Number of pixels to shift the image in the y direction

    rotation : float
               Degress of rotation in the initial affine transformation

    x_scale_delta : float
                    Delta to apply to the initial x_scale

    y_scale_delta : float
                    Delta to apply to the initial y_scale

    x_shift_delta : int
                    Pixel shift delta to apply to the initial x_shift

    y_shift_delta : int
                    Pixel shift delta to apply to the initial y_shift

    rotation_delta : float
                     Degree delta to apply to the initial rotation
    """
    cos_theta = math.cos(rotation)
    sin_theta = math.sin(rotation)
    scale_affine = [[x_scale, 0, 0], [0, y_scale, 0], [0, 0, 1]]
    shift_affine = [[1, 0, x_shift], [0, 1, y_shift], [0, 0, 1]]
    rotation_affine = [[cos_theta, sin_theta, 0], [-sin_theta, cos_theta, 0], [0, 0, 1]]

    before_affine = np.dot(scale_affine, shift_affine)
    before_affine = np.dot(before_affine, rotation_affine)

    cos_theta = math.cos(rotation + rotation_delta)
    sin_theta = math.sin(rotation + rotation_delta)
    scale_affine = [[x_scale + x_scale_delta, 0, 0], [0, y_scale + y_scale_delta, 0], [0, 0, 1]]
    shift_affine = [[1, 0, x_shift + x_shift_delta], [0, 1, y_shift + y_shift_delta], [0, 0, 1]]
    rotation_affine = [[cos_theta, sin_theta, 0], [-sin_theta, cos_theta, 0], [0, 0, 1]]

    after_affine = np.dot(scale_affine, shift_affine)
    after_affine = np.dot(after_affine, rotation_affine)

    return before_affine, after_affine
