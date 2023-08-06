import math
import numpy as np

def crossform(a):
    """
    Convert a three element vector into a 3 x 3 skew matrix as per
    Hartley and Zisserman pg. 581

    """
    return np.array([[0, a[2], -a[1]],
                     [-a[2], 0, a[0]],
                     [a[1], -a[0], 0]])

def normalize(a):
    """
    Normalize a set of coordinates such that the origin is
    translated to the center and then scaled isotropically such
    that the average distance from the origin is :math:`\\sqrt{2}`.

    Parameters
    ----------
    a : arraylike
        (n,2) array of x,y or (n,3) homogeneous coordinates

    Returns
    -------
    normalizer : ndarray
                 (3,3) transformation matrix
    """

    a = np.asarray(a)

    # Compute the normalization matrix
    centroid = a[:, :2].mean(axis=0)
    dist = np.sqrt(np.sum(((a[:, :2] - centroid)**2), axis=1))
    mean_dist = np.mean(dist)
    sq2 = math.sqrt(2)

    normalizer = np.array([[sq2 / mean_dist, 0, -sq2 / mean_dist * centroid[0]],
                          [0, sq2 / mean_dist,  -sq2 / mean_dist * centroid[1]],
                          [0, 0, 1]])

    return normalizer
