import logging

log = logging.getLogger(__name__)

try:
    import cudasift as cs
except:
    cs = None

def extract_features(array, nfeatures=None, **kwargs):
    """
    Use cudasift to extract features from an image

    See Also
    --------
    cudasift
    """
    if not nfeatures:
        nfeatures = int(max(array.shape) / 1.25)
    else:
        log.warning('NFeatures specified with the CudaSift implementation.  Please ensure the distribution of keypoints is what you expect.')

    siftdata = cs.PySiftData(nfeatures)
    cs.ExtractKeypoints(array, siftdata, **kwargs)
    keypoints, descriptors = siftdata.to_data_frame()
    keypoints = keypoints[['x', 'y', 'scale', 'sharpness', 'edgeness', 'orientation', 'score', 'ambiguity']]
    # Set the columns that have unfilled values to zero to avoid confusion
    keypoints['score'] = 0.0
    keypoints['ambiguity'] = 0.0

    return keypoints, descriptors
