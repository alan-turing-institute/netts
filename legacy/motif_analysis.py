# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'
# # Motif Analysis
#
# Analysing graphs according to their 3-node motifs.
#


import os
import os.path as op
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import datetime


# Graph analysis functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs
from graph_analysis_functions import print_bidirectional_edges, print_parallel_edges, get_parallel_edges, central_words, calc_vector_distance, calc_vector_distance_adj, choose_representative_word, find_representative_node_words

# Motif analysis functions
from motif_helper_functions import motifs, rasterplot, biplot


# PCA Packages
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from factor_analyzer import Rotator


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
motif_cols = list(motifs.keys())
df[motif_cols].describe()


# ----------- Plot Motif Counts : Stripplot -----------
# Reformat df for strip plot
df_m = pd.melt(df, id_vars=df.columns[0], value_vars=motif_cols)
# strip plot
fig = plt.figure(figsize=(25, 9))
plt.title('Motif Counts', fontsize=15)
sns.stripplot(y='value', x='variable',
              data=df_m,
              palette="colorblind",
              )

output = op.join(output_dir, 'Scatter_motif_counts' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# ----------- Plot Motif Counts : Histogram -----------
fig = plt.figure(figsize=(25.6, 20))
no_motifs = len(motifs)
for m, mkey in enumerate(motifs):
    ax = plt.subplot(2, int(np.ceil(no_motifs / 2)), m + 1)
    plt.hist(df[mkey])  # , bins=100)
    plt.grid(axis='y', alpha=0.75)
    # plt.ylabel('Frequency', fontsize=15)
    plt.xticks(fontsize=15)
    plt.title(mkey)

output = op.join(output_dir, 'Hist_motif_counts' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# ----------- Plot Motif Counts : 3D - coloured by node number -----------
fig = plt.figure(figsize=(25.6, 20))
for m in range(0, 12, 3):
    ax = fig.add_subplot(2, 2, int((m / 3) + 1), projection='3d')
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


output = op.join(output_dir, 'Motif_counts_3d_colored-nodes' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# ----------- Plot Motif Counts : 3D - coloured by bidirectional edges -----------
fig = plt.figure(figsize=(25.6, 20))
for m in range(0, 12, 3):
    ax = fig.add_subplot(2, 2, int((m / 3) + 1), projection='3d')
    ax.scatter(
        xs=df[f'm{m+1:02d}'],
        ys=df[f'm{m+2:02d}'],
        zs=df[f'm{m+3:02d}'],
        c=pd.to_numeric(df.bidirectional_edges),
        cmap='tab10',
    )
    ax.set_xlabel(f'motif_{m+1:02d}')
    ax.set_ylabel(f'motif_{m+2:02d}')
    ax.set_zlabel(f'motif_{m+3:02d}')

output = op.join(output_dir, 'Motif_counts_3d_colored-bidirect' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()


# ----------- Plot Motif Counts : 3D - coloured by edges -----------
fig = plt.figure(figsize=(25.6, 20))
for m in range(0, 12, 3):
    ax = fig.add_subplot(2, 2, int((m / 3) + 1), projection='3d')
    ax.scatter(
        xs=df[f'm{m+1:02d}'],
        ys=df[f'm{m+2:02d}'],
        zs=df[f'm{m+3:02d}'],
        c=pd.to_numeric(df.edges),
        cmap='tab10',
    )
    ax.set_xlabel(f'motif_{m+1:02d}')
    ax.set_ylabel(f'motif_{m+2:02d}')
    ax.set_zlabel(f'motif_{m+3:02d}')

output = op.join(output_dir, 'Motif_counts_3d_colored-bidirect' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()

# ----------- Plot Motif Counts : 3D - coloured by nodes/edges -----------
fig = plt.figure(figsize=(25.6, 20))
for m in range(0, 12, 3):
    ax = fig.add_subplot(2, 2, int((m / 3) + 1), projection='3d')
    ax.scatter(
        xs=df[f'm{m+1:02d}'],
        ys=df[f'm{m+2:02d}'],
        zs=df[f'm{m+3:02d}'],
        c=pd.to_numeric(df.nodes / df.edges),
        cmap='tab10',
    )
    ax.set_xlabel(f'motif_{m+1:02d}')
    ax.set_ylabel(f'motif_{m+2:02d}')
    ax.set_zlabel(f'motif_{m+3:02d}')

output = op.join(output_dir, 'Motif_counts_3d_colored-bidirect' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()
