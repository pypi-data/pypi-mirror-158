from collections import defaultdict, OrderedDict
from contextlib import contextmanager
import itertools
import json
import math
import os
from shutil import copyfile
import threading
from time import gmtime, strftime, time, sleep
import logging
from itertools import combinations

import networkx as nx
import geopandas as gpd
import pandas as pd
import numpy as np
from redis import StrictRedis
import shapely
import scipy.special

import geoalchemy2
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql import func
import shapely.affinity
import shapely.geometry
import shapely.wkt as swkt
import shapely.ops

from plio.io.io_controlnetwork import to_isis, from_isis
from plio.io import io_hdf, io_json
from plio.utils import utils as io_utils
from plio.io.io_gdal import GeoDataset
from plio.io.isis_serial_number import generate_serial_number
from plio.io import io_controlnetwork as cnet

from .. import sql

from plurmy import Slurm

import autocnet
from autocnet.config_parser import parse_config
from autocnet.cg import cg
from autocnet.graph.asynchronous_funcs import watch_insert_queue, watch_update_queue
from autocnet.graph import markov_cluster
from autocnet.graph.edge import Edge, NetworkEdge
from autocnet.graph.node import Node, NetworkNode
from autocnet.io import network as io_network
from autocnet.io.db import controlnetwork as io_controlnetwork
from autocnet.io.db.model import (Images, Keypoints, Matches, Cameras, Points,
                                  Base, Overlay, Edges, Costs, Measures, CandidateGroundPoints,
                                  JsonEncoder, try_db_creation)
from autocnet.io.db.connection import new_connection, Parent
from autocnet.matcher import subpixel
from autocnet.matcher import cross_instrument_matcher as cim
from autocnet.vis.graph_view import plot_graph, cluster_plot
from autocnet.control import control
from autocnet.spatial.isis import point_info
from autocnet.spatial.surface import GdalDem, EllipsoidDem
from autocnet.transformation.spatial import reproject, og2oc

# set up the logging file
log = logging.getLogger(__name__)
#np.warnings.filterwarnings('ignore')

# The total number of pixels squared that can fit into the keys number of GB of RAM for SIFT.
MAXSIZE = {0: None,
           2: 6250,
           4: 8840,
           8: 12500,
           12: 15310}


class CandidateGraph(nx.Graph):
    """
    A NetworkX derived directed graph to store candidate overlap images.

    Attributes
    ----------

    node_counter : int
                   The number of nodes in the graph.
    node_name_map : dict
                    The mapping of image labels (i.e. file base names) to their
                    corresponding node indices

    clusters : dict
               of clusters with key as the cluster id and value as a
               list of node indices

    cn : object
         A control network object instantiated by calling generate_cnet.

    """

    node_factory = Node
    edge_factory = Edge
    measures_keys = ['point_id', 'image_index', 'keypoint_index',
                     'edge', 'match_idx', 'x', 'y', 'x_off', 'y_off', 'corr']
    # dtypes are usful for allowing merges, otherwise they default to object
    cnet_dtypes = {
        'match_idx' : int,
        'point_id' : int,
        'image_index' : int,
        'keypoint_index' : int
    }

    def __init__(self, *args, basepath=None, node_id_map=None, overlaps=False, **kwargs):
        super(CandidateGraph, self).__init__(*args, **kwargs)

        self.graph['creationdate'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.graph['modifieddate'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.graph['node_name_map'] = {}
        self.graph['node_counter'] = 1

        self._point_id = 0
        self._measure_id = 0
        self.measure_to_point = {}
        self.controlnetwork = pd.DataFrame(columns=self.measures_keys).astype(self.cnet_dtypes)
        self.masks = pd.DataFrame()

        for i, n in self.nodes(data=True):
            if basepath:
                image_path = os.path.join(basepath, i)
            else:
                image_path = i

            if node_id_map:
                node_id = node_id_map[image_path]
            else:
                node_id = self.graph['node_counter']
                self.graph['node_counter'] += 1

            n['data'] = self.node_factory(
                image_name=i, image_path=image_path, node_id=node_id)

            self.graph['node_name_map'][i] = node_id

        # Relabel the nodes in place to use integer node ids
        nx.relabel_nodes(self, self.graph['node_name_map'], copy=False)
        for s, d, e in self.edges(data=True):
            if s > d:
                s, d = d, s
            edge = self.edge_factory(
                self.nodes[s]['data'], self.nodes[d]['data'])
            # Unidrected graph - both representation point at the same data
            self.edges[s, d]['data'] = edge
            self.edges[d, s]['data'] = edge

        if overlaps:
            self.compute_overlaps()

    def __key(self):
        # TODO: This needs to be a real self identifying key
        return 'abcde'

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        # Check the nodes
        if sorted(self.nodes()) != sorted(other.nodes()):
            return False
        for node in self.nodes:
            if not self.nodes[node] == other.nodes[node]:
                return False
        if sorted(self.edges()) != sorted(other.edges()):
            return False
        for s, d, e in self.edges.data('data'):
            if s > d:
                s, d = d, s
            if not e == other.edges[(s, d)]['data']:
                return False
        return True

    def _order_adjacency(self):  # pragma: no cover
        self.adj = OrderedDict(sorted(self.adj.items()))

    @property
    def maxsize(self):
        if not hasattr(self, '_maxsize'):
            self._maxsize = MAXSIZE[0]
        return self._maxsize

    @maxsize.setter
    def maxsize(self, value):
        if not value in MAXSIZE.keys():
            raise KeyError('Value must be in {}'.format(
                ','.join(map(str, MAXSIZE.keys()))))
        else:
            self._maxsize = MAXSIZE[value]

    @property
    def unmatched_edges(self):
        """
        Returns a list of edges (source, destination) that do not have
        entries in the matches dataframe.
        """
        unmatched = []
        for s, d, e in self.edges(data='data'):
            if len(e.matches) == 0:
                unmatched.append((s,d))

        return unmatched

    @classmethod
    def from_filelist(cls, filelist, basepath=None):
        """
        Instantiate the class using a filelist as a python list.
        An adjacency structure is calculated using the lat/lon information in the
        input images. Currently only images with this information are supported.

        Parameters
        ----------
        filelist : list
                   A list containing the files (with full paths) to construct an adjacency graph from

        Returns
        -------
        : object
          A Network graph object
        """
        if isinstance(filelist, str):
            filelist = io_utils.file_to_list(filelist)
        # TODO: Reject unsupported file formats + work with more file formats
        if basepath:
            datasets = [GeoDataset(os.path.join(basepath, f))
                        for f in filelist]
        else:
            datasets = [GeoDataset(f) for f in filelist]

        # This is brute force for now, could swap to an RTree at some point.
        adjacency_dict = {}
        valid_datasets = []

        for i in datasets:
            adjacency_dict[i.file_name] = []

            fp = i.footprint
            if fp and fp.IsValid():
                valid_datasets.append(i)
            else:
                log.warning(
                    'Missing or invalid geospatial data for {}'.format(i.base_name))

        # Grab the footprints and test for intersection
        for i, j in itertools.permutations(valid_datasets, 2):
            i_fp = i.footprint
            j_fp = j.footprint

            try:
                if i_fp.Intersects(j_fp):
                    adjacency_dict[i.file_name].append(j.file_name)
                    adjacency_dict[j.file_name].append(i.file_name)
            except:
                log.warning(
                    'Failed to calculate intersection between {} and {}'.format(i, j))
        return cls.from_adjacency(adjacency_dict)

    @classmethod
    def from_adjacency(cls, input_adjacency, node_id_map=None, basepath=None, **kwargs):
        """
        Instantiate the class using an adjacency dict or file. The input must contain relative or
        absolute paths to image files.

        Parameters
        ----------
        input_adjacency : dict or str
                          An adjacency dictionary or the name of a file containing an adjacency dictionary.

        Returns
        -------
         : object
           A Network graph object

        Examples
        --------
        >>> from autocnet.examples import get_path
        >>> inputfile = get_path('adjacency.json')
        >>> candidate_graph = CandidateGraph.from_adjacency(inputfile)
        >>> sorted(candidate_graph.nodes())
        [0, 1, 2, 3, 4, 5]
        """
        if not isinstance(input_adjacency, dict):
            input_adjacency = io_json.read_json(input_adjacency)
        return cls(input_adjacency, basepath=basepath, node_id_map=node_id_map, **kwargs)

    @classmethod
    def from_save(cls, input_file):
        """
        Loads a saved autocnet control network from a given input file

        Parameters
        ----------

        input_file : str
                     The saved off autocnet control network to be loaded
        """
        return io_network.load(input_file)

    def _update_date(self):
        """
        Update the last modified date attribute.
        """
        self.graph['modifieddate'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def get_name(self, node_index):
        """
        Get the image name for the given node.

        Parameters
        ----------
        node_index : int
                     The index of the node.

        Returns
        -------
         : str
           The name of the image attached to the given node.


        """
        return self.nodes[node_index]['data']['image_name']

    def get_index(self, image_name):
        """
        Get the node index using the full or partial image name.

        Parameters
        ----------
        image_name : str
                     That is matched using a simple 'in' check to
                     node['image_name']

        Returns
        -------
        i : int
            The node index
        """

        for i, node in self.nodes(data='data'):
            if image_name in node['image_name']:
                return i

    def get_matches(self, clean_keys=[]):
        """
        Returns all matched features on all edges within the CandidateGraph

        Parameters
        ----------
        clean_keys : list
                     A list of keys which reference masks previous attached to 
                     the edge by outlier detection methods

        Returns
        -------
        matches : list
                  All matches from each edge in the graph as a dictionary

        See Also
        --------
        autocnet.spatial.fundamental_matrix.update_fundamental_mask: example of a function which returns an outlier mask
        autocnet.spatial.fundamental_matrix.compute_fundamental_matrix: example of a function which returns an outlier mask
        autocnet.spatial.homography.compute_homography: example of a function which returns an outlier mask
        """
        matches = []
        for s, d, e in self.edges_iter(data=True):
            match, _ = e.clean(clean_keys=clean_keys)
            match = match[['source_image', 'source_idx',
                           'destination_image', 'destination_idx']]
            skps = e.get_keypoints('source', index=match.source_idx)
            skps.columns = ['source_x', 'source_y']
            dkps = e.get_keypoints('destination', index=match.destination_idx)
            dkps.columns = ['destination_x', 'destination_y']
            match = match.join(skps, on='source_idx')
            match = match.join(dkps, on='destination_idx')

            # TODO: This is a bandaid fix, join is creating an insane amount of duplicate points
            match = match.drop_duplicates()
            matches.append(match)

        return matches

    def add_node(self, n=None, image_name="", adjacency=[], basepath="", **attr):
        """
        Adds an image node to the graph.

        Parameters
        ----------
        image_name : str
                     The file name of the node

        adjacency : str list
                    List of files names of adjacent images that correspond
                    to names in CandidateGraph.graph["node_name_map"]
        basepath : str
                    The base path to the node image file
        """
        new_node = None

        # If image name is provided, build the node from the image before
        # calling nx.add_node()
        if len(image_name) is not 0:
            if len(basepath) is not 0:
                image_path = os.path.join(basepath, image_name)
            else:
                image_path = image_name
            if not os.path.exists(image_path):
                log.warning("Cannot find {}".format(image_path))
                return
            n = self.graph["node_counter"]
            self.graph["node_counter"] += 1
            new_node = Node(image_name=image_name,
                            image_path=image_path,
                            node_id=n)
            self.graph["node_name_map"][new_node["image_name"]
                                        ] = new_node["node_id"]
            attr["data"] = new_node

        # Add the new node to the graph using networkx
        super(CandidateGraph, self).add_node(n, **attr)

        # Populate adjacency, if provided
        if new_node is not None and adjacency is not None:
            for adj_img in adjacency:
                if adj_img not in self.graph["node_name_map"].keys():
                    log.warning("{} not found in the graph".format(adj_img))
                    continue
                new_idx = new_node["node_id"]
                adj_idx = self.graph["node_name_map"][adj_img]
                self.add_edge(adj_img, new_node["image_name"])

    def add_edge(self, u, v, **attr):
        """
        Adds an edge with the given src and dst nodes to the graph

        Parameters
        ----------
        u : str
            The filename of the source image for the edge

        v : Node
            The filename of the destination image for the edge
        """
        if ("node_name_map" in self.graph.keys() and
            u in self.graph["node_name_map"].keys() and
                v in self.graph["node_name_map"].keys()):
            # Grab node ids & create edge obj
            s_id = self.graph["node_name_map"][u]
            d_id = self.graph["node_name_map"][v]
            new_edge = Edge(self.nodes[s_id]["data"], self.nodes[d_id]["data"])
            # Prepare data for networkx
            u = s_id
            v = d_id
            attr["data"] = new_edge
        # Add the new edge to the graph using networkx
        super(CandidateGraph, self).add_edge(u, v, **attr)

    def extract_features(self, band=1, *args, **kwargs):  # pragma: no cover
        """
        Extracts features from each image in the graph and uses the result to assign the
        node attributes for 'handle', 'image', 'keypoints', and 'descriptors'.
        """
        for i, node in self.nodes.data('data'):
            array = node.geodata.read_array(band=band)
            node.extract_features(array, *args, **kwargs),

    def extract_features_with_downsampling(self, downsample_amount=None, *args, **kwargs):  # pragma: no cover
        """
        Extract interest points from a downsampled array.  The array is downsampled
        by the downsample_amount keyword using the Lanconz downsample amount.  If the
        downsample keyword is not supplied, compute a downsampling constant as the
        total array size divided by the network maxsize attribute.

        Parameters
        ----------

        downsample_amount : int
                            The amount of downsampling to apply to the image
        """
        for node in self.nodes:
            if downsample_amount == None:
                total_size = node.geodata.raster_size[0] * \
                    node.geodata.raster_size[1]
                downsample_amount = math.ceil(total_size / self.maxsize**2)
            node.extract_features_with_downsampling(
                downsample_amount, *args, **kwargs)

    def extract_features_with_tiling(self, *args, **kwargs): #pragma: no cover
        """
        Extract interest points from a tiled array.

        See Also
        --------
        autocnet.graph.node.Node.extract_features_with_tiling
        """
        self.apply(Node.extract_features_with_tiling, args=args, **kwargs)

    def save_features(self, out_path):
        """
        Save the features (keypoints and descriptors) for the
        specified nodes.

        Parameters
        ----------
        out_path : str
                   Location of the output file.  If the file exists,
                   features are appended.  Otherwise, the file is created.
        """
        self.apply(Node.save_features, args=(out_path,), on='node')

    def load_features(self, in_path, nodes=[], nfeatures=None, **kwargs):
        """
        Load features (keypoints and descriptors) for the
        specified nodes.

        Parameters
        ----------
        in_path : str
                  Location of the input file.

        nodes : list
                of nodes to load features for.  If empty, load features
                for all nodes
        """
        self.apply(Node.load_features, args=(in_path, nfeatures), on='node', **kwargs)
        for n in self.nodes:
            if n['node_id'] not in nodes:
                continue
            else:
                n.load_features(in_path, **kwargs)

    def match(self, *args, **kwargs):
        """
        For all connected edges in the graph, apply feature matching

        See Also
        --------
        autocnet.graph.edge.Edge.match
        """
        self.apply_func_to_edges('match', *args, **kwargs)

    def decompose_and_match(self, *args, **kwargs):
        """
        For all edges in the graph, apply coupled decomposition followed by
        feature matching.

        See Also
        --------
        autocnet.graph.edge.Edge.decompose_and_match
        """
        self.apply_func_to_edges('decompose_and_match', *args, **kwargs)

    def estimate_mbrs(self, *args, **kwargs):
        """
        For each edge, estimate the overlap and compute a minimum bounding
        rectangle (mbr) in pixel space.

        See Also
        --------
        autocnet.graph.edge.Edge.compute_overlap
        """
        self.apply_func_to_edges('compute_overlap', *args, **kwargs)

    def compute_clusters(self, func=markov_cluster.mcl, *args, **kwargs):
        """
        Apply some graph clustering algorithm to compute a subset of the global
        graph.

        Parameters
        ----------
        func : object
               The clustering function to be applied.  Defaults to
               Markov Clustering Algorithm

        args : list
               of arguments to be passed through to the func

        kwargs : dict
                 of keyword arguments to be passed through to the func
        """
        _, self.clusters = func(self, *args, **kwargs)

    def compute_triangular_cycles(self):
        """
        Find all cycles of length 3.  This is similar
        to cycle_basis (networkX), but returns all cycles.
        As opposed to all basis cycles.

        Returns
        -------
        cycles : list
                 A list of cycles in the form [(a,b,c), (c,d,e)],
                 where letters indicate node identifiers

        Examples
        --------
        >>> g = CandidateGraph()
        >>> g.add_edges_from([(0,1), (0,2), (1,2), (0,3), (1,3), (2,3)])
        >>> sorted(g.compute_triangular_cycles())
        [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
        """
        cycles = []
        for s, d in self.edges:
            for n in self.nodes:
                if(s, n) in self.edges and (d, n) in self.edges:
                    cycles.append(tuple(sorted([s, d, n])))
        return set(cycles)

    def minimum_spanning_tree(self):
        """
        Calculates the minimum spanning tree of the graph

        Returns
        -------

         : DataFrame
           boolean mask for edges in the minimum spanning tree
        """

        mst = nx.minimum_spanning_tree(self)
        return self.create_edge_subgraph(mst.edges())

    def apply_func_to_edges(self, function, *args, **kwargs):
        """
        Iterates over edges using an optional mask and and applies the given function.
        If func is not an attribute of Edge, raises AttributeError

        Parameters
        ----------
        function : obj
                   function to be called on every edge

        args : iterable
               Some iterable of positional arguments for function.

        kwargs : dict
                 keyword args to pass into function.
        """
        return_lis = []
        if callable(function):
            function = function.__name__

        for s, d, edge in self.edges.data('data'):
            try:
                func = getattr(edge, function)
            except:
                raise AttributeError(function, ' is not an attribute of Edge')
            else:
                ret = func(*args, **kwargs)
                return_lis.append(ret)

        if any(return_lis):
            return return_lis

    def apply(self, function, on='edge', out=None, args=(), **kwargs):
        """
        Applys a function to every node or edge, returns collected return
        values. If applying a functions to nodes, then all ignored nodes
        will be skipped.

        TODO: Merge with apply_func_to_edges?

        Parameters
        ----------
        function : callable
                   Function to apply to graph. Should accept (id, data).

        on : string
             Whether to use nodes or edges. default is 'edge'.

        out : var
              Optionally put the output in a variable rather than returning it

        args : iterable
               Some iterable of positional arguments for function.

        kwargs : dict
                 keyword args to pass into function.
        """
        options = {
            'edge': self.edges_iter,
            'edges': self.edges_iter,
            'e': self.edges_iter,
            0: self.edges_iter,
            'node': self.nodes_iter,
            'nodes': self.nodes_iter,
            'n': self.nodes_iter,
            1: self.nodes_iter
        }

        if not callable(function):
            raise TypeError('{} is not callable.'.format(function))

        res = []
        obj = 1
        # We just want to the object, not the indices, so slice appropriately
        if options[on] == self.edges_iter:
            obj = 2
        for elem in options[on](data=True):
            if getattr(elem[obj], 'ignore', False):
                continue
            res.append(function(elem[obj], *args, **kwargs))

        if out:
            out = res
        else:
            return res

    def symmetry_checks(self):
        '''
        Apply a symmetry check to all edges in the graph
        '''
        self.apply_func_to_edges('symmetry_check')

    def ratio_checks(self, *args, **kwargs):
        '''
        Apply a ratio check to all edges in the graph

        Parameters
        ----------

        args : iterable
               Some iterable of positional arguments for the
               ratio_check function.

        kwargs : dict
                 keyword args to pass into the ratio_check function.

        See Also
        --------
        autocnet.matcher.cpu_outlier_detector.distance_ratio
        '''
        self.apply_func_to_edges('ratio_check', *args, **kwargs)

    def compute_overlaps(self, *args, **kwargs):
        '''
        Computes overlap MBRs for all edges


        Parameters
        ----------

        args : iterable
               Some iterable of positional arguments for the
               compute_overlap function.

        kwargs : dict
                 keyword args to pass into the compute_overlap function.

        See Also
        --------
        autocnet.graph.edge.Edge.compute_overlap
        '''
        self.apply_func_to_edges('compute_overlap', *args, **kwargs)

    def overlap_checks(self):
        '''
        Apply overlap check to all edges in the graph
        '''
        self.apply_func_to_edges('overlap_check')

    def compute_homographies(self, *args, **kwargs):
        '''
        Compute homographies for all edges using identical parameters

        Parameters
        ----------

        args : iterable
               Some iterable of positional arguments for the
               compute_homography function.

        kwargs : dict
                 keyword args to pass into the compute_homography function.

        See Also
        --------
        autocnet.graph.edge.Edge.compute_homography
        autocnet.transformation.homography.compute_homography
        '''
        self.apply_func_to_edges('compute_homography', *args, **kwargs)

    def compute_fundamental_matrices(self, *args, **kwargs):
        '''
        Compute fundmental matrices for all edges using identical parameters

        Parameters
        ----------

        args : iterable
               Some iterable of positional arguments for the
               compute_fundamental_matrix function.

        kwargs : dict
                 keyword args to pass into the compute_fundamental_matrix function.

        See Also
        --------
        autocnet.graph.edge.Edge.compute_fundamental_matrix
        autocnet.transformation.fundamental_matrix.compute_fundamental_matrix
        '''
        self.apply_func_to_edges('compute_fundamental_matrix', *args, **kwargs)

    def subpixel_register(self, *args, **kwargs):
        '''
        Compute subpixel offsets for all edges using identical parameters

        Parameters
        ----------

        args : iterable
               Some iterable of positional arguments for the
               subpixel_register function.

        kwargs : dict
                 keyword args to pass into the subpixel_register function.

        See Also
        --------
        autocnet.graph.edge.Edge.subpixel_register
        '''
        self.apply_func_to_edges('subpixel_register', *args, **kwargs)

    def suppress(self, *args, **kwargs):
        '''
        Apply a metric of point suppression to the graph

        Parameters
        ----------

        args : iterable
               Some iterable of positional arguments for the suppress function.

        kwargs : dict
                 keyword args to pass into the suppress function.

        See Also
        --------
        autocnet.matcher.cpu_outlier_detector.spatial_suppression
        '''
        self.apply_func_to_edges('suppress', *args, **kwargs)

    def overlap(self):
        '''
        Compute the percentage and area coverage of two images

        See Also
        --------
        autocnet.cg.cg.two_poly_overlap
        '''
        self.apply_func_to_edges('overlap')

    def to_filelist(self):
        """
        Generate a file list for the entire graph.

        Returns
        -------

        filelist : list
                   A list where each entry is a string containing the full path to an image in the graph.
        """
        filelist = []
        for i, node in self.nodes.data('data'):
            filelist.append(node['image_path'])
        return filelist

    def island_nodes(self):
        """
        Finds single nodes that are completely disconnected from the rest of the graph

        Returns
        -------
        : list
          A list of disconnected nodes, nodes of degree zero, island nodes, etc.
        """
        return nx.isolates(self)

    def connected_subgraphs(self):
        """
        Finds and returns a list of each connected subgraph of nodes. Each subgraph is a set.

        Returns
        -------

         : list
           A list of connected sub-graphs of nodes, with the largest sub-graph first. Each subgraph is a set.
        """
        return sorted(nx.connected_components(self), key=len, reverse=True)

    def serials(self):
        """
        Create a dictionary of ISIS3 compliant serial numbers for each
        node in the graph.

        Returns
        -------
        serials : dict
                  with key equal to the node id and value equal to
                  an ISIS3 compliant serial number or None
        """
        serials = {}
        for n, node in self.nodes.data('data'):
            serials[n] = generate_serial_number(node['image_path'])
        return serials

    @property
    def files(self):
        """
        Return a list of all full file PATHs in the CandidateGraph
        """
        return [node['image_path'] for _, node in self.nodes(data='data')]

    def save(self, filename):
        """
        Save the graph object to disk.
        Parameters
        ----------
        filename : str
                   The relative or absolute PATH where the network is saved
        """
        io_network.save(self, filename)

    def plot(self, ax=None, **kwargs):  # pragma: no cover
        """
        Plot the graph object

        Parameters
        ----------
        ax : object
             A MatPlotLib axes object.

        Returns
        -------
         : object
           A MatPlotLib axes object
        """
        return plot_graph(self, ax=ax, **kwargs)

    def plot_cluster(self, ax=None, **kwargs):  # pragma: no cover
        """
        Plot the graph based on the clusters generated by
        the markov clustering algorithm

        Parameters
        ----------
        ax : object
             A MatPlotLib axes object.

        Returns
        -------
        ax : object
             A MatPlotLib axes object.

        """
        return cluster_plot(self, ax, **kwargs)

    def create_node_subgraph(self, nodes):
        """
        Given a list of nodes, create a sub-graph and
        copy both the node and edge attributes to the subgraph.
        Changes to node/edge attributes are propagated back to the
        parent graph, while changes to the graph structure, i.e.,
        the topology, are not.

        Parameters
        ----------
        nodes : iterable
                An iterable (list, set, ndarray) of nodes to subset
                the graph

        Returns
        -------
        H : object
            A networkX graph object

        """
        return self.subgraph(nodes)

    def create_edge_subgraph(self, edges):
        """
        Create a subgraph using a list of edges.
        This is pulled directly from the networkx dev branch.

        Parameters
        ----------
        edges : list
                A list of edges in the form [(a,b), (c,d)] to retain
                in the subgraph

        Returns
        -------
        H : object
            A networkx subgraph object
        """
        return self.edge_subgraph(edges)

    def size(self, weight=None):
        """
        This replaces the built-in size method to properly
        support Python 3 rounding.

        Parameters
        ----------
        weight : string or None, optional (default=None)
           The edge attribute that holds the numerical value used
           as a weight.  If None, then each edge has weight 1.

        Returns
        -------
        nedges : int
            The number of edges or sum of edge weights in the graph.

        """
        if weight:
            return sum(e[weight] for s, d, e in self.edges.data('data'))
        else:
            return len(self.edges())

    def subgraph_from_matches(self):
        """
        Returns a sub-graph where all edges have matches.
        (i.e. images with no matches are removed)

        Returns
        -------
        : Object
          A networkX graph object
        """

        # get all edges that have matches
        matches = [(u, v) for u, v, edge in self.edges.data('data')
                   if not edge.matches.empty]

        return self.create_edge_subgraph(matches)

    def filter_nodes(self, func, *args, **kwargs):
        """
        Filters graph and returns a sub-graph from matches. Mimics
        python's filter() function

        Parameters
        ----------
        func : function which returns bool used to filter out nodes

        Returns
        -------
        : Object
          A networkX graph object

        """
        nodes = [node for i, node in self.nodes.data(
            'data') if func(node, *args, **kwargs)]
        return self.create_node_subgraph(nodes)

    def filter_edges(self, func, *args, **kwargs):
        """
        Filters graph and returns a sub-graph from matches. Mimics
        python's filter() function

        Parameters
        ----------
        func : function
               A function which returns bool used to filter out edges

        Returns
        -------
        : Object
          A networkX graph object
        """
        edges_to_remove = [(u, v) for u, v, edge in self.edges.data(
                            'data') if func(edge, *args, **kwargs)]
        subgraph = nx.create_empty_copy(self)
        subgraph.add_edges_from(edges_to_remove)
        return subgraph

    def compute_cliques(self, node_id=None):  # pragma: no cover
        """
        Computes all maximum complete subgraphs for the given graph.
        If a node_id is given, method will return only the complete subgraphs that
        contain that node

        Parameters
        ----------
        node_id : int
                  Integer value for a given node

        Returns
        -------
        : list
          A list of lists of node ids that make up maximum complete subgraphs of the given graph
        """
        if node_id is not None:
            return list(nx.cliques_containing_node(self, nodes=node_id))
        else:
            return list(nx.find_cliques(self))

    def compute_weight(self, clean_keys, **kwargs):  # pragma: no cover
        """
        Computes a voronoi weight for each edge in a given graph.
        Can function as is, but is slightly optimized for complete subgraphs.

        Parameters
        ----------
        kwargs : dict
                 keyword arguments that get passed to compute_voronoi

        clean_keys : list
                     Strings used to apply masks to omit correspondences
        """

        if not self.is_connected():
            log.warning(
                'The given graph is not complete and may yield garbage.')

        for s, d, edge in self.edges.data('edge'):
            source_node = edge.source
            overlap, _ = self.compute_intersection(
                source_node, clean_keys=clean_keys)

            matches, _ = edge.clean(clean_keys)
            kps = edge.get_keypoints(edge.source, index=matches['source_idx'])[
                ['x', 'y']]
            reproj_geom = source_node.reproject_geom(
                overlap.geometry.values[0].__geo_interface__['coordinates'][0])
            initial_mask = cg.geom_mask(kps, reproj_geom)

            if (len(kps[initial_mask]) <= 0):
                continue

            kps['geometry'] = kps.apply(
                lambda x: shapely.geometry.Point(x['x'], x['y']), axis=1)
            kps_mask = kps['geometry'][initial_mask].apply(
                lambda x: reproj_geom.contains(x))
            voronoi_df = cg.compute_voronoi(
                kps[initial_mask][kps_mask], reproj_geom, **kwargs)

            edge['weights']['voronoi'] = voronoi_df

    def compute_unique_fully_connected_components(self, size=2):
        """
        Compute a list of all cliques with size greater than size.

        Parameters
        ----------
        size : int
               Only cliques larger than size are returned.  Default 2.

        Returns
        -------
         : list
           of lists of node ids

        Examples
        --------
        >>> G = CandidateGraph()
        >>> G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('A', 'E'), ('A', 'F'), ('E', 'F') ])
        >>> res = G.compute_unique_fully_connected_components()
        >>> sorted(map(sorted,res))
        [['A', 'B', 'C'], ['A', 'E', 'F']]
        """
        return [i for i in nx.enumerate_all_cliques(self) if len(i) > size]

    def compute_fully_connected_components(self):
        """
        For a given graph, compute all of the fully connected subgraphs with
        3+ components.

        Returns
        -------
        fc : list
             of lists of node identifiers

        Examples
        --------
        >>> G = CandidateGraph()
        >>> G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('A', 'E'), ('A', 'F'), ('E', 'F') ])
        >>> fc = G.compute_fully_connected_components()
        >>> len(fc) #A, B, C, E, A  - D is omitted because it is a singular terminal node
        5
        >>> sorted(map(sorted,fc['A']))  # Sort inner and outer lists
        [['A', 'B', 'C'], ['A', 'E', 'F']]
        """
        fully_connected = self.compute_unique_fully_connected_components()
        fc = defaultdict(list)
        for i in fully_connected:
            for j in i:
                fc[j].append(tuple(i))
        return fc

    def compute_intersection(self, source, clean_keys=[]):
        """
        Computes the intercetion of all images in a graph
        based around a given source node

        Parameters
        ----------
        source: object or int
                     Either a networkx Node object or an integer

        clean_keys : list
                           Strings used to apply masks to omit correspondences

        Returns
        -------
        intersect_gdf : dataframe
                               A geopandas dataframe of intersections for all images
                               that overlap with the source node. Also includes the common
                               overlap for all images in the source node.
        """
        if type(source) is int:
            source = self.node[source]['data']
        # May want to use a try except block here, but what error to raise?
        source_poly = swkt.loads(
            source.geodata.footprint.GetGeometryRef(0).ExportToWkt())

        source_gdf = gpd.GeoDataFrame(
            {'geometry': [source_poly], 'source_node': [source['node_id']]})

        proj_gdf = gpd.GeoDataFrame(columns=['geometry', 'proj_node'])
        proj_poly_list = []
        proj_node_list = []
        # Begin iterating through the edges in the graph that include the source node
        for s, d, edge in self.edges.data('data'):
            if s == source['node_id']:
                proj_poly = swkt.loads(
                    edge.destination.geodata.footprint.GetGeometryRef(0).ExportToWkt())
                proj_poly_list.append(proj_poly)
                proj_node_list.append(d)

            elif d == source['node_id']:
                proj_poly = swkt.loads(
                    edge.source.geodata.footprint.GetGeometryRef(0).ExportToWkt())
                proj_poly_list.append(proj_poly)
                proj_node_list.append(s)

        proj_gdf = gpd.GeoDataFrame(
            {"geometry": proj_poly_list, "proj_node": proj_node_list})
        # Overlay all geometry and find the one geometry element that overlaps all of the images
        intersect_gdf = gpd.overlay(source_gdf, proj_gdf, how='intersection')
        if len(intersect_gdf) == 0:
            raise ValueError(
                'Node ' + str(source['node_id']) + ' does not overlap with any other images in the candidate graph.')
        overlaps_mask = intersect_gdf.geometry.apply(
            lambda x: proj_gdf.geometry.contains(shapely.affinity.scale(x, .9, .9)).all())
        overlaps_all = intersect_gdf[overlaps_mask]

        # If there is no intersection polygon that overlaps all of the images, union all of the intersection
        # polygons into one large polygon that does overlap all of the images
        if len(overlaps_all) <= 0:
            new_poly = shapely.ops.unary_union(intersect_gdf.geometry)
            overlaps_all = gpd.GeoDataFrame({'source_node': source['node_id'], 'proj_node': source['node_id'],
                                             'geometry': [new_poly]})

        return overlaps_all, intersect_gdf

    def is_complete(self):
        """
        Checks if the graph is a complete graph
        """
        nneighbors = len(self) - 1
        for n in self.nodes:
            if self.degree(n) != nneighbors:
                return False
        return True

    def footprints(self):
        """
        Gets the geodata footprint polygons of ever node in the graph and
        returns them in a GeoDataFrame

        Returns
        -------
        : GeoDataFrame
          GeoDataFrame containing all footprint polygons from each node in the
          graph
        """
        geoms = []
        names = []
        for i, node in self.nodes.data('data'):
            geoms.append(node.footprint)
            names.append(node['image_name'])

        return gpd.GeoDataFrame(names, geometry=geoms)

    def identify_potential_overlaps(self, **kwargs):
        """
        Identify those points that could have additional measures

        See Also
        --------
        autocnet.control.control.identify_potential_overlaps
        """
        cc = control.identify_potential_overlaps(
            self, self.controlnetwork, **kwargs)
        return cc

    def nodes_iter(self, data=False):
        """
        Iterates over all nodes in the CandidateGraph

        Parameters
        ----------
        data : bool
               Whether to include the data from the node or just the index

        Yields
        ------
        i : int
            Index of the Node

        n : Node
            Node object
        """
        for i, n in self.nodes.data('data'):
            if data:
                yield i, n
            else:
                yield i

    def edges_iter(self, data=False):
        """
        Iterates over all edges in the CandidateGraph

        Parameters
        ----------
        data : bool
               Whether to include the data from the edge or just the indices

        Yields
        ------
        s : int
            Index of source Node

        d : int
            Index of source Node

        e : Edge
            Edge object
        """
        for s, d, e in self.edges.data('data'):
            if data:
                yield s, d, e
            else:
                yield s, d

    def generate_control_network(self, clean_keys=[], mask=None):
        """
        Generates a fresh control network from edge matches.

        parameters
        ----------
        clean_keys : list
                     A list of clean keys, same that would be used to filter edges

        mask


        """
        def add_measure(lis, key, edge, match_idx, fields, point_id=None):
            """
            Create a new measure that is coincident to a given point.  This method does not
            create the point if is missing.  When a measure is added to the graph, an associated
            row is added to the measures dataframe.

            Parameters
            ----------
            key : hashable
                      Some hashable id.  In the case of an autocnet graph object the
                      id should be in the form (image_id, match_id)

            point_id : hashable
                       The point to link the node to.  This is most likely an integer, but
                       any hashable should work.
            """
            if key in self.measure_to_point.keys():
                return
            if point_id == None:
                point_id = self._point_id
            self.measure_to_point[key] = point_id
            # The node_id is a composite key (image_id, correspondence_id), so just grab the image
            image_id = int(key[0])
            match_id = int(key[1])
            lis.append([point_id, image_id, match_id, edge, int(match_idx), *fields, 0, 0, np.inf])
            self._measure_id += 1

        # TODO: get rid of these wack variables
        self.measure_to_point = {}
        self._measure_id = 0
        self.point_id = 0

        matches = self.get_matches(clean_keys)
        cnet_lis = []
        for match in matches:
            for row in match.to_records():
                edge = (row.source_image, row.destination_image)
                source_key = (row.source_image, row.destination_image, row.source_idx)
                source_fields = [row.source_x, row.source_y]
                destin_key = (row.destination_image, row.source_image, row.destination_idx)
                destin_fields = [row.destination_x, row.destination_y]
                if self.measure_to_point.get(source_key, None) is not None:
                    tempid = self.measure_to_point[source_key]
                    add_measure(cnet_lis, destin_key, edge, row[0],
                                    destin_fields, point_id=tempid)
                elif self.measure_to_point.get(destin_key, None) is not None:
                    tempid = self.measure_to_point[destin_key]
                    add_measure(cnet_lis, source_key, edge, row[0],
                                    source_fields, point_id=tempid)
                else:
                    add_measure(cnet_lis, source_key, edge, row[0],  source_fields)
                    add_measure(cnet_lis, destin_key, edge, row[0],  destin_fields)
                    self._point_id += 1

        self.controlnetwork = pd.DataFrame(cnet_lis, columns=self.measures_keys)
        self.controlnetwork.index.name = 'measure_id'

    def remove_measure(self, idx):
        """
        Removes a measure from the CandidateGraph based on a given index

        Parameters
        ----------
        idx : int
              Index of the measure to remove
        """
        self.controlnetwork = self.controlnetwork.drop(
            self.controlnetwork.index[idx])
        for r in idx:
            self.measure_to_point.pop(r, None)

    def validate_points(self):
        """
        Ensure that all control points currently in the nework are valid.
        Criteria for validity:
        * Singularity: A control point can have one and only one measure from any image
        Returns
        -------
        : pd.Series
        """

        def func(g):
            # One and only one measure constraint
            if g.image_index.duplicated().any():
                return True
            else: return False

        return self.controlnetwork.groupby('point_id').apply(func)

    def clean_singles(self):
        """
        Take the `controlnetwork` dataframe and return only those points with
        at least two measures.  This is automatically called before writing
        as functions such as subpixel matching can result in orphaned measures.
        """
        return self.controlnetwork.groupby('point_id').apply(lambda g: g if len(g) > 1 else None)

    def to_isis(self, outname, flistpath=None, target="Mars"):  # pragma: no cover
        """
        Write the control network out to the ISIS3 control network format.
        """
        df = self.controlnetwork

        serials = [generate_serial_number(self.nodes[id_]["data"]["image_path"]) for id_ in df["image_index"]]

        #create columns in the dataframe; zeros ensure plio (/protobuf) will
        #ignore unless populated with alternate values
        df['aprioriX'] = 0
        df['aprioriY'] = 0
        df['aprioriZ'] = 0
        df['adjustedX'] = 0
        df['adjustedY'] = 0
        df['adjustedZ'] = 0
        df['type'] = 3
        df['measureType'] = 2

        df["serialnumber"] = serials

        #only populate the new columns for ground points. Otherwise, isis will
        #recalculate the control point lat/lon from control measures which where
        #"massaged" by the phase and template matcher.
        for i, group in df.groupby('point_id'):
            zero_group = group.iloc[0]
            apriori_geom = np.array(point_info(self.nodes[zero_group.image_index]['data'].geodata.file_name, zero_group.x, zero_group.y, 'image')['BodyFixedCoordinate'].value) * 1000
            for j, row in group.iterrows():
                row['aprioriX'] = apriori_geom[0]
                row['aprioriY'] = apriori_geom[1]
                row['aprioriZ'] = apriori_geom[2]
                df.iloc[row.name] = row

        if flistpath is None:
            flistpath = os.path.splitext(outname)[0] + '.lis'

        df = df.rename(columns={'image_index':'image_id','point_id':'id', 'type' : 'pointType',
             'x':'sample', 'y':'line'})
        cnet.to_isis(df, outname, targetname=target)
        cnet.write_filelist(self.files, path=flistpath)


class NetworkCandidateGraph(CandidateGraph):
    node_factory = NetworkNode
    edge_factory = NetworkEdge

    def __init__(self, *args, **kwargs):
        super(NetworkCandidateGraph, self).__init__(*args, **kwargs)
        # Job metadata
        self.job_status = defaultdict(dict)

        # Set the parents of the nodes/edges and populate the database
        # if unpopulated.
        for i, d in self.nodes(data='data'):
            d.parent = self
        for s, d, e in self.edges(data='data'):
            e.parent = self

        self.apply_iterable_options = {
                'edge' : self.edges,
                'edges' : self.edges,
                'e' : self.edges,
                0 : self.edges,
                'node' : self.nodes,
                'nodes' : self.nodes,
                'n' : self.nodes,
                1 : self.nodes,
                'measures' : Measures,
                'measure' : Measures,
                'm' : Measures,
                2 : Measures,
                'points' : Points,
                'point' : Points,
                'p' : Points,
                3 : Points,
                'overlaps': Overlay,
                'overlap' : Overlay,
                'o' :Overlay,
                4: Overlay,
                'image': Images,
                'images': Images,
                'i': Images,
                5: Images,
                'candidategroundpoints' : CandidateGroundPoints,
                'candidategroundpoint' : CandidateGroundPoints,
                6: CandidateGroundPoints
            }

    def config_from_file(self, filepath, async_watchers=False):
        """
        A NetworkCandidateGraph uses a database. This method parses a config
        file to set up the connection. Additionally, this loads planetary
        information and settings for other operations the candidate graph
        can perform.

        Parameters
        ----------
        filepath : str
                   The path to the config file

        async_watchers : bool
                         If True the ncg will also spawn redis queue watching threads
                         that manage asynchronous database inserts. This is primarily
                         used for increased write performance.
        """
        # The YAML library will raise any parse errors
        self.config_from_dict(parse_config(filepath), async_watchers=async_watchers)

    def config_from_dict(self, config_dict, async_watchers=False):
        """
        A NetworkCandidateGraph uses a database. This method loads a config
        dict to set up the connection. Additionally, this loads planetary
        information and settings for other operations the candidate graph
        can perform.

        Parameters
        ----------
        filepath : str
                   The path to the config file

        async_watchers : bool
                         If True the ncg will also spawn redis queue watching threads
                         that manage asynchronous database inserts. This is primarily
                         used for increased write performance.
        """
        self.config = config_dict
        self.async_watchers = async_watchers
        # Setup REDIS
        self._setup_queues()

        # Setup the database
        self._setup_database()

        # Setup threaded queue watchers
        if self.async_watchers == True:
            self._setup_asynchronous_workers()

        # Setup the DEM
        # I dislike having the DEM on the NCG, but in the short term it
        # is the best solution I think. I don't want to pass the DEM around
        # for the sensor calls.
        self._setup_dem()

    @contextmanager
    def session_scope(self):
     """
     Provide a transactional scope around a series of operations.
     """
     session = self.Session()
     try:
         yield session
         session.commit()
     except:
         session.rollback()
         raise
     finally:
         session.close()

    def _setup_dem(self):
        spatial = self.config['spatial']
        semi_major = spatial.get('semimajor_rad')
        semi_minor = spatial.get('semiminor_rad')
        dem_type = spatial.get('dem_type')
        dem = spatial.get('dem', False)
        if dem:
            self.dem = GdalDem(dem, semi_major, semi_minor, dem_type)
        else:
            self.dem = EllipsoidDem(semi_major, semi_minor)

    @property
    def Session(self):
        return self._Session

    @Session.setter
    def Session(self, Session):
        self._Session = Session

    def _setup_database(self):
        db = self.config['database']
        # A non-linear timeout if the DB is spinning up or loaded with many connections.
        sleeptime = 2
        retries = 0
        while retries < 5:
            try:
                self.Session, self.engine = new_connection(self.config['database'])

                # Attempt to create the database (if it does not exist)
                try_db_creation(self.engine, self.config)
                break
            except:
                retries += 1
                sleep(retries ** sleeptime)

    def _setup_edges(self):
        with self.session_scope() as session:
            res = session.query(Edges).all()

            edges = []
            for e in res:
                s = e.source
                d = e.destination
                if s > d:
                    s,d = d,s
                edges.append((s,d))

            to_add = []
            for e in self.edges:
                s = e[0]
                d = e[1]
                if s > d:
                    s,d = d,s
                edgeid = (s,d)
                if edgeid not in edges:
                    to_add.append(Edges(source=edgeid[0],
                                        destination=edgeid[1],
                                        weights=json.dumps({})))
            session.add_all(to_add)
            session.commit()

    def _setup_queues(self):
        """
        Setup a 2 queue redis connection for pushing and pulling work/results
        """
        conf = self.config['redis']

        self.redis_queue = StrictRedis(host=conf['host'],
                                       port=conf['port'],
                                       db=0)
        self.processing_queue = conf['basename'] + ':processing'
        self.completed_queue = conf['basename'] + ':completed'
        self.working_queue = conf['basename'] + ':working'
        self.point_insert_queue = conf['basename'] + ':point_insert_queue'
        self.point_insert_counter = conf['basename'] + ':point_insert_counter'
        self.measure_update_queue = conf['basename'] + ':measure_update_queue'
        self.measure_update_counter = conf['basename'] + ':measure_update_counter'

        self.queue_names = [self.processing_queue, self.completed_queue, self.working_queue,
                           self.point_insert_queue, self.point_insert_counter,
                           self.measure_update_queue, self.measure_update_counter]

    def _setup_asynchronous_workers(self):

        # Default the counters to zero, unless they are already set from a run
        # where the NCG did not exit cleanly
        if self.redis_queue.get(self.point_insert_counter) is None:
            self.redis_queue.set(self.point_insert_counter, 0)

        if self.redis_queue.get(self.measure_update_counter) is None:
            self.redis_queue.set(self.measure_update_counter, 0)


        # Start the insert watching thread
        self.point_inserter_stop_event = threading.Event()
        self.point_inserter = threading.Thread(target=watch_insert_queue,
                                               args=(self.redis_queue,
                                                     self.point_insert_queue,
                                                     self.point_insert_counter,
                                                     self.engine,
                                                     self.point_inserter_stop_event))
        self.point_inserter.setDaemon(True)
        self.point_inserter.start()

        # Start the update watching thread
        self.measure_updater_stop_event = threading.Event()
        self.measure_updater = threading.Thread(target=watch_update_queue,
                                               args=(self.redis_queue,
                                                     self.measure_update_queue,
                                                     self.measure_update_counter,
                                                     self.engine,
                                                     self.measure_updater_stop_event))
        self.measure_updater.setDaemon(True)
        self.measure_updater.start()

    def clear_queues(self):
        """
        Delete all messages from the redis queue. This a convenience method.
        The `redis_queue` object is a redis-py StrictRedis object with API
        documented at: https://redis-py.readthedocs.io/en/latest/#redis.StrictRedis

        This also needs to restart any threaded watchers of the queues.
        """
        if self.async_watchers:
            self.point_inserter_stop_event.set()
            self.measure_updater_stop_event.set()

        for q in self.queue_names:
            self.redis_queue.delete(q)

        self._setup_queues()
        if self.async_watchers:
            self._setup_asynchronous_workers()


    def _execute_sql(self, sql):
        """
        Execute a raw SQL string in the database currently specified
        by the AutoCNet config file.

        Use this method with caution as you can easily do things like
        truncate a table.

        Parameters
        ----------
        sql : str
              The SQL string to be passed to the DB engine and executed.
        """
        conn = self.engine.connect()
        conn.execute(sql)
        conn.close()

    def _push_obj_messages(self, onobj, function, walltime, args, kwargs):
        """
        Push messages to the redis queue for objects e.g., Nodes and Edges
        """
        pipeline = self.redis_queue.pipeline()
        for job_counter, elem in enumerate(onobj.data('data')):
            if getattr(elem[-1], 'ignore', False):
                continue
            # Determine if we are working with an edge or a node
            if len(elem) > 2:
                id = (elem[2].source['node_id'],
                    elem[2].destination['node_id'])
                image_path = (elem[2].source['image_path'],
                            elem[2].destination['image_path'])
                along = 'edge'
            else:
                id = (elem[0])
                image_path = elem[1]['image_path']
                along = 'node'

            msg = {'id':id,
                   'along':along,
                    'func':function,
                    'args':args,
                    'kwargs':kwargs,
                    'walltime':walltime,
                    'image_path':image_path,
                    'param_step':1,
                    'config':self.config}

            pipeline.rpush(self.processing_queue, json.dumps(msg, cls=JsonEncoder))
        pipeline.execute()
        return job_counter + 1

    def _push_row_messages(self, query_obj, on, function, walltime, filters, query_string, args, kwargs):
        """
        Push messages to the redis queue for DB objects e.g., Points, Measures
        """
        if filters and query_string:
            log.warning('Use of filters and query_string are mutually exclusive.')

        with self.session_scope() as session:
            # Support either an SQL query string, or a simple dict based query
            if query_string:
                res = session.execute(query_string).fetchall()
            else:
                query = session.query(query_obj)

                # Now apply any filters that might be passed in.
                for attr, value in filters.items():
                    query = query.filter(getattr(query_obj, attr)==value)

                # Execute the query to get the rows to be processed
                res = query.order_by(query_obj.id).all()
            # Expunge so that the connection can be rapidly returned to the pool
            session.expunge_all()

        if len(res) == 0:
            raise ValueError('Query returned zero results.')
        pipeline = self.redis_queue.pipeline()
        for i, row in enumerate(res):
            msg = {'along':on,
                    'id':row.id,
                    'func':function,
                    'args':args,
                    'kwargs':kwargs,
                    'walltime':walltime}
            msg['config'] = self.config  # Hacky for now, just passs the whole config dict
            pipeline.rpush(self.processing_queue,
                                json.dumps(msg, cls=JsonEncoder))
            if i % 1000 == 0:
                # Redis can only accept 512MB of messages at a time. This ensures that the pipe
                # stays under the size limit.
                pipeline.execute()
                pipeline = self.redis_queue.pipeline()
        pipeline.execute()
        return len(res)

    def _push_iterable_message(self, iterable, function, walltime, args, kwargs):
        if not iterable:  # the list is empty...
            raise ValueError('iterable is not an iterable object, e.g., a list or set')

        pipeline = self.redis_queue.pipeline()
        for job_counter, item in enumerate(iterable):
            msg = {'along':item,
                    'func':function,
                    'args':args,
                    'kwargs':kwargs,
                    'walltime':walltime}
            msg['config'] = self.config
            pipeline.rpush(self.processing_queue,
                                   json.dumps(msg, cls=JsonEncoder))
        pipeline.execute()
        return job_counter + 1

    def apply(self,
            function,
            on='edge',
            args=(),
            walltime='01:00:00',
            jobname='AutoCNet',
            chunksize=1000,
            arraychunk=25,
            ntasks=1,
            filters={},
            query_string='',
            reapply=False,
            log_dir=None,
            queue=None,
            redis_queue='processing_queue',
            exclude=None,
            just_stage=False,
            **kwargs):
        """
        A mirror of the apply function from the standard CandidateGraph object. This implementation
        dispatches the job to the cluster as an independent operation instead of applying an arbitrary function
        locally.

        This methods returns the number of jobs submitted. The job status is then asynchronously
        updated as the jobs complete.

        Parameters
        ----------

        function : string / obj
                   The function to apply. This can be either the full, importable path from
                   this library or an arbitrary function that will be serialized. If the arbitrary
                   function requires imports external to this library, those imports must be made
                   within the function scope.

        on : str
             {'edge', 'edges', 'e', 0} for an edge
             {'node', 'nodes', 'n' 1} for a node
             {'measures', 'measure', 'm', '2'} for measures
             {'points', 'point', 'p', '3'} for points

        args : tuple
               Of additional arguments to pass to the apply function

        walltime : str
                   in the format Hour:Minute:Second, 00:00:00

        chunksize : int
                    The maximum number of jobs to submit per job array. Defaults to 1000.
                    This number may be have an actualy higher or lower limited based on
                    how the cluster has been configured.

        arraychunk : int
                     The number of concurrent jobs to run per job array. e.g. chunksize=100 and
                     arraychunk=25 gives the job array 1-100%25

        ntasks : int
                 The number of tasks, distributed across the cluster on some set of nodes to be run.
                 When running apply with ntasks, set ntasks to some integer greater then 1. arraychunk and
                 chunksize arguments will then be ignored. In this mode, a number of non-communicating
                 CPUs equal to ntasks are allocated and these CPUs run jobs. Changing from arrays to ntasks
                 also likely requires increasing the walltime of the job significantly since less jobs
                 will need to run for a longer duration.

        filters : dict
                  Of simple filters to apply on database rows where the key is the attribute and
                  the value used to check equivalency (e.g., attribute == value).
                  This is usable only when applying to measures, points, or overlays.
                  Filters can not be used with a query_string. Filters are included as a convenience
                  and are really only usable for simple equivalency checks.

        query_string : str
                       A SQL query to be applied to the iterable.
                       This is usable only when applying to measures, points, or overlays.
                       The query_string can not be used with a filter and is appropriate for
                       any queries.
        reapply : bool
                  Flag indicating whether you want to resubmit jobs that are still on the queue
                  after an initial apply due to an slurm launching errors.
        log_dir: str
                 absolute path of directory used to store the jobs logs, defaults to location
                 indicated in the configuration file.

        kwargs : dict
                 Of keyword arguments passed to the function being applied

        queue : str
                The cluster processing queue to submit jobs to. If None (default),
                use the cluster processing queue from the config file.

        redis_queue : str
                      The redis queue to push messages to that are then pulled by the
                      cluster job this call launches. Options are: 'processing_queue' (default)
                      or 'working_queue'

        just_stage : bool
                     If True, push messages to the redis queue for processing, but do not
                     submit a slurm/sbatch job to the cluster. This is useful when one process
                     is being used to orchestrate queue population and another process is being
                     used to process the messages. Default: False.

        Returns
        -------
        job_str : str
                  The string job that is submitted to the job scheduler

        Examples
        --------
        Apply a function to the overlay table omitting those overlay rows that already have
        points within them and have an area less than a given threshold.

        >>> query_string = 'SELECT overlay.id FROM overlay LEFT JOIN\
            points ON ST_INTERSECTS(overlay.geom, points.geom) WHERE\
                pointGT_AREA(overlay.geom) >= 0.0001;'
        >>> njobs = ncg.apply('spatial.overlap.place_points_in_overlap', on='overlaps', query_string=query_string)

        Apply a function to the overlay table and pass keyword arguments (kwargs) to the function.

        >>> def ns(x):
                from math import ceil
                return ceil(round(x,1)*8)
        >>> def ew(x):
                from math import ceil
                return ceil(round(x,1)*2)
        >>> distribute_points_kwargs = {'nspts_func':ns, 'ewpts_func':ew, 'method':'classic'}
        >>> njobs = ncg.apply('spatial.overlap.place_points_in_overlap',\
            on='overlaps', distribute_points_kwargs=distribute_points_kwargs)
        """
        if log_dir is None:
            log_dir=self.config['cluster']['cluster_log_dir']

        job_counter = self.queue_length

        # TODO: reapply uses the queue name and reapplies on that queue.

        if not reapply:
            # Determine which obj will be called
            if isinstance(on, str):
                onobj = self.apply_iterable_options[on]
            elif isinstance(on, (list, np.ndarray)):
                onobj = on

            # This method support arbitrary functions. The name needs to be a string for the log name.
            if not isinstance(function, (str, bytes)):
                function_name = function.__name__
            else:
                function_name = function

            # Dispatch to either the database object message generator or the autocnet object message generator
            if isinstance(onobj, DeclarativeMeta):
                job_counter = self._push_row_messages(onobj, on, function, walltime, filters, query_string, args, kwargs)
            elif isinstance(onobj, (list, np.ndarray)):
                job_counter = self._push_iterable_message(onobj, function, walltime, args, kwargs)
            elif isinstance(onobj, (nx.classes.reportviews.EdgeView, nx.classes.reportviews.NodeView)):
                job_counter = self._push_obj_messages(onobj, function, walltime, args, kwargs)
            else:
                raise TypeError('The type of the `on` argument is not understood. Must be a database model, iterable, Node or Edge.')

        # Submit the jobs
        rconf = self.config['redis']
        rhost = rconf['host']
        rport = rconf['port']
        try:
            processing_queue = getattr(self, redis_queue)
        except AttributeError:
            log.exception(f'Unable to find attribute {redis_queue} on this object. Valid queue names are: "processing_queue" and "working_queue".')

        env = self.config['env']
        condaenv = env['conda']
        isisroot = env['ISISROOT']
        isisdata = env['ISISDATA']

        isissetup = f'export ISISROOT={isisroot} && export ISISDATA={isisdata}'
        condasetup = f'conda activate {condaenv}'
        job = f'acn_submit -r={rhost} -p={rport} {processing_queue} {self.working_queue}'
        if ntasks > 1:
            job += ' --queue'  # Use queue mode where jobs run until the queue is empty
        command = f'{condasetup} && {isissetup} && srun {job}'

        # The user does not want to submit the job. Only stage the messages.
        if just_stage:
            return command

        if queue == None:
            queue = self.config['cluster']['queue']

        submitter = Slurm(command,
                     job_name=jobname,
                     mem_per_cpu=self.config['cluster']['processing_memory'],
                     time=walltime,
                     partition=queue,
                     ntasks=ntasks,
                     output=log_dir+f'/autocnet.{function}-%j')

        # Submit the jobs to the cluster
        if ntasks > 1:
            job_str = submitter.submit(exclude=exclude)
        else:
            job_str = submitter.submit(array='1-{}%{}'.format(job_counter,arraychunk),
                                    chunksize=chunksize,
                                    exclude=exclude)
        return job_str

    def generic_callback(self, msg):
        """
        This method manages the responses from the jobs and updates
        the status on this object. The msg is in a standard, parseable
        format.
        """
        id = msg['id']
        if isinstance(id, (int, float, str)):
            # Working with a node
            obj = self.nodes[id]['data']
        else:
            obj = self.edges[id]['data']
            # Working with an edge

        func = msg['func']
        obj.job_status[func]['success'] = msg['success']

        # If the job was successful, no need to resubmit
        if msg['success'] == True:
            return

    def to_isis(self,
                path,
                flistpath=None,
                latsigma=10,
                lonsigma=10,
                radsigma=15,
                **db_kwargs):
        """
        Write a NetworkCandidateGraph to an ISIS control network

        Parameters
        ----------
        path : str
               Outpath to write the control network

        flishpath : str
                    Outpath to write the associated file list. If None (default),
                    the file list is written alongside the control network

        latsigma : int/float
               The estimated sigma (error) in the latitude direction

        lonsigma : int/float
                The estimated sigma (error) in the longitude direction

        radsigma : int/float
                The estimated sigma (error) in the radius direction

        radius : int/float
                The body semimajor radius

        db_kwargs : dict
                    Kwargs that are passed to the io.db.controlnetwork.db_to_df function

        Returns
        -------
        df : pd.DataFrame
             The pandas dataframe that is passed to plio to generate the control network.

        fpaths : list
                 of paths to the images being included in the control network

        """
        # Read the cnet from the db
        df = io_controlnetwork.db_to_df(self.engine, **db_kwargs)

        # Add the covariance matrices to ground measures
        df = control.compute_covariance(df,
                                        latsigma,
                                        lonsigma,
                                        radsigma,
                                        self.config['spatial']['semimajor_rad'])

        if flistpath is None:
            flistpath = os.path.splitext(path)[0] + '.lis'
        target = self.config['spatial'].get('target', None)

        ids = df['imageid'].unique()
        fpaths = [self.nodes[i]['data']['image_path'] for i in ids]
        for f in self.files:
            if f not in fpaths:
                log.warning(f'{f} in candidate graph but not in output network.')

        # Remap the df columns back to ISIS
        df.rename(columns={'pointtype':'pointType',
                           'measuretype':'measureType'},
                           inplace=True)
        cnet.to_isis(df, path, targetname=target)
        cnet.write_filelist(fpaths, path=flistpath)

        # Even though this method writes, having a non-None return
        # let's a user work with the data that is passed to plio
        return df, fpaths

    def update_from_jigsaw(self, path, pointid_func=lambda x: int(x.split('_')[-1])):
        """
        Updates the measures table in the database with data from
        a jigsaw bundle adjust

        Parameters
        ----------
        path : str
               Full path to a bundle adjusted isis control network

        pointid_func : callable
                       A function that is used to convert from the id in the ISIS network
                       back into the pointid that autocnet uses as the primary key. The
                       default takes a string, splits it on underscores and takes the final element(s).
                       For example, autocnet_14 becomes 14.
        """
        isis_network = cnet.from_isis(path)
        io_controlnetwork.update_from_jigsaw(isis_network,
                                             self.measures,
                                             self.engine,
                                             pointid_func=pointid_func)

    @classmethod
    def from_filelist(cls, filelist, config, clear_db=False):
        """
        Parse a filelist to add nodes to the database. Using the
        information in the database, then instantiate a complete,
        NCG.

        Parameters
        ----------
        filelist : list, str
                   If a list, this is a list of paths. If a str, this is
                   a path to a file containing a list of image paths
                   that is newline ("\\n") delimited.
        config : dict, str
                 configuration information; either a path to a yaml
                 file or a dictionary.

        clear_db : boolean
                   truncates all tables in the active database.

        Returns
        -------
        ncg : object
              A network candidate graph object

        See Also
        --------
        config_from_dict: config documentation
        """
        obj = cls()

        if isinstance(config, str):
            config = parse_config(config)
        obj.config_from_dict(config)

        if clear_db:
            obj.clear_db()

        obj.add_from_filelist(filelist, clear_db=clear_db)

        return obj

    def add_from_filelist(self, filelist, clear_db=False):
        """
        Parse a filelist to add nodes to the database.

        Parameters
        ----------
        filelist : list, str
                   If a list, this is a list of paths. If a str, this is
                   a path to a file containing a list of image paths
                   that is newline ("\\n") delimited.
        clear_db : boolean
                   truncates all tables in the active database.
        """
        if isinstance(filelist, list):
            pass
        elif os.path.exists(filelist):
            filelist = io_utils.file_to_list(filelist)
        else:
           log.warning('Unable to parse the passed filelist')

        if clear_db:
            self.clear_db()

        total=len(filelist)
        for cnt, f in enumerate(filelist):
            # Create the nodes in the graph. Really, this is creating the
            # images in the DB
            log.info('loading {} of {}'.format(cnt+1, total))
            self.add_image(f)

        self.from_database()
        # Execute the computation to compute overlapping geometries
        self._execute_sql(sql.compute_overlaps_sql)

    def add_image(self, img_path):
        """
        Upload a single image to NetworkCandidateGraph associated DB.

        Parameters
        ----------
        img_path : str
                  absolute path to image

        Returns
        -------
        node.id : int
                  The id of the newly added node.
        """
        image_name = os.path.basename(img_path)
        node = NetworkNode(image_path=img_path, image_name=image_name)
        node.parent = self
        node.populate_db()
        return node['node_id']

    def copy_images(self, newdir):
        """
        Copy images from a given directory into a new directory and
        update the 'path' column in the Images table.

        Parameters
        ----------
        newdir : str
                 The full output PATH where the images are to be copied to.
        """
        if not os.path.exists(newdir):
            os.makedirs(newdir)

        with self.session_scope() as session:
            images = session.query(Images).all()
            for obj in images:
                oldpath = obj.path
                filename = os.path.basename(oldpath)
                obj.path = os.path.join(newdir, filename)
                if oldpath != obj.path:
                    # Copy the files
                    copyfile(oldpath, obj.path)
                    session.commit()
                else:
                    continue

    def add_from_remote_database(self, source_db_config, path=None,  query_string=sql.select_ten_pub_image):
        """
        This is a constructor that takes an existing database containing images and sensors,
        copies the selected rows into the project specified in the autocnet_config variable,
        and instantiates a new NetworkCandidateGraph object. This method is
        similar to the `from_database` method. The main difference is that this
        method assumes that the image and sensor rows are prepopulated in an external db
        and simply copies those entires into the currently speficied project.

        Currently, this method does NOT check for duplicate serial numbers during the
        bulk add. Therefore multiple runs of this method on the same database will fail.

        Parameters
        ----------
        source_db_config : dict
                           In the form: {'username':'somename',
                                         'password':'somepassword',
                                         'host':'somehost',
                                         'pgbouncer_port':6543,
                                         'name':'somename'}

        path : str
               The PATH to which images in the database specified in the config
               will be copied to. This method duplicates the data and copies it
               to a user defined PATH to avoid issues with updating image ephemeris
               across projects. The default PATH is (None), meaning the data will
               not be copied.

        query_string : str
                       An optional string to select a subset of the images in the
                       database specified in the config.

        Examples
        --------
        >>> ncg = NetworkCandidateGraph()
        >>> ncg.config_from_dict(new_config)
        >>> source_db_config = {'username':'jay',
        'password':'abcde',
        'host':'autocnet.wr.usgs.gov',
        'pgbouncer_port':5432,
        'name':'mars'}
        >>> geom = 'LINESTRING(145 10, 145 10.25, 145.25 10.25, 145.25 10, 145 10)'
        >>> srid = 104971
        >>> outpath = '/scratch/jlaura/fromdb'
        >>> query = f"SELECT * FROM ctx WHERE ST_INTERSECTS(geom, ST_Polygon(ST_GeomFromText('{geom}'), {srid})) = TRUE"
        >>> ncg.add_from_remote_database(source_db_config, outpath, query_string=query)
        """

        sourceSession, _ = new_connection(source_db_config)
        sourcesession = sourceSession()

        sourceimages = sourcesession.execute(query_string).fetchall()
        # Change for SQLAlchemy >= 1.4, results are now row objects

        sourceimages = [sourceimage._asdict() for sourceimage in sourceimages]
        with self.session_scope() as destinationsession:
            destinationsession.execute(Images.__table__.insert(), sourceimages)

            # Get the camera objects to manually join. Keeps the caller from
            # having to remember to bring cameras as well.
            #ids = [i[0] for i in sourceimages]
            #cameras = sourcesession.query(Cameras).filter(Cameras.image_id.in_(ids)).all()
            #for c in cameras:
            #    destinationsession.merge(c)

        sourcesession.close()

        # Create the graph, copy the images, and compute the overlaps
        if path:
            self.copy_images(path)
        self.from_database()
        self._execute_sql(sql.compute_overlaps_sql)

    def from_database(self, query_string=sql.select_pub_image):
        """
        This is a constructor that takes the results from an arbitrary query string,
        uses those as a subquery into a standard polygon overlap query and
        returns a NetworkCandidateGraph object.  By default, an images
        in the Image table will be used in the outer query.

        Parameters
        ----------
        query_string : str
                       A valid SQL select statement that targets the Images table

        Examples
        --------
        Here, we provide usage examples for a few, potentially common use cases.

        Spatial Query:
        This example selects those images that intersect a given bounding polygon.  The polygon is
        specified as a Well Known Text LINESTRING with the first and last points being the same.
        The query says, select the geom (the bounding polygons in the database) that
        intersect the user provided polygon (the LINESTRING) in the given spatial reference system
        (SRID), 104971, for Mars. ::

            SELECT * FROM Images WHERE ST_INTERSECTS(geom, ST_Polygon(ST_GeomFromText('LINESTRING(159 10, 159 11, 160 11, 160 10, 159 10)'),104971)) = TRUE

        Select from a specific orbit:
        This example selects those images that are from a particular orbit. In this case,
        the regex string pulls all P##_* orbits and creates a graph from them. This method
        does not guarantee that the graph is fully connected. ::

          SELECT * FROM Images WHERE (split_part(path, '/', 6) ~ 'P[0-9]+_.+') = True
        """

        composite_query = sql.from_database_composite.format(formatInput=sql.select_pub_image)

        with self.session_scope() as session:
            res = session.execute(composite_query)

            adjacency = defaultdict(list)
            adjacency_lookup = {}
            for r in res:
                sid, spath, did, dpath = r

                adjacency_lookup[spath] = sid
                adjacency_lookup[dpath] = did
                if spath != dpath:
                    adjacency[spath].append(dpath)

        # Add nodes that do not overlap any images
        self.__init__(adjacency, node_id_map=adjacency_lookup)

        # Setup the edges
        self._setup_edges()

    def clear_db(self, tables=None):
        """
        Truncate all of the database tables and reset any
        autoincrement columns to start with 1.

        Parameters
        ----------
        table : str or list of str, optional
                the table name of a list of table names to truncate
        """
        with self.session_scope() as session:
            if tables:
                if isinstance(tables, str):
                    tables = [tables]
            else:
                tables = self.engine.table_names()

            for t in tables:
                if t != 'spatial_ref_sys':
                    try:
                        session.execute(f'TRUNCATE TABLE {t} CASCADE')
                    except Exception as e:
                        raise RuntimeError(f'Failed to truncate table {t}, {t} not modified').with_traceback(e.__traceback__)
                    try:
                        session.execute(f'ALTER SEQUENCE {t}_id_seq RESTART WITH 1')
                    except Exception as e:
                        log.warning(f'Failed to reset primary id sequence for table {t}')

    def cnet_to_db(self, cnet):
        """
        Splits an isis control network into two subsets mirroring the points and measures
        database table formats.

        Parameters
        ----------
        cnet: str or IsisControlNetwork
              The ISIS control network or path to the ISIS control network to be loaded.

        Returns
        -------
        points: IsisControlNetwork
                Subset of the ISIS controlnetwork formatted as io.db.model.Points table

        measures: IsisControlNetwork
                  Subset of the Isis controlnetwork formatted as io.db.model.Measures table
        """

        semi_major, semi_minor = self.config["spatial"]["semimajor_rad"], self.config["spatial"]["semiminor_rad"]

        if isinstance(cnet, str):
            cnet = from_isis(cnet)
        cnet = cnet.rename(columns={'id':'identifier',
                                    'measureChoosername': 'ChooserName',
                                    'sampleResidual':'sampler',
                                    'lineResidual': 'liner'})

        points = cnet.copy(deep=True) # this prevents Pandas value being set on copy of slice warnings
        points.drop_duplicates(subset=['identifier'], inplace=True)
        points.insert(0, 'id', list(range(1,len(points)+1)))
        points[['overlapid','residuals', 'maxResidual']] = None
        points[['cam_type']] = 'isis'

        points['apriori'] = [geoalchemy2.shape.from_shape(shapely.geometry.Point(x,y,z)) for x,y,z in zip(points['aprioriX'].values, points['aprioriY'].values, points['aprioriZ'].values)]
        if (points['adjustedX'] == 0).all():
            points['adjusted'] = points['apriori']
            xyz_data = [points['aprioriX'].values, points['aprioriY'].values, points['aprioriZ'].values]
        else:
            points[['adjusted']] = [geoalchemy2.shape.from_shape(shapely.geometry.Point(x,y,z)) for x,y,z in zip(points['adjustedX'].values, points['adjustedY'].values, points['adjustedZ'].values)]
            xyz_data = [points['adjustedX'].values, points['adjustedY'].values, points['adjustedZ'].values]

        og = reproject(xyz_data, semi_major, semi_minor, 'geocent', 'latlon')
        oc = og2oc(og[0], og[1], semi_major, semi_minor)
        points['geom'] = [geoalchemy2.shape.from_shape(shapely.geometry.Point(lon, lat), srid=self.config['spatial']['latitudinal_srid']) for lon, lat in zip(oc[0], oc[1])]

        cnet.insert(0, 'id', list(range(1,len(cnet)+1)))
        pid_map = {ident: pid for ident, pid in zip(points['identifier'], points['id'])}
        cnet['pointid']  = cnet.apply(lambda row: pid_map[row['identifier']], axis=1)

        with self.session_scope() as session:
            imgs = session.query(Images.serial, Images.id).all()
        iid_map = {ii[0]: ii[1] for ii in imgs}
        cnet['imageid'] = cnet.apply(lambda row: iid_map[row['serialnumber']], axis=1)

        def GoodnessOfFit_value_extract(row):
            mlog = row['measureLog']
            if mlog:
                for m in mlog:
                    if m.messagetype.name == "GoodnessOfFit":
                        return m.value
            return None

        cnet['templateMetric'] = cnet.apply(GoodnessOfFit_value_extract, axis=1)
        cnet['templateShift'] = cnet.apply(lambda row: np.sqrt((row['line']-row['aprioriline'])**2 + (row['sample']-row['apriorisample'])**2) if row['ChooserName'] != row['pointChoosername'] else 0, axis=1)
        cnet['residual'] = np.sqrt(cnet['liner']**2+cnet['sampler']**2)
        cnet['rms'] = np.sqrt(np.mean([cnet['liner']**2, cnet['sampler']**2], axis=0))

        cnet[['phaseError','phaseDiff','phaseShift']] = None
        cnet['weight'] = None

        point_columns = Points.__table__.columns.keys()
        measure_columns = Measures.__table__.columns.keys()
        points = points[point_columns]
        measures = cnet[measure_columns]

        return points, measures

    def place_points_from_cnet(self, cnet, clear_tables=True):
        """
        Loads points from a ISIS control network into an AutoCNet formatted database.

        Parameters
        ----------
        cnet: str or IsisControlNetwork
              The ISIS control network or path to the ISIS control network to be loaded.

        clear_tables: boolean
                  Clears enteries out of the points and measures database tables if True.
                  Appends the control network points and measures onto the current points
                  and measures database tables if False.
        """

        if isinstance(cnet, str):
            cnet = from_isis(cnet)

        points, measures = self.cnet_to_db(cnet)

        engine = self.engine
        with engine.connect() as connection:
            # Execute an SQL COPY from a CSV buffer into the DB

            if engine.dialect.has_table(engine.connect(), 'points', schema='public') and clear_tables:
                connection.execute('DROP TABLE measures, points;')
                Points.__table__.create(bind=engine, checkfirst=True)
                Measures.__table__.create(bind=engine, checkfirst=True)

            points.to_sql('points', connection, schema='public', if_exists='append', index=False, method=io_controlnetwork.copy_from_method)
            measures.to_sql('measures', connection, schema='public', if_exists='append', index=False, method=io_controlnetwork.copy_from_method)

    @classmethod
    def from_cnet(cls, cnet, filelist, config):
        """
        Instantiates and populates a NetworkCandidateGraph from an
        ISIS control network and corresponding cube list.

        Parameters
        ----------
        cnet:  str
               path to control network file from which you want to populate
               the NetworkCandidateGraph.

        filelist:  str
                   path to file containing list of cubes associated with
                   the control network file.

        config : dict, str
                 configuration information; either a path to a yaml
                 file or a dictionary.

        Returns
        -------
        obj:  NetworkCandidateGraph
             The NetworkCandidateGraph populated with the points and measures
             from the control network and the images from the filelist.

        See Also
        --------
        config_from_dict: config documentation
        """
        obj = cls.from_filelist(filelist, config)
        obj.place_points_from_cnet(cnet)

        return obj

    @property
    def measures(self):
        df = pd.read_sql_table('measures', con=self.engine)
        return df

    @property
    def queue_length(self):
        """
        Returns the length of the processing queue.

        Jobs are left on the queue if a cluster job is cancelled. Those cancelled
        jobs are then called on next cluster job launch, causing failures. This
        method provides a check for left over jobs.
        """
        llen = self.redis_queue.llen(self.processing_queue)
        return llen

    @property
    def union(self):
        """
        The boundary formed by unioning (or merging) all of the input footprints. The result
        will likely be a multipolygon, likely with holes where data were not collected.

        Returns
        """
        if not hasattr(self, '_union'):
            with self.session_scope() as session:
                self._union = Images.union(session)
        return self._union

    def overlays(self, size_threshold=0):
        """
        Return the overlays in a database

        Parameters
        ----------
        size_threshold: float
                        Minimum area requirment for returned overlaps. Units are
                        determined by spatial reference system.

        Returns
        -------
        overlays: list of Overlay objects
                 Model information associated with overlaps that contain one or more valid points

        See Also
        --------
        autocnet.io.db.model.Overlay: for description of information associated with Overlay class
        """

        with self.session_scope() as session:
            q = session.query(Overlay).filter(func.ST_Area(Overlay.geom)>=size_threshold)
            overlays = q.all()
            session.expunge_all()
            return overlays

    def empty_overlays(self, filters={'ignore': False}, size_threshold=0):
        """
        Find overlaps that do not contain valid points. By default, valid points
        include not ignored points, but additional point properties can be used to
        further define a valid point. For example, to look at not ignored, free
        (not ground) points; filters = {'ignored': False, 'pointtype': 2}.

        Parameters
        ----------
        filters: dict
                 Points object properties for point filtering.

        size_threshold: float
                        Minimum area requirment for returned overlaps. Units are
                        determined by spatial reference system.

        Returns
        -------
        overlays: list of Overlay objects
                  Model information associated with overlaps that contain no valid points

        See Also
        --------
        autocnet.io.db.model.Overlay: for description of information associated with Overlay class
        autocnet.io.db.model.Points: for description of information associated with Points class
        """
        with self.session_scope() as session:
            # Find overlap ids that contain one or more valid points
            sq = session.query(Overlay.id).join(Points, func.ST_Contains(Overlay.geom, Points.geom))
            for attr, value in filters.items():
                sq = sq.filter(getattr(Points, attr)==value)
            sq = sq.group_by(Overlay.id)

            # find overlap information not satisfying previous query
            q = session.query(Overlay).filter(Overlay.id.notin_(sq)).filter(func.ST_Area(Overlay.geom)>=size_threshold)
            overlays = q.all()
            session.expunge_all()
            return overlays

    def overlay_connection(self, oid):
        """
        Evaluate the connection status of an overlay. An overlap can be empty (no points),
        fully connected (all images are connected by points), or partially connected. The
        first two status return empty lists while partially connected overlaps will return
        a list of image pairs that are missing point connections.

        Parameters
        ----------
        overlay: int
                 Database id of overlay of interest.

        Returns
        -------
        missing_edges: list of tuples
                       tuples correspond to image ids that comprise an overlap
                       but are not connected by a point.
        """

        graph = nx.Graph()

        with self.session_scope() as session:
            # create graph nodes
            overlap = session.query(Overlay).filter(Overlay.id==oid).first()
            ointersections = overlap.intersections
            for ii in ointersections:
                graph.add_node(ii)

            # find measures in relevant overlap and images
            geom = geoalchemy2.shape.from_shape(overlap.geom, srid=self.config['spatial']['latitudinal_srid'])
            q = session.query(Measures).join(Points, Measures.pointid==Points.id).\
                                        filter(func.ST_Contains(geom, Points.geom)).\
                                        filter(Measures.imageid.in_(ointersections))
            df = pd.read_sql(q.statement, session.bind)

            # TO DO: RETURN ALL EDGES
            if len(df) == 0:
                log.info(f'Overlap {oid} is empty')
                return []

            # create graph edges
            for pid, g in df.groupby('pointid'):
                edge_pool = np.sort([row['imageid'] for i, row in g.iterrows()])
                graph.add_edges_from(list(combinations(edge_pool, 2)))

            # evaluate connectivity of overlap
            fully_connected_number_of_edges = scipy.special.comb(graph.number_of_nodes(),2)
            all_edges = list(combinations(graph.nodes, 2))
            if graph.number_of_edges() == fully_connected_number_of_edges:
                log.info(f'Overlap {oid} is fully connected')
                return []

            # return missing image id pairs
            return [e for e in all_edges if e not in graph.edges]

    def cluster_propagate_control_network(self,
                                          base_cnet,
                                          walltime='00:20:00',
                                          chunksize=1000,
                                          exclude=None):
        log.warning('This function is not well tested. No tests currently exists \
        in the test suite for this version of the function.')

        # Setup the redis queue
        rqueue = StrictRedis(host=config['redis']['host'],
                             port=config['redis']['port'],
                             db=0)

        # Push the job messages onto the queue
        queuename = config['redis']['processing_queue']

        groups = base_cnet.groupby('pointid').groups
        for cpoint, indices in groups.items():
            measures = base_cnet.loc[indices]
            measure = measures.iloc[0]

            p = measure.point

            # get image in the destination that overlap
            lon, lat = measures["point"].iloc[0].xy
            msg = {'lon' : lon[0],
                   'lat' : lat[0],
                   'pointid' : cpoint,
                   'paths' : measures['path'].tolist(),
                   'lines' : measures['line'].tolist(),
                   'samples' : measures['sample'].tolist(),
                   'walltime' : walltime}
            rqueue.rpush(queuename, json.dumps(msg, cls=JsonEncoder))

        # Submit the jobs
        submitter = Slurm('acn_propagate',
                     job_name='cross_instrument_matcher',
                     mem_per_cpu=config['cluster']['processing_memory'],
                     time=walltime,
                     partition=config['cluster']['queue'],
                     output=config['cluster']['cluster_log_dir']+'/autocnet.cim-%j')
        job_counter = len(groups.items())
        submitter.submit(array='1-{}'.format(job_counter))
        return job_counter

    def distribute_ground_uniform(self, distribute_points_kwargs={}):
        """
        Distribute candidate ground points into the union of the image footprints. This
        function returns a list of 2d nd-arrays where the first element is the longitude
        and the second element is the latitude.

        Parameters
        ----------
        distirbute_points_kwargs : dict
                                   Of arguments that are passed on the the
                                   distribute_points_in_geom argument in autocnet.cg.cg

        Returns
        -------
        valid : np.ndarray
                n, 2 array with each row in the form lon, lat

        Examples
        --------
        To use this method, one can first define the spacing of ground points in the north-
        south and east-west directions using the `distribute_points_kwargs` keyword argument::

            def ns(x):
                from math import ceil
                return ceil(round(x,1)*3)
            def ew(x):
                from math import ceil
                return ceil(round(x,1)*3)

        Next these arguments can be passed in in order to generate the grid of points::

            distribute_points_kwargs = {'nspts_func':ns, 'ewpts_func':ew, 'method':'classic'}
            valid = ncg.distribute_ground_uniform(distribute_points_kwargs=distribute_points_kwargs)

        At this point, it is possible to visualize the valid points inside of a Jupyter notebook. This
        is frequently convenient when combined with the `ncg.union` property that displays the unioned
        geometries in the NetworkCandidateGraph.

        Finally, the valid points can be propagated using apply. The code below will use the defined base
        to find the most interesting ground feature in the region of the valid point and write that point
        to the table defined by CandidateGroundPoints (autocnet.io.db.model)::

            base = 'mc11_oxia_palus_dir_final.cub'
            ncg.apply('matcher.ground.find_most_interesting_ground', on=valid, args=(base,))
        """
        geom  = self.union
        valid = cg.distribute_points_in_geom(geom, **distribute_points_kwargs)
        return valid

    def distribute_ground_density(self, threshold=4, distribute_points_kwargs={}):
        """
        Distribute candidate ground points into overlaps with a number of images greater than or equal
        to the threshold. This function returns a list of 2d nd-arrays where the first element is the
        longitude and the second element is the latitude.

        Parameters
        ----------
        distirbute_points_kwargs : dict
                                   Of arguments that are passed on the the
                                   distribute_points_in_geom argument in autocnet.cg.cg
        threshold : int
                    Overlaps intersecting threshold images or greater have points placed.
                    Default 4.
        Returns
        -------
        valid : np.ndarray
                n, 2 array in the form lon, lat

        Examples
        --------
        Usage for `distribute_ground_density` is identical to usage for `distribute_ground_uniform`.
        See Also
        --------
        autocnet.graph.network.NetworkCandidateGraph.distribute_ground_uniform
        """
        valid = []
        with self.session_scope() as session:
            res = session.query(Overlay).filter(func.array_length(Overlay.intersections, 1) >= threshold).all()
            for r in res:
                coords = cg.distribute_points_in_geom(r.geom, **distribute_points_kwargs)
                if len(coords) > 0:
                    valid.append(coords)
        valid = np.vstack(valid)
        return valid

    def subpixel_register_points(self, **kwargs):
        subpixel.subpixel_register_points(self.Session, **kwargs)

    def subpixel_register_point(self, pointid, **kwargs):
        subpixel.subpixel_register_point(self.Session, pointid, **kwargs)

    def subpixel_regiter_mearure(self, measureid, **kwargs):
        subpixel.subpixel_register_measure(self.Session, measureid, **kwargs)

    def propagate_control_network(self, control_net, **kwargs):
        cim.propagate_control_network(self.Session,
                                      self.config,
                                      self.dem,
                                      control_net)

    def generate_ground_points(self, ground_mosaic, **kwargs):
        cim.generate_ground_points(self.Session, ground_mosaic, **kwargs)

    def place_points_in_overlaps(self, nodes, **kwargs):
        overlap.place_points_in_overlaps(self.Session,
                                         self.config,
                                         self.dem,
                                         nodes,
                                         **kwargs)
