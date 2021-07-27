'density',
'diameter',
'average_shortest_path',
'clustering',
# edge_list = list(G.edges(data=False))
# nx.write_edgelist(my_G, "test.edgelist", data=False)
# nx.read_edgelist(my_G, "test.edgelist", data=False)
# edge_dict = dict(my_G.edges)


# data = {1: edge_list}
data = {1: [edge_list]}
key = 1
graphs = data[key]
index = 0
G = graphs[0]

# graph = nx.DiGraph(G)

degree = 0

np.count_nonzero(G) < len(G) * degree

graph = nx.DiGraph(G > threshold)

import FinalMotif as fm
fm.findMotifs(data, key, motifSize=3, degree=degree,
              randGraphs=None, useCache=True)


# objects = []
# with (open("aznorbert_corrsd_new.pkl", "rb")) as openfile:
#     while True:
#         try:
#             objects.append(pickle.load(openfile))
#         except EOFError:
#             break

with open("aznorbert_corrsd_new.pkl", mode='r+b', encoding='utf-8') as handle:
    tfidf_vectorizer = pickle.load(handle)


g = my_G

# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# PCA Stuff


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
from compile_graphs_dataset import get_graphs, graph_properties
from graph_analysis_functions import print_bidirectional_edges, print_parallel_edges, get_parallel_edges, central_words, calc_vector_distance, calc_vector_distance_adj, choose_representative_word, find_representative_node_words
import itertools

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler

# --- Import motif data ---
# If already counted and motif_counts.csv exists, imports motif count data
motif_cols = list(motifs.keys())
motif_data = op.join(graph_dir, 'motif_counts.csv')
try:
    # Import motif count data
    df = pd.read_csv(op.join(motif_data))
except FileNotFoundError:
    print('----- Error: Cannot find motif_counts.csv -----\nIt seems motifs have not been counted yet.\nRun motifs.py to count motifs before running this cell.')

# ----------- Plot Motif Counts -----------
# Strip plot
fig = plt.figure(figsize=(25, 9))
plt.title('Motif Counts', fontsize=15)
sns.stripplot(y='value', x='variable',
              data=df_m,
              palette="colorblind",
              )

output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Scatter_motif_counts' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# Histograms
fig = plt.figure(figsize=(25.6, 20))
no_motifs = len(motifs)
for m, mkey in enumerate(motifs):
    ax = plt.subplot(2, np.ceil(no_motifs / 2), m + 1)
    plt.hist(df[mkey])  # , bins=100)
    plt.grid(axis='y', alpha=0.75)
    # plt.ylabel('Frequency', fontsize=15)
    plt.xticks(fontsize=15)
    plt.title(mkey)

output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_motif_counts' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# ---------------------- PCA ----------------------
# PCA implemented in sklearn centers (subtracting the mean from each datapoint).
# But it doesn't scale input data (i.e. divides the data by the data's std dev).
# Therefore, we z-transform the input data before running PCA
#
# Standardizing data: Z-transform motif counts
for col in motif_cols:
    df[col + '_z'] = (df[col] - df[col].mean()) / df[col].std()

# Alternatively, use scipy.stats.zscore:
# for col in motif_cols:
#     df[col + '_z'] == scipy.stats.zscore(df[col])

# Add label
df['tat'] = graph_props.tat
df['label'] = df['tat']  # .apply(lambda i: str(i))
X, y = None, None

motifs_z = [col + '_z' for col in motif_cols]
feat_cols = motifs_z[:-2]
# PCA - other implementation
n_components = 11
pca = PCA(n_components=n_components)
pca.fit(df[feat_cols].values)
variance = pca.explained_variance_ratio_  # calculate variance ratios
var = np.cumsum(
    np.round(pca.explained_variance_ratio_, decimals=3) * 100)
print('Cumulative variance explained: {}'.format(
    var))

# Plot explained Variance
plt.ylabel('% Variance Explained')
plt.xlabel('# of Features')
plt.title('PCA Analysis')
plt.ylim(30, 100.5)
plt.style.context('seaborn-whitegrid')
plt.plot(var)
plt.show()

# Add PCA scores to df
pca_result = pca.transform(df[feat_cols].values)
df['pca-one'] = pca_result[:, 0]
df['pca-two'] = pca_result[:, 1]
df['pca-three'] = pca_result[:, 2]
print('Explained variation per principal component: {}'.format(
    pca.explained_variance_ratio_))


# # Plot covariance of motif counts
# ax = plt.axes()
# X = StandardScaler().fit_transform(df[feat_cols])
# corrmatrix = np.corrcoef(X.T)
# im = ax.imshow(corrmatrix,
#                cmap="RdBu_r", vmin=-1, vmax=1)
# ax.set_xticks(np.arange(len(feat_cols)))
# ax.set_xticklabels(list(feat_cols), rotation=90)
# ax.set_yticks(range(0, len(feat_cols)))
# ax.set_yticklabels(list(feat_cols))
# plt.colorbar(im).ax.set_ylabel("$r$", rotation=0)
# ax.set_title("Motif count correlation matrix")
# plt.tight_layout()
# plt.show()

# ----------------------- Plot PCA -----------------------
# Get Loadings
pc_cols = ['PC' + str(n + 1) for n in range(0, n_components)]

loadings = pd.DataFrame(pca.components_.T, columns=pc_cols, index=feat_cols)
print(loadings.round(2))
loadings.round(2).to_csv(op.join(graph_dir, 'pca_loadings.csv'))
components = loadings.values

# As Matrix
ax = plt.figure(figsize=(16, 10))
vmax = np.abs(components).max()
# plt.imshow(components, cmap="RdBu_r", vmax=vmax, vmin=-vmax)
sns.heatmap(components, annot=True, vmin=-1, vmax=1, center=0,
            cmap='coolwarm')
plt.yticks(np.arange(len(feat_cols)), feat_cols)
plt.title('PCA')
plt.xticks(np.arange(len(pc_cols)), pc_cols)
plt.tight_layout()
plt.show()

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


# ------------ Motif Morphospace ------------
fig = plt.figure(figsize=(25.6, 20))
for m in range(0, 12, 3):
    ax = fig.add_subplot(2, 2, (m / 3) + 1, projection='3d')
    ax.scatter(
        xs=df[f'm{m+1:02d}'],
        ys=df[f'm{m+2:02d}'],
        zs=df[f'm{m+3:02d}'],
        c=pd.to_numeric(df.nodes),
        cmap='tab10',
    )
    ax.set_xlabel(f'motif_{m+1:02d}')
    ax.set_ylabel(f'motif_{m+2:02d}')
    ax.set_zlabel(f'motif_{m+3:02d}')

plt.show()


# ------ 3D plot of PCA with vector piercing components ----
# define vector

# def draw_vector(v0, v1, ax=None):
#     ax = ax or plt.gca()
#     arrowprops = dict(arrowstyle='->',
#                       linewidth=2,
#                       shrinkA=0, shrinkB=0)
#     ax.annotate('', v1, v0, arrowprops=arrowprops)


# ax = plt.figure(figsize=(16, 10)).gca(projection='3d')
# ax.scatter(
#     xs=df["pca-one"],
#     ys=df["pca-two"],
#     zs=df["pca-three"],
#     c=pd.to_numeric(df["y"]),
#     cmap='tab10'
# )
# ax.set_xlabel('pca-one')
# ax.set_ylabel('pca-two')
# ax.set_zlabel('pca-three')

# # plot vector
# for length, vector in zip(pca.explained_variance_, pca.components_):
#     v = vector * 3 * np.sqrt(length)
#     draw_vector(pca.mean_, pca.mean_ + v)

# plt.show()


# Oblique rotation methods: oblimin rotation and promax (recommended)


from pca import pca as pca_pca

# Initialize to reduce the data up to the number of componentes that explains 95% of the variance.
# model = pca(n_components=0.95)

# Or reduce the data towards 2 PCs
model = pca_pca(n_components=2)

# Fit transform
results = model.fit_transform(df[feat_cols])

# Plot explained variance
fig, ax = model.plot()

# Scatter first 2 PCs
fig, ax = model.scatter()

# Make biplot with the number of features
fig, ax = model.biplot(n_feat=11)


# ------- PCA -------
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from advanced_pca import CustomPCA

X_std = StandardScaler().fit_transform(df[feat_cols])

# fit pca objects with and without rotation with 5 principal components
standard_pca5 = CustomPCA(n_components=5).fit(X_std)
varimax_pca5 = CustomPCA(n_components=5, rotation='varimax').fit(X_std)


# from sklearn.decomposition import FactorAnalysis, PCA

# n_comps = 2

methods = [('PCA', PCA()),
           ('Unrotated FA', FactorAnalysis()),
           ('Varimax FA', FactorAnalysis(rotation='varimax'))]
fig, axes = plt.subplots(ncols=len(methods), figsize=(10, 8))
feat_cols = feat_cols
for ax, (method, fa) in zip(axes, methods):
    fa.set_params(n_components=n_comps)
    fa.fit(df[feat_cols])
    #
    components = fa.components_.T
    print("\n\n %s :\n" % method)
    print(components)
    #
    vmax = np.abs(components).max()
    ax.imshow(components, cmap="RdBu_r", vmax=vmax, vmin=-vmax)
    ax.set_yticks(np.arange(len(feat_cols)))
    if ax.is_first_col():
        ax.set_yticklabels(feat_cols)
    else:
        ax.set_yticklabels([])
    ax.set_title(str(method))
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Comp. 1", "Comp. 2"])

# fig.suptitle("Factors")
# plt.tight_layout()
# plt.show()


# --------- Use Varimax rotation to rotate PCA ---------
from factor_analyzer import Rotator
rotate_cols = pc_cols[:2]

# Varimax
rotator = Rotator(method='varimax')
rotated_loading_varimax = rotator.fit_transform(loadings[rotate_cols])
loadings_rot_varimax = pd.DataFrame(
    rotated_loading_varimax, index=feat_cols, columns=rotate_cols)
# Promax
rotator = Rotator(method='promax')
rotated_loading_promax = rotator.fit_transform(loadings[rotate_cols])
loadings_rot_promax = pd.DataFrame(
    rotated_loading_promax, index=feat_cols, columns=rotate_cols)
# Oblimin
rotator = Rotator(method='oblimin')
rotated_loading_oblimin = rotator.fit_transform(loadings[rotate_cols])
loadings_rot_oblimin = pd.DataFrame(
    rotated_loading_oblimin, index=feat_cols, columns=rotate_cols)

print(loadings)
print(loadings_rot_varimax)
print(loadings_rot_promax)
print(loadings_rot_oblimin)


# Plot rotated and unrotated
fig = plt.figure(figsize=(10, 8))
ax = plt.subplot(1, 4, 1)
feat_cols = feat_cols
vmax = np.abs(loadings.values).max()
ax.imshow(loadings, cmap="RdBu_r", vmax=vmax, vmin=-vmax)
ax.set_yticks(np.arange(len(loadings.index)))
ax.set_yticklabels(loadings.index)
ax.set_title('Unrotated')
ax.set_xticks(np.arange(len(loadings.columns)))
ax.set_xticklabels(loadings.columns)

ax = plt.subplot(1, 4, 2)
feat_cols = feat_cols
vmax = np.abs(loadings_rot_varimax.values).max()
ax.imshow(loadings_rot_varimax, cmap="RdBu_r", vmax=vmax, vmin=-vmax)
ax.set_yticks(np.arange(len(loadings_rot_varimax.index)))
ax.set_yticklabels(loadings_rot_varimax.index)
ax.set_title('Rotated_Varimax')
ax.set_xticks(np.arange(len(loadings_rot_varimax.columns)))
ax.set_xticklabels(loadings_rot_varimax.columns)

ax = plt.subplot(1, 4, 3)
vmax = np.abs(loadings_rot_promax.values).max()
ax.imshow(loadings_rot_promax, cmap="RdBu_r", vmax=vmax, vmin=-vmax)
ax.set_yticks(np.arange(len(loadings_rot_promax.index)))
ax.set_yticklabels(loadings_rot_promax.index)
ax.set_title('Rotated_Promax')
ax.set_xticks(np.arange(len(loadings_rot_promax.columns)))
ax.set_xticklabels(loadings_rot_promax.columns)

ax = plt.subplot(1, 4, 4)
vmax = np.abs(loadings_rot_oblimin.values).max()
ax.imshow(loadings_rot_oblimin, cmap="RdBu_r", vmax=vmax, vmin=-vmax)
ax.set_yticks(np.arange(len(loadings_rot_oblimin.index)))
ax.set_yticklabels(loadings_rot_oblimin.index)
ax.set_title('Rotated_Oblimin')
ax.set_xticks(np.arange(len(loadings_rot_oblimin.columns)))
ax.set_xticklabels(loadings_rot_oblimin.columns)

plt.show()

# --------- Biplot with rotated components ---------


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


import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)  # reset ggplot style
# Call the biplot function for only the first 2 PCs
# project the original data into the PCA space
X_new = pca.fit_transform(df[feat_cols])

biplot(X_new[:, 0:2], np.transpose(pca.components_[0:2, :]), y)
plt.show()

# Plot rotated Varimax
from factor_analyzer import Rotator
rotate_cols = pc_cols[:2]
rotator = Rotator(method='varimax')
rotated_loading_varimax = rotator.fit_transform(loadings[rotate_cols])
loadings_rot_varimax = pd.DataFrame(
    rotated_loading_varimax, index=feat_cols, columns=rotate_cols)


X_new = rotator.fit_transform(df[feat_cols])
biplot(X_new[:, 0:2], loadings_rot_varimax.values, y)
plt.show()

# Plot rotated Varimax
rotator = Rotator(method='promax')
rotated_loading_promax = rotator.fit_transform(loadings[rotate_cols])
loadings_rot_promax = pd.DataFrame(
    rotated_loading_promax, index=feat_cols, columns=rotate_cols)


X_new = rotator.fit_transform(df[feat_cols])
biplot(X_new[:, 0:2], loadings_rot_promax.values, y)
plt.show()


variance = pca.explained_variance_ratio_  # calculate variance ratios
var = np.cumsum(
    np.round(pca.explained_variance_ratio_, decimals=3) * 100)
print('Cumulative variance explained: {}'.format(
    var))

# Plot explained Variance
plt.ylabel('% Variance Explained')
plt.xlabel('# of Features')
plt.title('PCA Analysis')
plt.ylim(30, 100.5)
plt.style.context('seaborn-whitegrid')
plt.plot(var)
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

# # --- Rotated : Varimax ---
# X_new = rotator.fit_transform(df[motif_cols])
# biplot(X_new[:, 0:2], loadings_rot_varimax.values, labels)
# output = op.join(output_dir, 'PCA_biplot_rotated-varimax_color-bidirectionality' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show()

# # --- Rotated : Varimax ---
# X_new = rotator.fit_transform(df[motif_cols])
# biplot(X_new[:, 0:2], loadings_rot_varimax.values, labels)
# output = op.join(output_dir, 'PCA_biplot_rotated-varimax_color-edges' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show()


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


# HR Salary Calculation


associate_salary = 1986.52
assistant_salary = 1842.49

one_time_paid = 2066.95


3 * (associate_salary - assistant_salary) - (one_time_paid - associate_salary)


paid_back = 80.42999999999984

owed = 351.6600000000001


syn_nonavg = pd.read_csv(
    '/Users/CN/Dropbox/speech_graphs/oasis/output/syntactic_graph_data.csv')

syn_nonavg.subj = syn_nonavg.subj.astype('int')
syn_nonavg.set_index('subj')
syn = (syn_nonavg.groupby((syn_nonavg.subj != syn_nonavg.subj.shift()).cumsum())
       .mean()
       .reset_index(drop=True))

syn.subj = syn.subj.astype('int')
syn.to_csv(
    '/Users/CN/Dropbox/speech_graphs/oasis/output/syntactic_graph_data_avg.csv')


avg = (raw.groupby((raw.subj != raw.subj.shift()).cumsum())
       .mean()
       .reset_index(drop=True))

avg.subj = avg.subj.astype('float')
avg.subj = avg.subj.astype('int')
nlp.subj = nlp.subj.astype('int')


ls = [el == sorted(avg.subj)[e] for e, el in enumerate(sorted(nlp.subj))]
ls = [el == sorted(avg.subj)[e] for e, el in enumerate(sorted(syn.subj))]

avg.to_csv(
    '/Users/CN/Dropbox/speech_graphs/oasis/output/graph_data_normalised_avg.csv')
