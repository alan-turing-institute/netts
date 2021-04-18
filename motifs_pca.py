#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  analyse_graphs.py
#
# Description:
#               Script to analyse semantic speech graphs
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

# Number of Tats for each stimulus
# Stimulus  N   N_transcripts
# TAT8     26   28
# TAT10    64   68
# TAT13    59   61
# TAT19    30   32
# TAT21    13   13
# TAT24    42   43
# TAT28    13   /
# TAT30    39   43

from motifs import motifs, motif_counter
import networkx as nx
import os
import os.path as op
import pandas as pd
import sys
sys.path.extend([
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/',
    '/Users/CN/Documents/Projects/Cambridge/Network-Motif/',
    '/Users/CN/Documents/Projects/Cambridge/orca-py/'])
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import datetime
import glob
import re
from pprint import pprint
import seaborn as sns
import collections
from compile_graphs_dataset import get_graphs, graph_properties
from graph_analysis_functions import print_bidirectional_edges, print_parallel_edges, get_parallel_edges, central_words, calc_vector_distance, calc_vector_distance_adj, choose_representative_word, find_representative_node_words
import itertools
# PCA Packages
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from factor_analyzer import Rotator

# Define biplot function


def biplot(score, coeff, y):
    '''
    Author: Serafeim Loukas, serafeim.loukas@epfl.ch
    Inputs:
       score: the projected data
       coeff: the eigenvectors (PCs)
       y: the class labels
   '''
    #
    #
    xs = score[:, 0]  # projection on PC1
    ys = score[:, 1]  # projection on PC2
    n = coeff.shape[0]  # number of variables
    plt.figure(figsize=(10, 8), dpi=100)
    classes = np.unique(y)
    colors = ['g', 'r', 'y']
    markers = ['o', '^', 'x']
    for s, l in enumerate(classes):
        plt.scatter(xs[y == l], ys[y == l], c=colors[s],
                    marker=markers[s])  # color based on group
        for i in range(n):
            # plot as arrows the variable scores (each variable has a score for PC1 and one for PC2)
            plt.arrow(0, 0, coeff[i, 0], coeff[i, 1], color='k',
                      alpha=0.9, linestyle='-', linewidth=1.5, overhang=0.2)
            plt.text(coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, "Var" +
                     str(i + 1), color='k', ha='center', va='center', fontsize=10)
        plt.xlabel("PC{}".format(1), size=14)
        plt.ylabel("PC{}".format(2), size=14)
        limx = int(xs.max()) + 1
        limy = int(ys.max()) + 1
        plt.xlim([-limx, limx])
        plt.ylim([-limy, limy])
        plt.grid()
        plt.tick_params(axis='both', which='both', labelsize=14)


# --- Count motifs or if already counted, import motif count data ---
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graphs, filelist = get_graphs(graph_dir)
graph_props = graph_properties(graphs, filelist)
# Count motifs
already_counted = True
if already_counted is False:
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
    df.to_csv(op.join(graph_dir, 'motif_counts.csv'))
else:
    # Import motif count data
    motif_cols = list(motifs.keys())
    df = pd.read_csv(op.join(graph_dir, 'motif_counts.csv'))

df_m = pd.melt(df, id_vars=df.columns[0], value_vars=motif_cols)
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
