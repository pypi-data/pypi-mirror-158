import pyproj
import numpy as np

def og2oc(lon, lat, semi_major, semi_minor):
    """
    Converts planetographic latitude to planetocentric latitude using pyproj pipeline.

    Parameters
    ----------
    lon : float or np.array
          longitude 0 to 360 domain (in degrees)

    lat : float or np.array
          planetographic latitude (in degrees)

    semi_major : float
                 Radius from the center of the body to the equator

    semi_minor : float
                 Radius from the center of the body to the pole

    Returns
    -------
    lon: float or np.array
         longitude (in degrees)

    lat: float or np.array
         planetocentric latitude (in degrees)
    """

    proj_str = f"""
    +proj=pipeline
    +step +proj=geoc +a={semi_major} +b={semi_minor} +lon_wrap=180 +xy_in=deg +xy_out=deg
    """
    og2oc = pyproj.transformer.Transformer.from_pipeline(proj_str)
    lon_oc, lat_oc = og2oc.transform(lon, lat, errcheck=True)
    return lon_oc, lat_oc

def oc2og(lon, lat, semi_major, semi_minor):
    """
    Converts planetocentric latitude to planetographic latitude using pyproj pipeline.

    Parameters
    ----------
    lon : float or np.array
          longitude 0 to 360 domain (in degrees)

    lat : float or np.array
          planetocentric latitude (in degrees)

    semi_major : float
                 Radius from the center of the body to the equator

    semi_minor : float
                 Radius from the center of the body to the pole

    Returns
    -------
    lon : float or np.array
          longitude (in degrees)

    lat : float or np.array
          planetographic latitude (in degrees)
    """

    proj_str = f"""
    +proj=pipeline
    +step +proj=geoc +a={semi_major} +b={semi_minor} +lon_wrap=180 +inv +xy_in=deg +xy_out=deg
    """
    oc2og = pyproj.transformer.Transformer.from_pipeline(proj_str)
    lon_og, lat_og = oc2og.transform(lon, lat, errcheck=True)

    return lon_og, lat_og

def reproject(record, semi_major, semi_minor, source_proj, dest_proj, **kwargs):
    """
    Thin wrapper around PyProj's Transform() function to transform 1 or more three-dimensional
    point from one coordinate system to another. If converting between Cartesian
    body-centered body-fixed (BCBF) coordinates and Longitude/Latitude/Altitude coordinates,
    the values input for semi-major and semi-minor axes determine whether latitudes are
    planetographic or planetocentric and determine the shape of the datum for altitudes.
    If semi_major == semi_minor, then latitudes are interpreted/created as planetocentric
    and altitudes are interpreted/created as referenced to a spherical datum.
    If semi_major != semi_minor, then latitudes are interpreted/created as planetographic
    and altitudes are interpreted/created as referenced to an ellipsoidal datum.

    Parameters
    ----------
    record : array of np.array
             Array containing the coordinates to reproject. 
             Formatted like [[x1, x2, ..., xn], [y1, y2, ..., yn], [z1, z2, ..., zn]]

    semi_major : float
                 Radius from the center of the body to the equater

    semi_minor : float
                 Radius from the pole to the center of mass

    source_proj : str
                         Pyproj string that defines a projection space ie. 'geocent'

    dest_proj : str
                      Pyproj string that defines a project space ie. 'latlon'

    Returns
    -------
    : np.arrays
      Transformed coordinates as y, x, z

    """
    source_pyproj = pyproj.Proj(proj=source_proj, a=semi_major, b=semi_minor, lon_wrap=180)
    dest_pyproj = pyproj.Proj(proj=dest_proj, a=semi_major, b=semi_minor, lon_wrap=180)

    y, x, z = pyproj.transform(source_pyproj, dest_pyproj, record[0], record[1], record[2], **kwargs)
    return y, x, z
