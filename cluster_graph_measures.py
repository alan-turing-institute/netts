#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  cluster_graph_measures.py
#
# Description:
#               Script to describe semantic speech graphs by calculating basic
#               and advanced graph measures.
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

import warnings
warnings.filterwarnings("ignore")
import glob
import os
import os.path as op
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')

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
import scipy


# SemanticSpeechGraph functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs

# Community detection toolbox
import bct
from netneurotools import plotting


# --------------------- Set graph path ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/oasis'
output_dir = op.join(graph_dir, 'output')
output_figures = op.join(graph_dir, 'figures')


# --------------------- Import all graph measures ---------------------------------------
oasis = pd.read_csv(op.join(output_dir, 'graph_data_all_avg.csv'), index_col=0)

# Exclude subject 12 with bad quality transcript
oasis = oasis[oasis.subj != 12]
oasis.subj.unique()

# --------------------- Exclude non-informative columns before correlating ---------------------------------------
#
# exclude_columns = ['average_total_degree_normF', 'parallel_edges_normF',
#                    'parallel_edges_normZ', 'L1_normF', 'group_n', 'group', 'subj']
#
# --------------------- Select only columns that are in Sarahs paper and the connected component measures ---------------------------------------
selected_columns = ['words', 'sentences', 'mean_sentence_length', 'nodes', 'edges',
                    'cc_size_mean', 'cc_size_med', 'connected_components',
                    'max_degree_centrality', 'max_indegree_centrality_value', 'max_outdegree_centrality_value',
                    'cc_size_mean_normZ', 'cc_size_med_normZ', 'connected_components_normZ',
                    'syn_WC', 'syn_Nodes', 'syn_Edges', 'syn_RE', 'syn_PE', 'syn_L1',
                    'syn_L2', 'syn_L3', 'syn_LCC', 'syn_LSC', 'syn_ATD', 'syn_Density',
                    'syn_Diameter', 'syn_ASP', 'syn_CC', 'syn_Degree', 'syn_Degree.1',
                    'syn_Degree.2', 'syn_Degree.3', 'No. words', 'No. sent.',
                    'Sent. length', 'Coh.', 'Max similarity', 'Tangent', 'On-topic']

selected_columns = ['words', 'sentences', 'mean_sentence_length', 'nodes', 'edges',
                    'cc_size_mean', 'cc_size_med', 'connected_components',
                    'max_degree_centrality', 'max_indegree_centrality_value', 'max_outdegree_centrality_value',
                    'cc_size_mean_normZ', 'cc_size_med_normZ', 'connected_components_normZ',
                    'syn_LCC', 'syn_LSC', 'syn_CC',
                    'No. words', 'No. sent.', 'Sent. length',
                    'Coh.', 'Max similarity', 'Tangent', 'On-topic']

selected_columns = ['nodes', 'edges', 'words', 'sentences', 'mean_sentence_length',
                    'cc_size_mean', 'cc_size_med', 'connected_components',
                    # 'max_degree_centrality', 'max_indegree_centrality_value', 'max_outdegree_centrality_value',
                    # 'cc_size_mean_normZ', 'cc_size_med_normZ', 'connected_components_normZ',
                    # 'syn_LCC', 'syn_LSC',
                    'No. words', 'No. sent.', 'Sent. length',
                    'Coh.', 'Max similarity', 'Tangent', 'On-topic']


oasis_selected = oasis[selected_columns]
corrMatrix = oasis_selected.corr()


# --------------------- Louvain Clustering ---------------------------------------

corr = corrMatrix.copy().to_numpy()
nonegative = corr
# nonegative[nonegative < 0] = 0
nonegative = abs(nonegative)

ci, Q = bct.community_louvain(nonegative)
num_ci = len(np.unique(ci))
print('{} clusters detected with a modularity of {:.2f}.'.format(num_ci, Q))

ax = plotting.plot_mod_heatmap(corr, ci, vmin=-1, vmax=1, cmap='viridis',
                               xticklabels=corrMatrix.columns, yticklabels=corrMatrix.columns, figsize=(13.5, 10), xlabelrotation=90)
ax.set_xticklabels(corrMatrix.columns, rotation=30, ha="right")

# plt.xticks(rotation=90)
output = op.join(
    output_figures, 'Clustered_oasis')
plt.savefig(output)
plt.show()
