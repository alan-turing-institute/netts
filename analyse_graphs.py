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
import word2vec as w2v
import gensim
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import collections
import stanza

# import operator


graph_dir = '/Users/CN/Dropbox/speech_graphs/'
# --------------------- Read several graphs ---------------------------------------
filelist = sorted(glob.glob(op.join(graph_dir, 'all_tats', '*.gpickle')))

# filelist = sorted(glob.glob(op.join(graph_dir, 'pilot', '*.gpickle')))
# filelist.extend(
#     sorted(glob.glob(op.join(graph_dir, 'general_public_tat', '*.gpickle'))))
graphs = []
for file in filelist:
    # print(f, file)
    graph = op.join(graph_dir, file)
    graphs.append(nx.read_gpickle((graph)))

# for G in graphs:
#     # Node number & Edge number
#     print('Nodes: {} \t Edges: {}'.format(len(G.nodes()), G.size()))

# --------------------- Collect properties ---------------------------------------
g_properties = []
for g, G in enumerate(graphs):
    file = filelist[g]
    # find tat index (two-digit combination from 00 to 39 after word "TAT")
    tat = re.search('(?<=TAT)\w+', file)[0]
    if len(tat) > 2:
        tat = tat.split('_')[0]
    # find subject id (7 digit combination before word "TAT")
    subj = file.split('-TAT')[0][-7:]
    # --- Get basic transcript descriptors ---
    n_words = G.graph['tokens']
    n_sents = G.graph['sentences']
    #
    # --- Get basic graph descriptors ---
    n_nodes = len(G.nodes())
    n_edges = G.size()
    n_unconnected_nodes = len(G.graph['unconnected_nodes'])
    # Get average total degree
    average_total_degree = n_edges / n_nodes
    # Get number of parallel edges
    arr = nx.to_numpy_matrix(G)
    parallel_edges = np.sum(arr >= 2)
    # LSC
    lsc = len(max(nx.strongly_connected_components(G), key=len))
    # LCC
    lcc = len(max(nx.weakly_connected_components(G), key=len))
    # Recurrence measures: L1, L2, L3
    cycles = list(nx.simple_cycles(G))
    cycle_lengths = [len(cycle) for cycle in cycles]
    # equivalent to cycle_lengths.count(1):
    L1 = len(list(nx.selfloop_edges(G)))
    L2 = cycle_lengths.count(2)
    L3 = cycle_lengths.count(3)
    # Number of weakly connected components
    sizes_weakly_conn_components = [len(c) for c in sorted(
        nx.weakly_connected_components(G), key=len, reverse=True)]
    number_weakly_conn_components = len(sizes_weakly_conn_components)
    # Degree centrality
    degree_cents = nx.degree_centrality(G)
    degree_cents = dict(sorted(degree_cents.items(),
                               key=lambda item: item[1], reverse=True))
    max_deg_cent = next(iter(degree_cents.items()))[1]
    max_deg_node = next(iter(degree_cents.items()))[0]
    #
    # Indegree centrality
    in_degree_cents = nx.in_degree_centrality(G)
    in_degree_cents = dict(sorted(in_degree_cents.items(),
                                  key=lambda item: item[1], reverse=True))
    max_indeg_cent = next(iter(in_degree_cents.items()))
    #
    # Outdegree centrality
    out_degree_cents = nx.out_degree_centrality(G)
    out_degree_cents = dict(sorted(out_degree_cents.items(),
                                   key=lambda item: item[1], reverse=True))
    max_outdeg_cent = next(iter(out_degree_cents.items()))
    #
    # Confidence measures of relations
    confidence_vals = [edge[2]['confidence']
                       for edge in G.edges(data=True) if 'confidence' in edge[2]]
    if confidence_vals == []:
        confidence_vals = np.nan
    #
    mean_confidence = np.mean(confidence_vals)
    std_confidence = np.std(confidence_vals)
    # --- Properties for undirected version of the graph (w/o self-loops or PEs) ---
    G_basic = nx.Graph(G)
    density = nx.density(G_basic)
    # Create subgraph for all connected components
    # S = [G.subgraph(s).copy() for s in sorted(
    # nx.connected_components(G), key=len, reverse=True)]
    #
    # Get only largest connected component subgraph
    s = sorted(nx.connected_components(G_basic), key=len, reverse=True)[0]
    S = G_basic.subgraph(s).copy()
    #
    diameter = nx.diameter(S)
    #
    average_shortest_path = nx.average_shortest_path_length(S)
    #
    avg_clustering = nx.average_clustering(S)
    # nx.average_degree_connectivity(G)
    # nx.average_neighbor_degree(G)
    # avg_node_conn = nx.average_node_connectivity(G)
    #
    # --- Collect Properties ---
    g_properties.append([
        subj,
        tat,
        n_words,
        n_sents,
        n_nodes,
        n_edges,
        n_unconnected_nodes,
        average_total_degree,
        parallel_edges,
        lsc,
        lcc,
        L1,
        L2,
        L3,
        sizes_weakly_conn_components,
        number_weakly_conn_components,
        max_deg_cent,
        max_deg_node,
        max_indeg_cent,
        max_outdeg_cent,
        mean_confidence,
        std_confidence,
        density,
        diameter,
        average_shortest_path,
        avg_clustering,
    ])


# --------------------- Make dataframe ---------------------------------------
df = pd.DataFrame(g_properties, columns=[
    'subj', 'tat',
    'words', 'sentences',
    'nodes', 'edges',
    'unconnected',
    'average_total_degree',
    'parallel_edges',
    'lsc', 'lcc',
    'L1', 'L2', 'L3',
    'sizes_connected_components',
    'connected_components',
    'max_degree_centrality',
    'max_degree_node',
    'max_indegree_centrality',
    'max_outdegree_centrality',
    'mean_confidence',
    'std_confidence',
    'density',
    'diameter',
    'average_shortest_path',
    'clustering',
])

df.subj = pd.Categorical(df.subj)
df.tat = pd.Categorical(df.tat)
df.tat = df.tat.cat.rename_categories({'8': '08'})
df.tat = df.tat.cat.reorder_categories(
    ['08', '10', '13', '19', '21', '24', '28', '30'])
# --------------------- Calculate central node word2vec distance ---------------------------------------
# Initialise Word2Vec model
model = w2v.load('word2vec_data/text8.bin')
# model = gensim.models.KeyedVectors.load_word2vec_format(
#     'GoogleNews-vectors-negative300.bin.gz', binary=True)
# Initialise stanza to get word lemma
# nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')
df['distance'] = np.nan
# Requires word2vec python package and word2vec binary file (setup instructions are in nlp_helper_functions.py)
fig = plt.figure(figsize=(25, 25))
n_subplots = len(df.tat.cat.categories)
n_cols_subplots = np.ceil(np.sqrt(n_subplots))
n_rows_subplots = np.ceil(n_subplots / n_cols_subplots)
tat_words = []
most_frequent_words = []
for t, tat in enumerate(df.tat.cat.categories):
    # print(tat)
    tat_words = df.query('tat == @tat').max_degree_node
    # ---- Get the most frequent word ---
    stop_words = ['the']
    filtered_words = []
    for i, words in enumerate(tat_words):
        # if len(words[0]) > 1
        for word in words.split(' '):
            filtered = []
            if word not in stop_words:
                filtered.append(word)
            all_filtered = (' ').join(filtered)
        filtered_words.append(all_filtered)
    #
    counted_words = collections.Counter(filtered_words)
    words = []
    counts = []
    for letter, count in counted_words.most_common(10):
        words.append(letter)
        counts.append(count)
    #
    irrelevant_words = ['i', 'image', 'picture', 'it']
    words = [word for word in words if word not in irrelevant_words]
    most_frequent_words.append(words[0])
    # ---- Calculate distance between to most frequent word for all words ---
    row_indices = df.index[df.tat == tat].tolist()
    # col_index = df.columns.get_indexer_for('distance')
    distance = []
    for i, current_word in enumerate(filtered_words):
        try:
            dist = model.distance(most_frequent_words[-1], current_word)
            distance.append(dist[0][2])
        except KeyError:
            print('Word is not in word2vec vocabulary: {}. Setting distance as nan.'.format(
                current_word))
            distance.append(np.nan)
    df.loc[row_indices, 'distance'] = distance
    # Plot word cloud from most frequent words
    tat_words_joined = (' ').join(words)
    ax = plt.subplot(n_rows_subplots, n_cols_subplots, t + 1)
    wordcloud = WordCloud(background_color=None,
                          mode="RGBA").generate(tat_words_joined)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('TAT' + tat, fontsize=15)
    plt.axis("off")

output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'WordClouds_Distance' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
# plt.show(block=False)
plt.show()

# =================================================================================
# ======================================= Plots ===================================
# =================================================================================

# --------------------- Degree distribution ---------------------------------------
#
degrees = []
in_degrees = []
out_degrees = []
for G in graphs:
    deg = [G.degree(n) for n in G.nodes()]
    degrees.extend(deg)
    outdeg = [G.out_degree(n) for n in G.nodes()]
    out_degrees.extend(outdeg)
    indeg = [G.in_degree(n) for n in G.nodes()]
    in_degrees.extend(indeg)

# --------------------- Raster Plot of all Graphs ---------------------------------------
# # Plot
# fig = plt.figure(figsize=(14, 9.6))
# ax = plt.subplot(1, 3, 1)
# plt.hist(degrees)
# plt.title('Degrees')
# ax = plt.subplot(1, 3, 2)
# plt.hist(in_degrees)
# plt.title('Indegrees')
# ax = plt.subplot(1, 3, 3)
# plt.hist(out_degrees)
# plt.title('Outdegrees')
# # Save figure
# output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
# output = op.join(output_dir, 'DegreeDistribution_' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show(block=False)


# fig = plt.figure(figsize=(25.6, 20))
# for g, G in enumerate(graphs):
#     ax = plt.subplot(17, 17, g + 1)
#     pos = nx.spring_layout(G)
#     plt.axis("off")
#     nx.draw_networkx_nodes(G, pos, node_size=20)
#     nx.draw_networkx_edges(G, pos, alpha=0.4)

# output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
# output = op.join(output_dir, 'GraphsRaster_' +
#                  '_{0}'.format(str(datetime.date.today())))
# plt.savefig(output)
# plt.show(block=False)

# --------------------- Word clouds ---------------------------------------
fig = plt.figure(figsize=(25, 25))

n_subplots = len(df.tat.cat.categories)
n_cols_subplots = np.ceil(np.sqrt(n_subplots))
n_rows_subplots = np.ceil(n_subplots / n_cols_subplots)
for t, tat in enumerate(df.tat.cat.categories):
    tat_words = df.query('tat == @tat').max_degree_node
    # ---- Get the most frequent word ---
    stop_words = ['the']
    filtered_words = []
    for i, words in enumerate(tat_words):
        # if len(words[0]) > 1
        for word in words.split(' '):
            filtered = []
            if word not in stop_words:
                filtered.append(word)
            all_filtered = (' ').join(filtered)
        filtered_words.append(all_filtered)
    #
    tat_words_joined = (' ').join(filtered_words)
    ax = plt.subplot(n_rows_subplots, n_cols_subplots, t + 1)
    wordcloud = WordCloud(background_color=None,
                          mode="RGBA").generate(tat_words_joined)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('TAT' + tat, fontsize=15)
    plt.axis("off")

output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'WordClouds_' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)


# ----------- Histogram -----------
# Sentences, Words, Unconnected Nodes, Average Total Degree,
fig = plt.figure(figsize=(25, 15))
# Sentences
ax = plt.subplot(2, 2, 1)
plt.hist(df.sentences)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Sentences', fontsize=15)
#
# Words
ax = plt.subplot(2, 2, 2)
plt.hist(df.words)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Words', fontsize=15)
#
# Unconnected Nodes
ax = plt.subplot(2, 2, 3)
plt.hist(df.unconnected)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Unconnected Nodes', fontsize=15)
#
# Average Total Degree
ax = plt.subplot(2, 2, 4)
plt.hist(df.average_total_degree)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Average Total Degree', fontsize=15)
#
# Save figure
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_Basics' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)


# ----------- stripplot for each TAT -----------
# Sentences, Words, Unconnected Nodes, Average Total Degree,
fig = plt.figure(figsize=(25, 9))
ax = plt.subplot(2, 2, 1)
sns.stripplot(y='sentences', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 2, 2)
sns.stripplot(y='words', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 2, 3)
sns.stripplot(y='unconnected', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 2, 4)
sns.stripplot(y='average_total_degree', x='tat',
              data=df,
              palette="colorblind",
              )

output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_TAT_Basics' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)

# ----------- Histogram -----------
# L1, L2, L3
fig = plt.figure(figsize=(25, 15))
# L1
ax = plt.subplot(2, 2, 1)
plt.hist(df.L1)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('L1', fontsize=15)
#
# L2
ax = plt.subplot(2, 2, 2)
plt.hist(df.L2)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('L2', fontsize=15)
#
# L3
ax = plt.subplot(2, 2, 3)
plt.hist(df.L3)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('L3', fontsize=15)
#
# Save figure
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_L' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)


# ----------- Histogram -----------
# Density, Diameter, Average Shortest Path, Clustering,
fig = plt.figure(figsize=(25, 15))
# Density
ax = plt.subplot(2, 2, 1)
plt.hist(df.density)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Density', fontsize=15)
#
# Diameter
ax = plt.subplot(2, 2, 2)
plt.hist(df.diameter)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Diameter', fontsize=15)
#
# Average Shortest Path
ax = plt.subplot(2, 2, 3)
plt.hist(df.average_shortest_path)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Average Shortest Path', fontsize=15)
#
# Clustering
ax = plt.subplot(2, 2, 4)
plt.hist(df.clustering)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Clustering', fontsize=15)
#
# Save figure
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_UndirectedGraphProperties' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)


# ----------- Histogram -----------
# Mean Confidence, Std Confidence, Connected Components, Max Degree Centrality, Distance
fig = plt.figure(figsize=(25, 15))
# Mean Confidence
ax = plt.subplot(2, 3, 1)
plt.hist(df.mean_confidence[~np.isnan(df.mean_confidence)])
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Mean Confidence', fontsize=15)
#
# Std Confidence
ax = plt.subplot(2, 3, 2)
plt.hist(df.std_confidence[~np.isnan(df.std_confidence)])
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Std Confidence', fontsize=15)
#
# Connected Components
ax = plt.subplot(2, 3, 3)
plt.hist(df.connected_components)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Connected Components', fontsize=15)
#
# Max Degree Centrality
ax = plt.subplot(2, 3, 4)
plt.hist(df.max_degree_centrality)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Max Degree Centrality', fontsize=15)
#
# Distance
ax = plt.subplot(2, 3, 5)
plt.hist(df.distance[~np.isnan(df.distance)])
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.title('Distance', fontsize=15)
# Save figure
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)

# ----------- stripplot for each TAT -----------
# Mean Confidence, Std Confidence, Connected Components, Max Degree Centrality, Distance
fig = plt.figure(figsize=(25, 9))
ax = plt.subplot(2, 3, 1)
sns.stripplot(y='mean_confidence', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 3, 2)
sns.stripplot(y='std_confidence', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 3, 3)
sns.stripplot(y='connected_components', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 3, 4)
sns.stripplot(y='max_degree_centrality', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 3, 5)
sns.stripplot(y='distance', x='tat',
              data=df,
              palette="colorblind",
              )
# ax.set_xticklabels(most_frequent_words)

output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_TAT_noTicks' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)

# ----------- Hist -----------
# LCC & LSC
fig = plt.figure(figsize=(25, 9))
# ---- LCC ----
# Set up the plot
ax = plt.subplot(1, 2, 1)
plt.hist(df.lcc)
plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Nodes', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.title('LCC', fontsize=15)
# ---- LSC ----
# Set up the plot
ax = plt.subplot(1, 2, 2)
plt.hist(df.lsc)
plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Nodes', fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('Frequency', fontsize=15)
plt.title('LSC', fontsize=15)
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_LCC-LSC' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)

# ----------- LCC, LSC, Nodes, Edges by TAT -----------
fig = plt.figure(figsize=(25, 9))
ax = plt.subplot(2, 2, 1)
sns.stripplot(y='lcc', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 2, 2)
sns.stripplot(y='lsc', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 2, 3)
sns.stripplot(y='nodes', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(2, 2, 4)
sns.stripplot(y='edges', x='tat',
              data=df,
              palette="colorblind",
              )
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_LCC-LSC_TAT' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)

# ----------- Plot nodes vs edges -----------
fig, ax = plt.subplots(figsize=(10, 6))
tats = df.tat.unique()
colors = cm.rainbow(np.linspace(0, 1, len(tats)))
for t, c in zip(tats, colors):
    plt.scatter(df[df.tat == t].nodes, df[df.tat == t].edges, color=c, label=t)

ax.legend(title="TAT")
plt.title('Nodes vs. Edges')
plt.xlabel('Nodes')
plt.ylabel('Edges')
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Nodes_vs_Edges' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)
# ----------- How many parallel edges? -----------
print('{0:f} % have at least one parallel edge. Mean number of parallel edges that are parallel in those: {1:f}'.format(
    len(df[df.parallel_edges > 0]) / len(df) * 100, df[df.parallel_edges > 0].parallel_edges.mean()))
# ----------- Histogram: Nodes, Edges, Node-Edge ratio, Parallel edges -----------
# Set up the plot
fig = plt.figure(figsize=(25, 9))
# Nodes
ax = plt.subplot(2, 2, 1)
plt.hist(df.nodes)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('Nodes', fontsize=15)
# Edges
ax = plt.subplot(2, 2, 2)
plt.hist(df.edges)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('Edges', fontsize=15)
# Histogram Nodes/Edges ratio
ax = plt.subplot(2, 2, 3)
plt.hist(df.nodes / df.edges)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('Nodes / Edges', fontsize=15)
# Parallel edges
ax = plt.subplot(2, 2, 4)
plt.hist(df.parallel_edges)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.title('No of parallel edges', fontsize=15)
# Save
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_LCC-LSC_TAT' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show(block=False)

tat = '21'
df.query('tat == @tat')
