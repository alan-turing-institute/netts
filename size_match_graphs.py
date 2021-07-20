#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  size_match_graphs.py
#
# Description:
#               Script to find size-matched graphs for each oasis graph from the
#               general public graphs to normalise graph measures.
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

import glob
import os
import os.path as op
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')

import numpy as np


# SemanticSpeechGraph functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs
from word_embedding_analysis import central_node_distance, adjacent_node_distance, adjacent_edge_distance

# --------------------- Set graph path ---------------------------------------
graph_dir_oasis = '/Users/CN/Dropbox/speech_graphs/oasis'
graph_dir_genpub = '/Users/CN/Dropbox/speech_graphs/all_tats'
# --------------------- Import OASIS graphs ---------------------------------------
graphs_oasis, filelist = get_graphs(graph_dir_oasis)
graphs_oasis, filelist = exclude_empty_graphs(
    graphs_oasis, filelist, be_quiet=True)
oasis = graph_properties(graphs_oasis, filelist)
# --------------------- Import GENPUB graphs ---------------------------------------
graphs_genpub, filelist = get_graphs(graph_dir_genpub)
graphs_genpub, filelist = exclude_empty_graphs(
    graphs_genpub, filelist, be_quiet=True)
genpub = graph_properties(graphs_genpub, filelist)

# --------------------- Find a size-matched graph for each oasis graph in the general public dataset ---------------------------------------
genpub_sizes = [(n, e) for n, e in zip(genpub.nodes, genpub.edges)]

size_matches = [genpub_sizes.count((n, e))
                for n, e in zip(oasis.nodes, oasis.edges)]

size_matches.count(0)
size_matches = np.array(size_matches)

print('Of the {0} graphs, {1} have at least one size match ({2} ± {3} matches on average, range {4}-{5}) and {6} graphs have no match.'.format(
    size_matches.shape[0], np.where(size_matches > 0)[0].shape[0],
    round(size_matches[np.where(size_matches > 0)].mean(), 2),
    round(size_matches[np.where(size_matches > 0)].std(), 2),
    size_matches[np.where(size_matches > 0)].min(),
    size_matches[np.where(size_matches > 0)].max(),
    np.where(size_matches == 0)[0].shape[0]))


(n, e) in genpub_sizes
matches = [(n_o, e_o) for n_o, e_o in zip(oasis.nodes, oasis.edges)
           for n_gp, e_gp in zip(genpub.nodes, genpub.edges)]
