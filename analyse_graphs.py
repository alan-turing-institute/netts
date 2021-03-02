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
# TAT8    28
# TAT10   68
# TAT13   61
# TAT19   32
# TAT21   13
# TAT24   43
# TAT27   0
# TAT30   43

import networkx as nx
import os
import os.path as op
import pandas as pd
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import datetime
import glob
import re
from pprint import pprint
import seaborn as sns


graph_dir = '/Users/CN/Dropbox/speech_graphs/'
# --------------------- Read several graphs ---------------------------------------
filelist = sorted(glob.glob(op.join(graph_dir, 'all_tats', '*.gpickle')))

# filelist = sorted(glob.glob(op.join(graph_dir, 'pilot', '*.gpickle')))
# filelist.extend(
#     sorted(glob.glob(op.join(graph_dir, 'general_public_tat', '*.gpickle'))))
graphs = []
for filename in filelist:
    # print(f, filename)
    graph = op.join(graph_dir, filename)
    graphs.append(nx.read_gpickle((graph)))

for G in graphs:
    # Node number & Edge number
    print('Nodes: {} \t Edges: {}'.format(len(G.nodes()), G.size()))

# --------------------- Collect properties ---------------------------------------
g_properties = []
for g, G in enumerate(graphs):
    filename = filelist[g]
    # find tat index (two-digit combination from 00 to 39 after word "TAT")
    tat = re.findall(r"([0-3][0-9])\D", filename.split('TAT')[1])[0]
    # find subject id (7 digit combination before word "TAT")
    subj = filename.split('-TAT')[0][-7:]
    # Convert graph to MultiDiGraph
    G = nx.MultiDiGraph(G)  # (only for current versions of the gpickle graphs)
    # Get basic graph descriptors
    n_nodes = len(G.nodes())
    n_edges = G.size()
    # Get number of parallel edges
    arr = nx.to_numpy_matrix(G)
    num_multiedges = np.sum(arr >= 2)
    # LCC
    lcc = len(max(nx.weakly_connected_components(G), key=len))
    # LSC
    lsc = len(max(nx.strongly_connected_components(G), key=len))
    # if lsc == 1:
    #     print('=======================')
    #     print(max(nx.strongly_connected_components(G), key=len))
    #     print('-----------')
    #     print(list(nx.selfloop_edges(G, data=True)))
    #     break
    # --- Properties that are only defined for non-multi Graphs ---
    # G = nx.DiGraph(G)
    # nx.clustering(G)
    # avg_clustering = nx.average_clustering(G)
    # nx.average_degree_connectivity(G)
    # nx.average_neighbor_degree(G)
    # avg_node_conn = nx.average_node_connectivity(G)
    g_properties.append([
        subj,
        tat,
        n_nodes,
        n_edges,
        num_multiedges,
        lcc,
        lsc
        # avg_clustering,
        # avg_node_conn
    ])

# for i in nx.weakly_connected_components(G):
#     print(i)
# for c in sorted(nx.weakly_connected_components(G), key=len, reverse=True):
#     print(nx.average_shortest_path_length(c))
# # --------------------- Visualise parallel edges-----------------------------------
# # for g, G in enumerate(graphs):
# # Plot graph as matrix
# fig, ax = plt.subplots()
# arr = nx.to_numpy_matrix(G)
# im = plt.imshow(arr, interpolation='nearest', cmap='gray')
# node_labels = list(G.nodes())
# ax.set_xticks(np.arange(len(node_labels)))
# ax.set_xticklabels(node_labels)
# ax.set_yticks(np.arange(len(node_labels)))
# ax.set_yticklabels(node_labels)
# plt.show()

# --------------------- Print parallel edges ---------------------------------------
# Print all parallel edge data
for g, G in enumerate(graphs):
    # print('\n', filelist[g].split('SpeechGraph_')[1])
    arr = nx.to_numpy_matrix(G)
    boo = (arr >= 2)
    if boo.any():
        parallel_edges = np.where(boo)
        node_labels = list(G.nodes())
        # print info for all parallel edges
        for p in range(0, parallel_edges[0].shape[0]):
            node1 = node_labels[parallel_edges[0][p]]
            node2 = node_labels[parallel_edges[1][p]]
            print('\n', g, ' : ', node1, node2)
            # print(node1, node2)
            # par_edges_info = G.get_edge_data(node1, node2)
            # print([edge_info['confidence']
            #        for edge_info in par_edges_info.values()])
            # print([edge_info['relation']
            #        for edge_info in par_edges_info.values()])
            #             pprint(par_edges_info)
# ---> There are no parallel edges after the edge cleaning!

# # --------------------- Get edge labels ---------------------------------------
# edge_labels = dict([((u, v,), d['relation'])
#                     for u, v, d in G.edges(data=True)])

# --------------------- Make dataframe ---------------------------------------
df = pd.DataFrame(g_properties, columns=[
    'subj', 'tat',
    'nodes', 'edges', 'num_multiedges', 'lcc', 'lsc'
    # 'cc','node_conn'
])

# ----------- LCC -----------
# Set up the plot
ax = plt.subplot(1, 2, 1)
hist, bin_edges = np.histogram(df.lcc, bins=1000)
# plt.figure(figsize=[10, 8])
plt.bar(bin_edges[:-1], hist, color='#0504aa', alpha=0.7)
plt.xlim(min(bin_edges), max(bin_edges))
plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Nodes', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.title('LCC', fontsize=15)
# ----------- LSC -----------
# Set up the plot
ax = plt.subplot(1, 2, 2)
hist, bin_edges = np.histogram(df.lsc, bins=1000)
# plt.figure(figsize=[10, 8])
plt.bar(bin_edges[:-1], hist, color='#0504aa', alpha=0.7)
plt.xlim(min(bin_edges), max(bin_edges))
plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Nodes', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.title('LSC', fontsize=15)
plt.show()

# ----------- LCC, LSC, Nodes, Edges by TAT -----------
ax = plt.subplot(2, 2, 1)
sns.boxplot(y='lcc', x='tat',
            data=df,
            palette="colorblind",
            # hue='year'
            )
ax = plt.subplot(2, 2, 2)
sns.boxplot(y='lsc', x='tat',
            data=df,
            palette="colorblind",
            # hue='year'
            )
ax = plt.subplot(2, 2, 3)
sns.boxplot(y='nodes', x='tat',
            data=df,
            palette="colorblind",
            # hue='year'
            )
ax = plt.subplot(2, 2, 4)
sns.boxplot(y='edges', x='tat',
            data=df,
            palette="colorblind",
            # hue='year'
            )
plt.show()

# ----------- Plot nodes vs edges -----------
tats = df.tat.unique()
colors = cm.rainbow(np.linspace(0, 1, len(tats)))
fig, ax = plt.subplots()
for t, c in zip(tats, colors):
    plt.scatter(df[df.tat == t].nodes, df[df.tat == t].edges, color=c, label=t)

ax.legend(title="TAT")
plt.title('Nodes vs. Edges')
plt.xlabel('Nodes')
plt.ylabel('Edges')
plt.show()
# ----------- How many parallel edges? -----------
print('{0:f} % have at least one parallel edge. Mean number of parallel edges that are parallel in those: {1:f}'.format(
    len(df[df.num_multiedges > 0]) / len(df) * 100, df[df.num_multiedges > 0].num_multiedges.mean()))
# ----------- Histogram Nodes -----------
# Set up the plot
ax = plt.subplot(2, 2, 1)
hist, bin_edges = np.histogram(df.nodes, bins=1000)
# plt.figure(figsize=[10, 8])
plt.bar(bin_edges[:-1], hist, color='#0504aa', alpha=0.7)
plt.xlim(min(bin_edges), max(bin_edges))
plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Nodes', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.title('Nodes', fontsize=15)
# ----------- Histogram Edges -----------
ax = plt.subplot(2, 2, 2)
hist, bin_edges = np.histogram(df.edges, bins=1000)
# plt.figure(figsize=[10, 8])
plt.bar(bin_edges[:-1], hist, color='#0504aa', alpha=0.7)
plt.xlim(min(bin_edges), max(bin_edges))
plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Edges', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.title('Edges', fontsize=15)
# ----------- Histogram Nodes/Edges ratio -----------
ax = plt.subplot(2, 2, 3)
hist, bin_edges = np.histogram(df.nodes / df.edges, bins=50000)
# plt.figure(figsize=[10, 8])
plt.bar(bin_edges[:-1], hist, color='#0504aa', alpha=0.7)
plt.xlim(min(bin_edges), max(bin_edges))
plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Nodes / Edges', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('Nodes / Edges', fontsize=15)
# ----------- Parallel edges -----------
ax = plt.subplot(2, 2, 4)
hist, bin_edges = np.histogram(df.num_multiedges, bins=10000)
# plt.figure(figsize=[10, 8])
plt.bar(bin_edges[:-1], hist, color='#0504aa', alpha=0.7)
plt.xlim(min(bin_edges), max(bin_edges))
plt.grid(axis='y', alpha=0.75)
# plt.xlabel('No of parallel edges', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('No of parallel edges', fontsize=15)
plt.show()

# ----------- Get largest connected component -----------
largest = max(nx.strongly_connected_components(G), key=len)
weakest = max(nx.weakly_connected_components(G), key=len)

# ----------- Size of largest connected component -----------
# Not implemented for directed graphs. See:
# https://stackoverflow.com/questions/47283612/networkx-node-connected-component-not-implemented-for-directed-type
# ----------- Average size of most connected component -----------
# ----------- Average shortest path length for each connected component -----------
for C in (G.subgraph(c).copy() for c in nx.strongly_connected_components(G)):
    print(nx.average_shortest_path_length(C))
# ----------- Motifs -----------
# ----------- XX -----------
for m, M in enumerate(graphs):
    print(' ')
    DG = nx.DiGraph()
    for u, v, d in M.edges(data=True):
        if DG.has_edge(u, v):
            # print('MultiEdge in graph{}'.format(m))
            print('{} {} \t {} / {} || {} / {} || {}'.format(u, v,
                                                             d['relation'], DG[u][v]['relation'],
                                                             d['extractor'], DG[u][v]['extractor'],
                                                             d['sentence'] == DG[u][v]['sentence']))
            DG[u][v]['weight'] += 1
        else:
            DG.add_edge(u, v,
                        relation=d['relation'],
                        extractor=d['extractor'],
                        sentence=d['sentence'], weight=1)

# Make MultiDiGraph into DiGraph by setting weights as number of edges
for M in graphs:
    DG = nx.DiGraph()
    for u, v in M.edges():
        if DG.has_edge(u, v):
            DG[u][v]['weight'] += 1
        else:
            DG.add_edge(u, v, weight=1)
    #
    # Draw graph weighted by number of edges between nodes
    pos = nx.spring_layout(DG)
    weights = nx.get_edge_attributes(DG, 'weight')
    weights = weights.values()
    options = {
        "node_color": "#A0CBE2",
        "edge_color": weights,
        "width": 4,
        "edge_cmap": plt.cm.Blues,
        "with_labels": False,
    }
    nx.draw(DG, pos, **options)
    edge_labels = dict([((u, v,), d['relation'])
                        for u, v, d in M.edges(data=True)])
    nx.draw_networkx_edge_labels(
        DG, pos, edge_labels=edge_labels, font_color='red')
    plt.show()

# create weighted graph from M
# G = nx.DiGraph()
for u, v in M.edges():
    if G.has_edge(u, v):
        G[u][v]['weight'] += 1
    else:
        G.add_edge(u, v, weight=1)


clustering = nx.clustering(G, weight='weight')
# --------------------- Make directed multigraph into undirected graph ---------------------------------------
G = G.to_undirected()
G = nx.Graph(G)
# --------------------- Get graph properties ---------------------------------------
# size, clustering, path lengths

# Size
G.size()
# Clustering
nx.clustering(G)
nx.average_clustering(G)
nx.generalized_degree(G)
# Path lengths
nx.non_randomness(G)
len(G.edges())
len(G.nodes())
nx.shortest_path_length(G)
# Efficiency
nx.global_efficiency(G)
nx.local_efficiency(G)

# Find parallel edges
for G in graphs:
    # For every node in graph
    for node in G.nodes():
        # We look for adjacent nodes
        for adj_node in G[node]:
            # If adjacent node has an edge to the first node
            # Or our graph have several edges from the first to the adjacent node
            if node != adj_node and node in G[adj_node] or len(G[node][adj_node]) > 1:
                # DO MAGIC!!
                print(node, adj_node)


# Construct Speech Graphs
# G = nx.read_gpickle((graph))

weights = nx.get_edge_attributes(G, 'confidence')
weights = weights.values()


# If I change the arrowstyle (to get a bigger arrowhead), the graphs are not curved anymore
node_labels = {node: node for node in G.nodes()}
options_graph = {
    "node_color": "pink",
    "node_size": 2000,
    "font_size": 18,
    "alpha": 0.9,
    "arrowsize": 20,
    "arrowstyle": "-|>",
    "labels": node_labels,
    "edge_color": "black",
    "width": 1,
    "linewidths": 1,
    "edge_cmap": plt.cm.Blues,
    # "connectionstyle" :’arc1,rad : 0.9’
}
pos = nx.spring_layout(G)
# pos = nx.circular_layout(G)
nx.draw(G, pos, **options_graph)


edge_labels = dict([((u, v,), d['relation'])
                    for u, v, d in G.edges(data=True)])
options_edge_label = {
    "edge_labels": edge_labels,
    "font_color": 'red',
    "font_size": 12
}
nx.draw_networkx_edge_labels(G, pos, **options_edge_label)
plt.axis('off')
plt.show()

# --------------------- Plot graph ---------------------------------------
pos = nx.spring_layout(G)
nx.draw(G, pos,
        edge_color='black',
        width=1,
        linewidths=1,
        node_size=500,
        node_color='pink',
        alpha=0.9,
        labels={node: node for node in G.nodes()})
edge_labels = dict([((u, v,), d['relation'])
                    for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_color='red')
plt.show(block=False)
