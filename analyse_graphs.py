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

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D

# --------------------- Import graphs ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'

graphs, filelist = get_graphs(graph_dir)
graph_props = graph_properties(graphs, filelist)

# --- Count motifs or if already counted, import motif count data ---

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

# Z-score motif counts
for col in motif_cols:
    df[col + '_z'] = (df[col] - df[col].mean()) / df[col].std()

# for col in motif_cols:
#     df[col + '_z'] == scipy.stats.zscore(df[col])

# Add label
df['y'] = graph_props.tat
df['label'] = df['y'].apply(lambda i: str(i))
X, y = None, None

motifs_z = [col + '_z' for col in motif_cols]
feat_cols = motifs_z[:-2]
# PCA
pca = PCA(n_components=3)
pca_result = pca.fit_transform(df[feat_cols].values)
df['pca-one'] = pca_result[:, 0]
df['pca-two'] = pca_result[:, 1]
df['pca-three'] = pca_result[:, 2]
print('Explained variation per principal component: {}'.format(
    pca.explained_variance_ratio_))

plt.figure(figsize=(16, 10))
sns.scatterplot(
    x="pca-one", y="pca-two",
    hue="y",
    palette=sns.color_palette("hls", len(df.label.cat.categories)),
    data=df,
    legend="full",
    alpha=0.6
)
plt.show()

# 3D plot of PCA
ax = plt.figure(figsize=(16, 10)).gca(projection='3d')
ax.scatter(
    xs=df["pca-one"],
    ys=df["pca-two"],
    zs=df["pca-three"],
    c=pd.to_numeric(df["y"]),
    cmap='tab10'
)
ax.set_xlabel('pca-one')
ax.set_ylabel('pca-two')
ax.set_zlabel('pca-three')
plt.show()


# 3D plot of Motif Morphospace
ax = plt.figure(figsize=(16, 10)).gca(projection='3d')
ax.scatter(
    xs=df["m01"],
    ys=df["m02"],
    zs=df["m03"],
    c=pd.to_numeric(df["y"]),
    cmap='tab10'
)
ax.set_xlabel('Motif_01')
ax.set_ylabel('Motif_02')
ax.set_zlabel('Motif_03')
plt.show()


# 3D plot of Motif Morphospace
ax = plt.figure(figsize=(16, 10)).gca(projection='3d')
ax.scatter(
    xs=df["m04"],
    ys=df["m05"],
    zs=df["m06"],
    c=pd.to_numeric(df["y"]),
    cmap='tab10'
)
ax.set_xlabel('Motif_04')
ax.set_ylabel('Motif_05')
ax.set_zlabel('Motif_06')
plt.show()


df.var()
df.mean()


# ------ 3D plot of PCA with vector piercing components ----
# define vector

def draw_vector(v0, v1, ax=None):
    ax = ax or plt.gca()
    arrowprops = dict(arrowstyle='->',
                      linewidth=2,
                      shrinkA=0, shrinkB=0)
    ax.annotate('', v1, v0, arrowprops=arrowprops)


ax = plt.figure(figsize=(16, 10)).gca(projection='3d')
ax.scatter(
    xs=df["pca-one"],
    ys=df["pca-two"],
    zs=df["pca-three"],
    c=pd.to_numeric(df["y"]),
    cmap='tab10'
)
ax.set_xlabel('pca-one')
ax.set_ylabel('pca-two')
ax.set_zlabel('pca-three')

# plot vector
for length, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(length)
    draw_vector(pca.mean_, pca.mean_ + v)

plt.show()
