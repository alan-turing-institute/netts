#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  motifs_pca.py
#
# Description:
#               Script to analyse semantic speech graphs
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

import os
import os.path as op
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
# import sys
# sys.path.extend([
#     '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/',
#     '/Users/CN/Documents/Projects/Cambridge/Network-Motif/',
#     '/Users/CN/Documents/Projects/Cambridge/orca-py/'])

# PCA Packages
from sklearn.decomposition import PCA
# from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from factor_analyzer import Rotator

# Graph analysis functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs
from graph_analysis_functions import print_bidirectional_edges, print_parallel_edges, get_parallel_edges, central_words, calc_vector_distance, calc_vector_distance_adj, choose_representative_word, find_representative_node_words

# Motif analysis functions
from motif_helper_functions import motif_counter, rasterplot, biplot

# --- Import graphs ---
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)
graph_props = graph_properties(graphs, filelist)
print('Imported and described {0} graphs.\n{1} subjects described {2} ± {3} pictures on average.'.format(
    graph_props.shape[0], len(graph_props.subj.unique()), graph_props.subj.value_counts().mean(), round(graph_props.subj.value_counts().std(), 2)))

# --- Import motif data ---
# If already counted and motif_counts.csv exists, imports motif count data
motif_cols = list(motifs.keys())
motif_data = op.join(graph_dir, 'motif_counts.csv')
try:
    # Import motif count data
    df = pd.read_csv(op.join(motif_data))
except FileNotFoundError:
    print('----- Error: Cannot find motif_counts.csv -----\nIt seems motifs have not been counted yet.\nRun motifs.py to count motifs before running this cell.')

# ---------------------- PCA ----------------------
# Standardizing data: Z-transform motif counts
for col in motif_cols:
    df[col + '_z'] = (df[col] - df[col].mean()) / df[col].std()

motifs_z = [col + '_z' for col in motif_cols]
feat_cols = motifs_z[:-2]
# PCA
n_components = 11
pca = PCA(n_components=n_components)
pca.fit(df[feat_cols].values)
variance = pca.explained_variance_ratio_  # calculate variance ratios
var = np.cumsum(
    np.round(pca.explained_variance_ratio_, decimals=3) * 100)
print('Variance explained: {}'.format(
    np.round(variance, decimals=3) * 100))
print('Cumulative variance explained: {}'.format(
    var))
# Get Loadings
pc_cols = ['PC' + str(n + 1) for n in range(0, n_components)]
# ----------------------- Plot PCA -----------------------
loadings = pd.DataFrame(pca.components_.T, columns=pc_cols, index=feat_cols)
print(loadings.round(2))
loadings.round(2).to_csv(op.join(graph_dir, 'pca_loadings.csv'))
components = loadings.values
# --------- Biplot with unrotated components ---------
X_new = pca.fit_transform(df[feat_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), None)
plt.show()
# --------- Rotate with Varimax ---------
rotate_cols = pc_cols[:2]
rotator = Rotator(method='varimax')
rotated_loading_varimax = rotator.fit_transform(loadings[rotate_cols])
loadings_rot_varimax = pd.DataFrame(
    rotated_loading_varimax, index=feat_cols, columns=rotate_cols)
# --------- Biplot with rotated components ---------
X_new = rotator.fit_transform(df[feat_cols])
biplot(X_new[:, 0:2], loadings_rot_varimax.values, None)
plt.show()
# --------- Rotate with Promax ---------
rotator = Rotator(method='promax')
rotated_loading_promax = rotator.fit_transform(loadings[rotate_cols])
loadings_rot_promax = pd.DataFrame(
    rotated_loading_promax, index=feat_cols, columns=rotate_cols)
# --------- Biplot with rotated components ---------
X_new = rotator.fit_transform(df[feat_cols])
biplot(X_new[:, 0:2], loadings_rot_promax.values, None)
plt.show()

plt.plot(rotated_loading_promax)
plt.plot(rotated_loading_varimax)
plt.xlabel("Promax")
plt.ylabel("Varimax")
plt.show()

np.round(np.abs(rotazted_loading_promax - rotated_loading_varimax), decimals=4)

# TODO: Cluster the motif correlation plot and plot the motifs into the different clusters
# TODO: Colour the datapoints according to cluster identity
