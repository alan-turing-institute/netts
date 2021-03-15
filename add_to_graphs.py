#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  add_to_graphs.py
#
# Description:
#               Script to add specific properties to already created semantic graphs.
#               If graphs have already been created and the extraction of simple properties
#               (like number of tokens in the transcript) was only added to the
#               speech_graph.py script after initial creation of the graphs, then this
#               script can add simple properties to the already existing graph objects.
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
# TODO: The matching of graphs and filenames needs fixing before saving the graph files. After fixing, comment in the saving line (line 99).

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

from nlp_helper_functions import expand_contractions, remove_interjections, replace_problematic_symbols, process_sent, all_tat_files, get_transcript_properties


# import operator
graph_dir = '/Users/CN/Dropbox/speech_graphs/'
data_dir = '/Users/CN/Documents/Projects/Cambridge/data'
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

for g, G in enumerate(graphs):
    file = filelist[g]
    unconnected_nodes = G.graph['unconnected_nodes']
    # --------------------- New properties ---------------------------------------
    # ++++++++ Read TAT file ++++++++
    output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/'
    filename = all_tat_files[g]
    if g < 119:
        tat_data_dir = op.join(
            data_dir, 'Kings', 'Prolific_pilot_all_transcripts')
        input_file = op.join(tat_data_dir, filename)
    else:
        genpub_data_dir = op.join(data_dir, 'Kings', 'general_public_tat')
        input_file = op.join(genpub_data_dir, filename)
    #
    #
    #
    with open(input_file, 'r') as fh:
        orig_text = fh.read()
    #
    # ------- Clean text -------
    text = replace_problematic_symbols(orig_text)  # replace ’ with '
    text = expand_contractions(text)  # expand it's to it is
    text = remove_interjections(text)  # remove Ums and Mmms
    text = text.strip()  # remove trailing and leading whitespace
    #
    # Basic Transcript Descriptors
    transcript = filename.strip('.txt')
    total_tokens, total_sentences = get_transcript_properties(text)
    # Add Graph properties
    transcript = filename.strip('.txt')
    attributes = {'transcript': transcript, 'sentences': total_sentences,
                  'tokens': total_tokens, 'unconnected_nodes': unconnected_nodes}
    G.graph.update(attributes)
    # --- Save graph ---
    # Initialize output
    output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/'
    output = op.join(output_dir, 'SpeechGraph_{0:04d}_{1}_{2}'.format(
        g, filename.strip('.txt'), str(datetime.date.today())))
    # --- Save graph object ---
    # print('Saving {}'.format(output + ".gpickle"))
    # nx.write_gpickle(G, output + ".gpickle")
