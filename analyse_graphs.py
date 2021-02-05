#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  speech_graph.py
#
# Description:
#               Script to visualise sentence using OpenIE5 and Stanford CoreNLP
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
# Usage: python ./speech_graph.py 3
#        tat=3; python -u ./speech_graph.py ${tat} > figures/SpeechGraph_log_${tat}_`date +%F` # (pipe graph to text file)
# TO DO
#   - Sanity check: Is each relation represented only once in the edge? (Also check parallel edges in multiedge graph)
#   - Plot graphs coloured by confidence / extraction type

# ------------------------------------------------------------------------------
#
#                                               EXAMPLE TRANSCRIPTS
#                                               ===================
# Property                                  Topic                                       Index       Name
# ________________________________________________________________________________________________________________
# ambiguous coreferencing:                  (two women)                                 0       3138838-TAT10
# ambiguous coreferencing:                  (four men lying on field)                   1       3138838-TAT13
# clear text and very connected network:    (man wearing jacket, hat and hoodie)        2       3138838-TAT30
# network as one long, connected line       (women and child at home)                   3       3138849-TAT10

# many synonyms for picture:                (picture, photograph, photo)                10      3138883-TAT30
# many adjectives:                          (picture, photograph, photo)                11      3138910-TAT24

# many adjectives:                          (snowy day)                                 41      3145067-TAT30
# many self-references                      (history major)                             8       3138883-TAT13
# faulty transcript                         (clasped hands)                             9       3138883-TAT24


import networkx as nx
import os
import os.path as op
import pandas as pd
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
import matplotlib.pyplot as plt
import datetime
import glob

graph_dir = '/Users/CN/Dropbox/speech_graphs/'
# ------------------------------------------------------------------------------
# Index file
selected_file = 1
graph = op.join(graph_dir, 'SpeechGraph_{0:04d}_{1}'.format(
    selected_file, str(datetime.date.today())))
G = nx.read_gpickle((graph + ".gpickle"))
# --------------------- Read several graphs ---------------------------------------
filelist = sorted(glob.glob(graph_dir + '*.gpickle'))
graphs = []
for filename in filelist:
    # print(f, filename)
    graph = op.join(graph_dir, filename)
    graphs.append(nx.read_gpickle((graph)))

for G in graphs:
    # Node number & Edge number
    print('Nodes: {} \t Edges: {}'.format(len(G.nodes()), G.size()))

g_properties = []
for G in graphs:
    n_nodes = len(G.nodes())
    n_edges = G.size()
    G = nx.DiGraph(G)
    # nx.clustering(G)
    avg_clustering = nx.average_clustering(G)
    # nx.average_degree_connectivity(G)
    # nx.average_neighbor_degree(G)
    avg_node_conn = nx.average_node_connectivity(G)
    g_properties.append([
        n_nodes,
        n_edges,
        avg_clustering,
        avg_node_conn
    ])

df = pd.DataFrame(g_properties, columns=[
    'nodes', 'edges', 'cc',
    'node_conn'])

plt.scatter(df.nodes, df.edges, c="g", alpha=0.5,
            label="Luck")
df.describe(include='all')

# length = nx.all_pairs_shortest_path_length(G)

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
