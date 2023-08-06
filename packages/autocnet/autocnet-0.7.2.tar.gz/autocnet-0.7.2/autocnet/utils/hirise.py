import os
from glob import glob
import textwrap
import geopandas as gpd

try:
    import kalasiris as isis
except Exception as exception:
    from autocnet.utils.utils import FailedImport
    isis = FailedImport(exception)
    
from subprocess import CalledProcessError

from plio.io.io_gdal import GeoDataset

from shapely import wkt
import numpy as np
import pvl
import logging

# setup logging file
log = logging.getLogger(__name__)

def segment_hirise(directory, offset=300):
    images = glob(os.path.join(directory, "*RED*.stitched.norm.cub"))
    for image in images:
        label = pvl.loads(isis.catlab(image).stdout)

        dims = label["IsisCube"]["Core"]["Dimensions"]
        nlines, nsamples = dims["Lines"], dims["Samples"]
        log.info("Lines, Samples: ", nlines, nsamples)

        starts = np.arange(1, nlines, nsamples)
        stops = np.append(np.arange(starts[1], nlines, nsamples), [nlines])

        starts[1:] -= offset
        stops[:-1] += offset

        segments = np.asarray([starts, stops]).T

        for i, seg in enumerate(segments):
            start, stop = seg
            output = os.path.splitext(image)[0] + f".{start}_{stop}" + ".cub"
            log.info(f"Writing: {output}")
            isis.crop(
                image,
                to=output,
                line=start,
                nlines=stop - start,
                sample=1,
                nsamples=nsamples
            )
            isis.footprintinit(output)

    return load_segments(directory)


def load_segments(directory):
    images = glob(os.path.join(directory, "*RED*.*_*.cub"))
    objs = [GeoDataset(image) for image in images]
    footprints = [o.footprint for o in objs]
    footprints = [wkt.loads(f.ExportToWkt()) for f in footprints]
    return gpd.GeoDataFrame(data=np.asarray([images, objs, footprints]).T, columns=["path", "image", "footprint"], geometry="footprint")


def ingest_hirise(directory):

    # This function is very brittle attempting to guess filenames in the
    # provided directory.  Much better to have this take a list of Path
    # objects and operate on them, and leave it up to the user (or some
    # convenience function) to figure out how to create that list.
    l = glob(os.path.join(directory, "*RED*.IMG")) + \
        glob(os.path.join(directory, "*RED*.img"))
    l = [os.path.splitext(i)[0] for i in l]
    log.info(l)
    cube_name = "_".join(os.path.splitext(os.path.basename(l[0]))[0].split("_")[:-2])

    log.info("Cube Name:", cube_name)

    try:
        log.info(f"Running hi2isis on {l}")
        for i,cube in enumerate(l):
            log.info(f"{i+1}/{len(l)}")
            isis.hi2isis(f'{cube}.IMG', to=f"{cube}.cub")
            log.info(f"finished {cube}")

        log.info(f"running spiceinit on {l}")
        for i,cube in enumerate(l):
            log.info(f"{i+1}/{len(l)}")
            isis.spiceinit(f'{cube}.cub')

        log.info(f"running hical on {l}")
        for i,cube in enumerate(l):
            log.info(f"{i}/{len(l)}")
            isis.hical(f'{cube}.cub', to=f'{cube}.cal.cub')

        cal_list_0 = sorted(glob(os.path.join(directory, "*0.cal*")))
        cal_list_1 = sorted(glob(os.path.join(directory, "*1.cal*")))
        log.info(f"Channel 0 images: {cal_list_0}")
        log.info(f"Channel 1 images: {cal_list_1}")

        for i,cubes in enumerate(zip(cal_list_0, cal_list_1)):
            log.info(f"{i+1}/{len(cal_list_0)}")
            c0, c1 = cubes
            output ="_".join(c0.split("_")[:-1])
            isis.histitch(from1=c0, from2=c1, to=f"{output}.stitched.cub")

        stitch_list = glob(os.path.join(directory, "*stitched*"))
        for cube in stitch_list:
            output = os.path.splitext(cube)[0] + ".norm.cub"
            isis.cubenorm(cube, to=output)

    except CalledProcessError as e:
        log.exception(
            textwrap.dedent(
                f"""\
                Had a subprocess error:
                {' '.join(e.cmd)}
                {e.stdout}
                {e.stderr}
                """
            )
        )
    return




