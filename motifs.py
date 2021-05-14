#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  motifs.py
#
# Description:
#               Counts motifs in semantic speech networks.
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate


import os
import os.path as op
import time
import datetime
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

# Graph analysis functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs
from graph_analysis_functions import print_bidirectional_edges, print_parallel_edges, get_parallel_edges, central_words, calc_vector_distance, calc_vector_distance_adj, choose_representative_word, find_representative_node_words

# Motif analysis functions
from motif_helper_functions import motifs, motif_counter, rasterplot, biplot


# ------------------------------------------------------------------------------
# Time execution of script
start_time = time.time()

# --- Import graphs ---
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)
graph_props = pd.read_csv(op.join(graph_dir, 'graph_data.csv'))
# --- Count motifs ---
# If already counted and motif_counts.csv exists, imports motif count data
motif_data = op.join(graph_dir, 'motif_counts.csv')
if op.isfile(motif_data):
    # Import motif count data
    motif_cols = list(motifs.keys())
    df = pd.read_csv(op.join(graph_dir, 'motif_counts.csv'))
else:
    motif_counts = []
    for G in graphs:
        G = nx.convert_node_labels_to_integers(G, label_attribute='old_label')
        G = nx.DiGraph(G)
        motif_count = motif_counter(G, motifs)
        motif_counts.append(motif_count)
    #
    # Convert motif counts to Pandas DataFrame
    motif_cols = list(motifs.keys())
    X = [list(x.values()) for x in motif_counts]
    df = pd.DataFrame(X, columns=motif_cols)
    df.to_csv(op.join(graph_dir, 'output/motif_counts.csv'))


# Print execution time
print("Counting motifs in %s graphs finished in --- %s seconds ---" %
      (len(graphs), time.time() - start_time))
