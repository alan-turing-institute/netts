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
import time
import datetime
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import scipy

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
from motif_helper_functions import motifs, motif_counter, rasterplot, biplot, biplot_3d


# --- Import motif data ---
# If already counted and motif_counts.csv exists, imports motif count data
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graph_data = op.join(graph_dir, 'graph_data.csv')
try:
    # Import motif count data
    df = pd.read_csv(op.join(graph_data))
except FileNotFoundError:
    print('----- Error: Cannot find {}} -----\nIt seems motifs have not been counted yet.\nRun motifs.py to count motifs before running this cell.'.format(graph_data))

# Output directory for figures
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'


# ----------- Quick inspection -----------
# shows missing values as null count (if non-null count == number of entries, then there are no missing values)
df.info()


# ----------- Summary stats on motif counts -----------
# shows missing values as null count (if non-null count == number of entries, then there are no missing values)
motif_cols = list(motifs.keys())[:-1]
# motif_cols = list(motifs.keys())[:4] + ['m07']
# motif_cols = list(motifs.keys())[:4]

# Standardizing data: Z-transform motif counts
# motif_cols = list(motifs.keys())
# for col in motif_cols:
#     df[col] = (df[col] - df[col].mean()) / df[col].std()
#
# df.m13 = np.zeros(len(df.m13))
# motif_cols = motif_cols[:-1]

# motif_cols = list(motifs.keys())[:5] + ['m07']
df[motif_cols].describe()
df[list(motifs.keys())].describe()

# ---------------------- PCA ----------------------
# Do not standardize data, since motif counts are on the same scale
# and also to avoid taking sparse motifs (motifs over m07) into account too much

# PCA
n_components = len(motif_cols) - 1
pca = PCA(n_components=n_components)
pca.fit(df[motif_cols].values)
variance = pca.explained_variance_ratio_  # calculate variance ratios
var = np.cumsum(
    np.round(pca.explained_variance_ratio_, decimals=3) * 100)
print('Variance explained: {}'.format(
    np.round(variance, decimals=3) * 100))
print('Cumulative variance explained: {}'.format(
    var))
# Get Loadings
pc_cols = ['PC' + str(n + 1) for n in range(0, n_components)]
# ----------------------- Plot PCA ----------------------------------------------
loadings = pd.DataFrame(pca.components_.T, columns=pc_cols, index=motif_cols)
print(loadings.round(2))
loadings.round(2).to_csv(op.join(graph_dir, 'pca_loadings.csv'))
components = loadings.values
# --- Biplot with unrotated components ---
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), df.edges)
output = op.join(output_dir, 'PCA_biplot_unrotated' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()
# # ----------------------- Rotate with Varimax -----------------------
# rotate_cols = pc_cols[:2]
# rotator = Rotator(method='varimax')
# rotated_loading_varimax = rotator.fit_transform(
#     loadings[rotate_cols].to_numpy())
# loadings_rot_varimax = pd.DataFrame(
#     rotated_loading_varimax, index=motif_cols, columns=rotate_cols)
# # --- Biplot with Varimax rotation ---
# X_new = rotator.fit_transform(df[motif_cols])
# biplot(X_new[:, 0:2], loadings_rot_varimax.values, df.edges)
# output = op.join(output_dir, 'PCA_biplot_rotated-varimax' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show()
# # ----------------------- Rotate with Promax -----------------------
# rotator = Rotator(method='promax')
# rotated_loading_promax = rotator.fit_transform(loadings[rotate_cols])
# loadings_rot_promax = pd.DataFrame(
#     rotated_loading_promax, index=motif_cols, columns=rotate_cols)
# # --- Biplot with Promax rotation ---
# X_new = rotator.fit_transform(df[motif_cols])
# biplot(X_new[:, 0:2], loadings_rot_promax.values, None)
# output = op.join(output_dir, 'PCA_biplot_rotated-promax' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show()
# ----------------------- Colour by directionality -----------------------
# --- Unrotated ---
labels = df.bidirectional_edges.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), labels)
output = op.join(output_dir, 'PCA_biplot_unrotated_color-bidirectionality' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()
# # --- Rotated : Varimax ---
# X_new = rotator.fit_transform(df[motif_cols])
# biplot(X_new[:, 0:2], loadings_rot_varimax.values, labels)
# output = op.join(output_dir, 'PCA_biplot_rotated-varimax_color-bidirectionality' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show()

# ----------------------- Colour by edges -----------------------
# --- Unrotated ---
labels = df.edges.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), labels)
output = op.join(output_dir, 'PCA_biplot_unrotated_color-edges' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()
# # --- Rotated : Varimax ---
# X_new = rotator.fit_transform(df[motif_cols])
# biplot(X_new[:, 0:2], loadings_rot_varimax.values, labels)
# output = op.join(output_dir, 'PCA_biplot_rotated-varimax_color-edges' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show()

# ----------------------- 3D Plot -----------------------
# ----------- 3D - coloured by node number -----------
labels = df.edges.to_numpy()
X_new = pca.fit_transform(df[motif_cols])
score = X_new[:, 0:3]
coeff = np.transpose(pca.components_[0:3, :])
biplot_3d(score, coeff, labels)

output = op.join(output_dir, 'PCA_biplot_3d_colored-nodes' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# # --- Rotated : Varimax ---
# X_new = rotator.fit_transform(df[motif_cols])
# score = X_new[:, 0:3]
# coeff = loadings_rot_varimax.values
# biplot_3d(score, coeff, labels)
# output = op.join(output_dir, 'PCA_biplot_rotated-varimax_color-edges' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show()

# plt.plot(rotated_loading_promax)
# plt.plot(rotated_loading_varimax)
# plt.xlabel("Promax")
# plt.ylabel("Varimax")
# plt.show()

# np.round(np.abs(rotazted_loading_promax - rotated_loading_varimax), decimals=4)

# TODO: Cluster the motif correlation plot and plot the motifs into the different clusters
# TODO: Colour the datapoints according to cluster identity
# TODO: Exclude the stanza only edges graphs


# ----------------------- 3D Plot with example graphs -----------------------
# ----------- 3D - coloured by node number -----------
labels = df.edges.to_numpy()
X_new = pca.fit_transform(df[motif_cols])
score = X_new[:, 0:3]
coeff = np.transpose(pca.components_[0:3, :])
biplot_3d(score, coeff, labels)
plt.show(block=False)

max_x = int(np.where(score[:, 0] == score[:, 0].max())[0])
max_y = int(np.where(score[:, 1] == score[:, 1].max())[0])
max_z = int(np.where(score[:, 2] == score[:, 2].max())[0])

min_x = np.where(score[:, 0] == score[:, 0].min())[0][0]
min_y = np.where(score[:, 1] == score[:, 1].min())[0][0]
min_z = np.where(score[:, 2] == score[:, 2].min())[0][0]
# --------------------- Import graphs ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)

representative_idx = [min_x, max_x, min_y, max_y, min_z, max_z]
representative_graphs = [G for g, G in enumerate(
    graphs) if g in representative_idx]


fig = plt.figure(figsize=(25.6, 20))
for g, G in enumerate(representative_graphs):
    ax = plt.subplot(3,
                     2, g + 1)
    pos = nx.spring_layout(G)
    plt.axis("off")
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    if g % 2 == 0:
        ax.title.set_text('Lowest PC {} Score'.format(int(np.ceil(g / 2) + 1)))
    else:
        ax.title.set_text('Highest PC {} Score'.format(int(np.ceil(g / 2))))


output = op.join(output_dir, 'RepresentativeGraphs_unrotated' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# ----------------------- Sort raster plot by PC score -----------------------
graph_scores = pd.DataFrame(
    index=graphs, data=score, columns=['PC1', 'PC2', 'PC3'])

plot_fraction = 1
plot_graphs = graph_scores_sorted.iloc[::plot_fraction, :].index
for pc in range(1, 4):
    graph_scores_sorted = graph_scores.sort_values(
        by=['PC{}'.format(pc)], ascending=[True])
    fig = plt.figure(figsize=(20, 20))
    for g, G in enumerate(plot_graphs):
        ax = plt.subplot(np.ceil(np.sqrt(len(graph_scores_sorted))),
                         np.ceil(np.sqrt(len(graph_scores_sorted))), g + 1)
        pos = nx.spring_layout(G)
        plt.axis("off")
        nx.draw_networkx_nodes(G, pos, node_size=20)
        nx.draw_networkx_edges(G, pos, alpha=0.4)
    #
    # --- Optional: Save plot ---
    output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
    output = op.join(
        output_dir, 'GraphsRaster_subset_sorted_by_PC-{}_{}'.format(pc, str(datetime.date.today())))
    plt.savefig(output)
    # plt.show()

# ----------------------- Plot Correlation Plot -----------------------
#
# --------------------- Import graphs ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'

graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)
gprops = graph_properties(graphs, filelist)


X_new = pca.fit_transform(df[motif_cols])
score = X_new[:, 0:3]

for pc in range(0, 3):
    gprops['PC{}_score'.format(pc)] = score[:, pc]

plt.figure(figsize=(25.6, 20))
corrMatrix = gprops.corr()
# sns.heatmap(corrMatrix, mask=np.triu(corrMatrix), annot=True)
sns.heatmap(corrMatrix, annot=True)
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(
    output_dir, 'CorrMat_PCA_GraphProps')
plt.savefig(output)
plt.show()

# --------------------- Correlate with motif counts ---------------------------------------
for pc in range(0, 3):
    df['PC{}_score'.format(pc)] = score[:, pc]

plt.figure(figsize=(25.6, 20))
corrMatrix = df.iloc[:, -16:].corr()
# sns.heatmap(corrMatrix, mask=np.triu(corrMatrix), annot=True)
sns.heatmap(corrMatrix, annot=True)
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(
    output_dir, 'CorrMat_PCA_Motifs')
plt.savefig(output)
plt.show()


# Show only significant
def corr_sig(df=None):
    p_matrix = np.zeros(shape=(df.shape[1], df.shape[1]))
    for col in df.columns:
        for col2 in df.drop(col, axis=1).columns:
            _, p = scipy.stats.pearsonr(df[col], df[col2])
            p_matrix[df.columns.to_list().index(
                col), df.columns.to_list().index(col2)] = p
    return p_matrix


numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
gprops_numeric_nonan = gprops[gprops.columns[~gprops.isnull(
).all()]].select_dtypes(include=numerics)
p_values = corr_sig(gprops_numeric_nonan)
mask = np.invert(np.tril(p_values < 0.05))
