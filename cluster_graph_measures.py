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
output_figs = op.join(graph_dir, 'figures')

# --------------------- Import all graph measures ---------------------------------------
oasis = pd.read_csv(op.join(output_dir, 'graph_data_all_avg.csv'), index_col=0)
corrMatrix = oasis.drop(columns='subj').corr()


# --------------------- Plot correlation matrix ---------------------------------------

# plt.figure(figsize=(25.6, 20))
# # sns.heatmap(corrMatrix, mask=np.triu(corrMatrix), annot=True)
# sns.heatmap(corrMatrix, annot=True)
# output = op.join(
#     output_figs, 'CorrMat_All_GraphProps')
# plt.savefig(output)
# plt.show()


# --------------------- Louvain Clustering ---------------------------------------

corr = corrMatrix.copy().to_numpy()
nonegative[corr < 0] = 0

ci, Q = bct.community_louvain(nonegative, gamma=1)
num_ci = len(np.unique(ci))
print('{} clusters detected with a modularity of {:.2f}.'.format(num_ci, Q))


plotting.plot_mod_heatmap(corr, ci, vmin=-1, vmax=1, cmap='viridis',
                          xticklabels=corrMatrix.columns, yticklabels=corrMatrix.columns)

plt.show()
