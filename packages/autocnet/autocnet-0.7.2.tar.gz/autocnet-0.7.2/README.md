<p align="center">
  <img src="docs/AutoCNet_Logo.svg" alt="AutoCNet" width=200> 
</p>

# AutoCNet

[![Gitter Chat](https://badges.gitter.im/USGS-Astrogeology/autocnet.svg)](https://gitter.im/USGS-Astrogeology/autocnet?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Travis-CI](https://travis-ci.org/USGS-Astrogeology/autocnet.svg?branch=dev)](https://travis-ci.org/USGS-Astrogeology/autocnet)
[![Coveralls](https://coveralls.io/repos/USGS-Astrogeology/autocnet/badge.svg?branch=dev&service=github)](https://coveralls.io/github/USGS-Astrogeology/autocnet?branch=dev)
[![Docs](https://img.shields.io/badge/Docs-latest-green.svg)](https://usgs-astrogeology.github.io/autocnet/)

Automated sparse control network generation to support photogrammetric control of planetary image data.

## Documentation
Is available at: https://autocnet.readthedocs.io/en/dev/

## Installation Instructions
We suggest using Anaconda Python to install Autocnet within a virtual environment.  These steps will walk you through the process.

1. [Download](https://www.continuum.io/downloads) and install the Python 3.x Miniconda installer.  Respond ``Yes`` when prompted to add conda to your BASH profile.
2. Install ISIS.   Follow the 
   [instructions to install ISIS](https://github.com/USGS-Astrogeology/ISIS3#installation) in its own conda 
   environment. With that ISIS environment activated, determine the values for the ISIS environment 
   variables, with a command like this (may vary by your shell):

   `printenv | grep ISIS`

   Copy down the values of ISISROOT and ISISDATA.  Exit the ISIS environment. 
   
3. Install `mamba`. [`mamba`](https://github.com/mamba-org/mamba) is a fast cross platform package manager that has, in our experience, improved environment solving. The AutoCNet environment is complex and `mamba` is necessary to get a solve. To install `conda install -c conda-forge mamba`.
4. Install the autocnet environment using the supplied environment.yml file: `mamba env create -n autocnet -f environment.yml` 
5. Activate your environment: `conda activate autocnet`
6. Ensure ISISROOT and ISISDATA are set in the *autocnet* environment.  One way is to
   ```
   conda env config vars set ISISROOT=value-you-wrote-down-from-step-2
   conda env config vars set ISISDATA=value-you-wrote-down-from-step-2
   conda deactivate
   conda activate autocnet
   ```
   If you use Jupyter notebooks, you may need to do the following in a cell before importing 
   *autocnet* modules:
   ```
   import os
   os.environ["ISISROOT"] = "path-you-wrote-down-in-step-2"
   os.environ["ISISDATA"] = "path-you-wrote-down-in-step-2"
   ```
   
7. If you are going to develop autocnet or would like to use the bleeding edge version: `python setup.py develop`. Otherwise, `conda install -c usgs-astrogeology autocnet`

## How to run the test suite locally

1. Install Docker
2. Get the Postgresql with Postgis container and run it `docker run --name testdb -e POSTGRES_PASSOWRD='NotTheDefault' -e POSTGRES_USER='postgres' -p 5432:5432 -d mdillon/postgis`
3. Run the test suite: `pytest autocnet`

## Simple Network Examples:


### Setup a project
This first example imports the NetworkCandidateGraph object, which is used to orchestrate jobs, manage
a database session, and generally work with the images, points, and measures in
a control network.

```
from autocnet.graph.network import NetworkCandidateGraph

# Make an empty NCG
ncg = NetworkCandidateGraph()
# Load the configuration file
ncg.config_from_file('config/demo.yml')

# Populate the nodes/edges from the DB
ncg.from_database()
```

Line by line, this code first imports the network candidate graph, a collection
of nodes and edges that represents a potential control network.
`from autocnet.graph.network import NetworkCandidateGraph`.

Next, a network candidate graph is instantiated. `ncg =
NetworkCandidateGraph()`.

The network candidate graph (or NCG) is assocaited with a collection of
PostGreSQL database tables. We have to initiate the database connection via a
configuration file. An example configuration file is
provided in the config directory. `ncg.config_from_file('config/demo.yml')`

Once configured, the images need to be loaded and the graph of potential
overlapping images generated. We do this with `ncg.from_database()`.

At this point, you have a fully functioning autocnet project using an NCG. The
above snippet assumes that a prepopulated database already exists. Keep reading
to see how AutoCNet supports importing images from an existing image data
store.

### Import images from a data store containing image footprints
Autocnet does not assume where your image footprints are coming from for
initial setup. We do assume that you have a prepopulated database of image
footprints with a `geom` column. Otherwise, you could use any software to
create image footprints and populate the footprint database.

To initialize a project from a data store of image footprints we can do the
following:

```
# These lines are pulled from the example above
from autocnet.graph.network import NetworkCandidateGraph

ncg = NetworkCandidateGraph()
ncg.config_from_file('config/demo.yml')

# Create the connection 
source_db_config = {'username':'jay',
        'password':'abcde',
        'host':'localhost',
        'pgbouncer_port':5432,
        'name':'someothertable'}

# Subset the data store using a spatial query.
geom = 'LINESTRING(145 10, 145 10.25, 145.25 10.25, 145.25 10, 145 10)'
srid = 104971
outpath = '/scratch/some/path/for/data'
query = f"SELECT * FROM ctx WHERE ST_INTERSECTS(geom, ST_Polygon(ST_GeomFromText('{geom}'), {srid})) = TRUE"
ncg.add_from_remote_database(source_db_config, outpath, query_string=query)
```

Here we create an NCG as above. Then we define a new database connection with
the name of the database from which data will be extracted. `source_db_config =
{'username':'jay', 'password':'abcde', 'host':'localhost',
'pgbouncer_port':5432, 'name':'someothertable'}.

In this example, we want to use a spatial query to subset the data. We could
also use an attribute query or some combination. The only restriction is that
the quert string be valid SQL. `geom = 'LINESTRING(145 10, 145 10.25, 145.25
10.25, 145.25 10, 145 10)'`

The PostGIS query requires a valid SRID for the input geometry, so we
explicitly define that here. This is the SRID that the footprints are being
stored in inside of the data store. `srid = 104971` The srid here is a custom
srid that has been added to the data store spatial reference table; the id can
be any arbitrary number as long as it exists in the spatial reference table.

The `add_from_remote_database` call copies the image files in the source
database into a new directory. Here we define that directory. `outpath =
'/scratch/some/path/for/data'`. 

The query string is then constructed: `query = f"SELECT * FROM ctx WHERE
ST_INTERSECTS(geom, ST_Polygon(ST_GeomFromText('{geom}'), {srid})) = TRUE"` 

Finally, our database associated with the NCG is populated and the image data
are copied. `ncg.add_from_remote_database(source_db_config, outpath,
query_string=query)`

### Creating a NCG Using a Filelist
It is also possible to create a NCG and instantiate an associated database from a
list of ISIS cube files that have had footprints created (using *footprintinit*).

```
from autocnet.graph.network import NetworkCandidateGraph

ncg = NetworkCandidateGraph.from_filelist(myimages.lis)
```

This method can take a bit of time to run if the filelist is large as the data
are loaded into the database sequentially and then a spatial overlay operation is performed
to determine how individual images overlap with one another (using the footprints
generated from the a priori sensor pointing.)

This method performs the following actions:
- Load each image, as a row, into the Images table of the database. This includes attempting to extract a footprint from the image. The footprint can be read from an ISIS cube if footprint init has been run. Alternatively, experimental support exists for Community Sensor Model sensors developed by USGS.
- Use the database to compute the overlapping geometries between each of the images. For large data sets this can be a costly, one time operation. Limiting the number of geometries in image footprints can significantly improve performance. For each overlap, a row is added to the Overlay table. This table tracks the overlapping geometries and the images that intersect those geometries.
- Return a NewtorkCandidateGraph where each node represents and image and each edge represents a spatial overlap between said images.

### Operations on the NCG: Database Rows
After we have an NCG, we want to perform operations on the graph or on database
rows associated with the graph (e.g., the Points, Measures, or Image Overlaps).
We use a functional approach where an arbitray function can be applied to an
iterable associated with the graph. Here is a concrete example to help
illustrate what this looks like in practice.

```
from autocnet.graph.network import NetworkCandidateGraph

ncg = NetworkCandidateGraph()
ncg.config_from_file('/home/jlaura/autocnet_projects/demo.yml')
ncg.from_database()


# Define a function to govern the distribution of points in the North/South direction
def ns(x):
    from math import ceil
    return ceil(round(x,1)*8)

# Define a function to govern the distribution of points in the East/West direction
def ew(x):
    from math import ceil
    return ceil(round(x,1)*1)

# Pack a set of kwargs into a keyword that the called function is expecting
distribute_points_kwargs = {'nspts_func':ns, 'ewpts_func':ew}

# Apply a function on an iterable
njobs = ncg.apply('spatial.overlap.place_points_in_overlap', 
                  on='overlaps', 
                  cam_type='isis',
                  distribute_points_kwargs=distribute_points_kwargs)
```

Most of the above is either familiar boiler plate or a pair of helper functions
that we want to pass in. The interesting stuff is happening in:

```
njobs = ncg.apply('spatial.overlap.place_points_in_overlap',
                  on='overlaps',
                  cam_type='isis',
                  distribute_points_kwargs=distribute_points_kwargs)
```

Here, we are applying the `spatial.overlap.place_points_in_overlap` function on
an iterable (`overlaps`) with three keyword arguments (that the function is
expecting). The syntax for the function is module.submodule.function_name'.
Where the submodule can be repeated, e.g.,
module.submodule.subsubmodule.function_name.

It is possible to use a similar block to, for example, apply some subpixel
registration algorithm: 

`njobs = ncg.apply('matcher.subpixel.subpixel_register_point', on='points')`

or to apply a second pass subpixel alignment on only measures meeting some
criteria:

```
filters = {'ignore' : True}  # A database filter in the form column name : equality
njobs = ncg.apply('matcher.subpixel.subpixel_register_measure',
                  on='measures',
                  filters=filters)
```

### Operations on the NCG: Nodes and Edges
Just like the above example, it is possible to apply arbitrary functions to
nodes and edges in a NetworkCandidateGraph.

```
ncg = NetworkCandidateGraph()
ncg.config_from_file('/home/jlaura/autocnet_projects/demo.yml')
ncg.from_database()

njobs = ncg.apply('network_to_matches', on='edges')
```

After the standard boilerplate, the `network_to_matches` function is applied to
every edge in the graph. This function takes the points and measures from the
database and expands them so that every edge now has the pairwise
(measure-to-measure) information that is frequently quite useful when using
computer vision techniques. Note that the function to be called is not longer
being specificed with the import path (e.g.,
spatial.overlap.place_points_in_overla-). Note that the function to be called is no longer
being specificed with the import path (e.g., spatial.overlap.place_points_in_overlaps) because 
only Edge or NetworkEdge methods can be called on the autocnet Edge or NetworkEdge objects.
