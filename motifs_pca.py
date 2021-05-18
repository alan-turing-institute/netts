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
from motif_helper_functions import motifs, motif_counter, rasterplot, biplot, biplot_3d, Arrow3D, biplot_with_inset


# --- Import data ---
# If full dataset has already been compiled (together with syntactic graph data and nlp measures), load in the full dataset
data_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/output'
graph_data = op.join(data_dir, 'graph_data_all.csv')
df = pd.read_csv(graph_data)

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

# ----------------------- Colour by size & LCC -----------------------
# --- Bidirectionality---
fig = plt.figure(figsize=(25.6, 20))
labels = df.edges.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), labels)
output = op.join(output_dir, 'PCA_PC1-2_biplot_unrotated_color-edges' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# --- LCC---
fig = plt.figure(figsize=(25.6, 20))
labels = df.lcc.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), labels)
output = op.join(output_dir, 'PCA_PC1-2_biplot_unrotated_color-lcc' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# ----------------------- Colour by size & LCC -----------------------
# --- Bidirectionality---
fig = plt.figure(figsize=(25.6, 20))
labels = df.nodes.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:3:2], np.transpose(pca.components_[0:3:2, :]), labels)
output = op.join(output_dir, 'PCA_PC1-3_biplot_unrotated_color-edges' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# --- LCC---
fig = plt.figure(figsize=(25.6, 20))
labels = df.lcc.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:3:2], np.transpose(pca.components_[0:3:2, :]), labels)
output = op.join(output_dir, 'PCA_PC1-3_biplot_unrotated_color-lcc' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# ----------------------- Colour by tat & subject -----------------------
# --- Bidirectionality---
fig = plt.figure(figsize=(25.6, 20))
labels = df.tat.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), labels)
output = op.join(output_dir, 'PCA_PC1-2_biplot_unrotated_color-tat' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# --- LCC---
fig = plt.figure(figsize=(25.6, 20))
labels = df.subj.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), labels)
output = op.join(output_dir, 'PCA_PC1-2_biplot_unrotated_color-subj' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# --- LCC---
fig = plt.figure(figsize=(25.6, 20))
labels = df.m02.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), labels)
output = op.join(output_dir, 'PCA_PC1-2_biplot_unrotated_color-m02' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()
# ----------------------- Colour by directionality & L2 -----------------------
# --- Bidirectionality---
fig = plt.figure(figsize=(25.6, 20))
labels = df.bidirectional_edges.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 1:3], np.transpose(pca.components_[1:3, :]), labels)
output = op.join(output_dir, 'PCA_PC2-3_biplot_unrotated_color-bidirectionality' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# --- L2---
fig = plt.figure(figsize=(25.6, 20))
labels = df.L2.to_numpy()
# array.reshape((3, 3))
# labels = np.array([df.nodes], [df.nodes])
X_new = pca.fit_transform(df[motif_cols])
biplot(X_new[:, 1:3], np.transpose(pca.components_[1:3, :]), labels)
output = op.join(output_dir, 'PCA_PC2-3_biplot_unrotated_color-L2' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


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

# ----------------------- 3D Plot -----------------------
# ----------- 3D - coloured by node number -----------
labels = df.L2.to_numpy()
X_new = pca.fit_transform(df[motif_cols])
score = X_new[:, 0:3]
coeff = np.transpose(pca.components_[0:3, :])
biplot_3d(score, coeff, labels)

output = op.join(output_dir, 'PCA_biplot_3d_colored-l2' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# TODO: Cluster the motif correlation plot and plot the motifs into the different clusters
# TODO: Colour the datapoints according to cluster identity
# TODO: Exclude the stanza only edges graphs


# ----------------------- 3D Plot with example graphs -----------------------
# ----------- 3D - coloured by node number -----------
labels = df.L2.to_numpy()
X_new = pca.fit_transform(df[motif_cols])
score = X_new[:, 0:3]
coeff = np.transpose(pca.components_[0:3, :])
biplot_3d(score, coeff, labels)
plt.show(block=False)

# --------------------- Find most representative graphs ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)


max_PC1 = int(np.where(score[:, 0] == score[:, 0].max())[0])
max_PC2 = int(np.where(score[:, 1] == score[:, 1].max())[0])
max_PC3 = int(np.where(score[:, 2] == score[:, 2].max())[0])

min_PC1 = np.where(score[:, 0] == score[:, 0].min())[0][0]
min_PC2 = np.where(score[:, 1] == score[:, 1].min())[0][0]
min_PC3 = np.where(score[:, 2] == score[:, 2].min())[0][0]
representative_idx = [min_PC1, max_PC1, min_PC2, max_PC2, min_PC3, max_PC3]
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


# ----------- Plot PCA Scores : 3D - coloured by size & LCC -----------
for pc in range(0, 3):
    df['PC{}_score'.format(pc)] = score[:, pc]

fig = plt.figure(figsize=(25.6, 20))
ax = plt.axes(projection='3d')
ax.scatter(
    xs=df['PC0_score'],
    ys=df['PC1_score'],
    zs=df['PC2_score'],
    c=pd.to_numeric(df.edges),
    cmap='rocket',
)
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')

output = op.join(output_dir, 'PCA_score_3d_colored-edges' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


fig = plt.figure(figsize=(25.6, 20))
ax = plt.axes(projection='3d')
ax.scatter(
    xs=df['PC0_score'],
    ys=df['PC1_score'],
    zs=df['PC2_score'],
    c=pd.to_numeric(df.lcc),
    cmap='rocket',
)
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')

output = op.join(output_dir, 'PCA_score_3d_colored-lcc' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# ----------- Plot PCA Scores : 3D - coloured by size & LCC -----------
for pc in range(0, 3):
    df['PC{}_score'.format(pc)] = score[:, pc]

fig = plt.figure(figsize=(25.6, 20))
ax = plt.axes(projection='3d')
ax.scatter(
    xs=df['PC0_score'],
    ys=df['PC1_score'],
    zs=df['PC2_score'],
    c=pd.to_numeric(df.edges),
    cmap='rocket',
)
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')

output = op.join(output_dir, 'PCA_score_3d_colored-edges' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


fig = plt.figure(figsize=(25.6, 20))
ax = plt.axes(projection='3d')
ax.scatter(
    xs=df['PC0_score'],
    ys=df['PC1_score'],
    zs=df['PC2_score'],
    c=pd.to_numeric(df.lcc),
    cmap='rocket',
)
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')

output = op.join(output_dir, 'PCA_score_3d_colored-lcc' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# Import Graphs
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)


# ------------- Biplot with mini graph insets -------------
# Info on plotting insets: https://matplotlib.org/1.3.1/mpl_toolkits/axes_grid/users/overview.html#insetlocator
labels = df.bidirectional_edges.to_numpy()
labels = None
score = pca.fit_transform(df[motif_cols])

x_PC = 1
y_PC = 3
coeff = np.transpose(pca.components_[[x_PC - 1, y_PC - 1], :])

# biplot_with_inset(score, coeff, labels, graphs, x_PC, y_PC)
biplot_with_inset(score, coeff, labels, graphs, x_PC, y_PC)


# ================ Correlation plots ============


plt.figure(figsize=(25.6, 20))
corrMatrix = df.iloc[:, -16:].corr()
# sns.heatmap(corrMatrix, mask=np.triu(corrMatrix), annot=True)
sns.heatmap(corrMatrix, annot=True)
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(
    output_dir, 'CorrMat_PCA_Syn')
plt.savefig(output)
plt.show()
