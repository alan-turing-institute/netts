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
from compile_graphs_dataset import get_graphs, graph_properties
from graph_analysis_functions import print_bidirectional_edges, print_parallel_edges, get_parallel_edges, central_words, calc_vector_distance, calc_vector_distance_all


# --------------------- Import graphs ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'

graphs, filelist = get_graphs(graph_dir)
df = graph_properties(graphs, filelist)


# --------------------- Calculate central node word2vec distance ---------------------------------------
df['distance_mean'] = np.nan
# Initialise Word2Vec model
model = w2v.load('word2vec_data/text8.bin')
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos')
for g, G in enumerate(graphs):
    # ---- Calculate distance between all adjacent nodes in graph ---
    distance = calc_vector_distance_all(G, model, nlp, quiet=False)
    df['distance_mean'][g] = distance

for G in graphs:
    edges = G.edges()
for edge in edges:
    edge = choose_representative_word(edge, nlp, quiet=False)
# TODO Continue here tomorrow
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
plt.show(block=False)

import stanza


print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')
