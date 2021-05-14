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

import warnings
warnings.filterwarnings("ignore")
import glob
import os
import os.path as op
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')

# Plotting
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

# Data Processing
import numpy as np
import pandas as pd
import datetime
import re
import word2vec as w2v
import gensim
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import collections
import networkx as nx
from stanza.server import CoreNLPClient


# SemanticSpeechGraph functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs
from graph_analysis_functions import print_bidirectional_edges, print_parallel_edges, get_parallel_edges, central_words, calc_vector_distance, calc_vector_distance_adj, choose_representative_word, find_representative_node_words
# --------------------- Import graphs ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'

graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)
df = graph_properties(graphs, filelist)

print('Imported and described {0} graphs.\n{1} subjects described {2} ± {3} pictures on average.'.format(
    df.shape[0], len(df.subj.unique()), df.subj.value_counts().mean(), round(df.subj.value_counts().std(), 2)))
df.head()

# --------------------- Calculate central node word2vec distance ---------------------------------------
df['distance'] = np.nan
frequent_words = []
# Initialise Word2Vec model
model = w2v.load('word2vec_data/text8.bin')
for tat in df.tat.cat.categories:
    most_frequent_word, tat_words_filtered = central_words(df, tat)
    frequent_words.append(most_frequent_word)
    # ---- Calculate distance between to most frequent word for all words ---
    distance = calc_vector_distance(
        most_frequent_word, tat_words_filtered, model)
    row_indices = df.index[df.tat == tat].tolist()
    df.loc[row_indices, 'distance'] = distance


# --------------------- Calculate word2vec distance between adjacent nodes (distance_mean) --------------
df['distance_mean'] = np.nan
# # Initialise Word2Vec model
model = w2v.load('word2vec_data/text8.bin')
#
# --- Find representative word in every node ---
# concatenate node words of every graph, with graphs seperated by \n\n to be split into seperate sentences by CoreNLP


nodes_allGraphs = ''
for G in graphs:
    nodes = list(G.nodes())
    nodes = (' ').join(nodes)
    nodes_allGraphs = nodes_allGraphs + nodes + '\n\n'

# --- Annotate node words ---
# Split concatenated nodes into chunks that are manageable by CoreNLP (of max 10000 characters length) while respecting graph boundaries (marked by '\n\n')
# Step size is chosen somewhat arbitrarily. For our data, the concatenated node labels of 950 graphs are 10000 characters long.
# To be on the safe side, we chose to concatenate the nodes of 500 graphs in each step.
# The concatenated node labels of a 500-graph dataset should be well below the character limit of 10000 characters that CoreNLP can handle.
step = 500
all_sentences = []
for i in range(0, len(nodes_allGraphs.split('\n\n')), step):
    # print(i, i+step)
    process_nodes = '\n\n'.join(nodes_allGraphs.split('\n\n')[i:i + step])
    # part-of-speech tag node words
    with CoreNLPClient(properties={'annotators': 'tokenize,ssplit,pos,lemma', 'ssplit.newlineIsSentenceBreak': 'two'}, be_quiet=False) as client:
        doc = client.annotate(process_nodes)
    #
    for sent in doc.sentence:
        all_sentences.append(sent)


# Get dictionary with one representative words for every node entry on the basis of pos tags
representative_node_words = find_representative_node_words(
    graphs, all_sentences, quiet=False)

# ---- Calculate distance between all adjacent nodes in graph ---
for g, G in enumerate(graphs):
    distance = calc_vector_distance_adj(
        G, model, representative_node_words, quiet=False)
    df['distance_mean'][g] = distance


# ----------- Plot -----------
fig = plt.figure(figsize=(25, 9))
plt.suptitle('Mean word2vec distance of all adjacent nodes', fontsize=15)
ax = plt.subplot(1, 2, 1)
sns.stripplot(y='distance_mean', x='tat',
              data=df,
              palette="colorblind",
              )
ax = plt.subplot(1, 2, 2)
plt.hist(df.distance_mean, bins=100)
plt.grid(axis='y', alpha=0.75)
plt.ylabel('Frequency', fontsize=15)
plt.xticks(fontsize=15)
output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/figures/'
output = op.join(output_dir, 'Hist_all_vector_distances' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()
