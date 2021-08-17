#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  cluster_graph_measures.py
#
# Description:
#               Script to describe semantic speech graphs by calculating basic
#               and advanced graph measures.
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

import re
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
from stanza.server import CoreNLPClient


import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/NLP_psychosis/code')

# load in functions required:
from basic_meas import *

# SemanticSpeechGraph functions
from compile_graphs_dataset import get_graphs, exclude_empty_graphs
from nlp_helper_functions import expand_contractions, remove_interjections, replace_problematic_symbols, remove_irrelevant_text, process_sent, get_transcript_properties, remove_duplicates, remove_bad_transcripts


# --------------------- Import filelist ---------------------------------------
# Get list of all transcripts
data_dir = '/Users/CN/Documents/Projects/Cambridge/data/oasis/'
all_transcripts = glob.glob(op.join(data_dir, '*/s46',
                                    '*pic*.txt'), recursive=True)
output_dir = op.join('/Users/CN/Dropbox/speech_graphs/oasis/output')


# ------ TAT index - pic index translation - --------------------------------------
pic_to_tat = {
    "01": "08",
    "02": "10",
    "03": "28",
    "04": "21",
    "05": "13",
    "06": "24",
    "07": "19",
    "08": "30"
}


# --------------------- Calculate semantic coherence measures ---------------------------------------

results = []
for f, file in enumerate(all_transcripts):
    # f = 21
    # f in [21, 25, 35, 41, 55, 64, 70, 71, 72, 73, 75, 90, 180, 220, 286]
    #
    file = all_transcripts[f]
    filename = file.split('/')[-1].strip('.txt')
    print('{0} \t {1}'.format(f, filename))
    # find tat index (two-digit combination from 00 to 39 after word "TAT")
    if 'oasis' in data_dir:
        # +++ For Oasis dataset +++
        # tat index is number between 'pic' and '_'
        tat = re.search('(?<=pic)\w+', file)[0].split('_')[0]
        # subject index is 7 digit combination after '_s'
        subj = filename.split('s')[1].split('_')[0]
    elif 'all_tats' in data_dir:
        # +++ For General Public dataset +++
        # tat index is two-digit combination from 00 to 39 after word "TAT"
        tat = re.search('(?<=TAT)\w+', file)[0]
        if len(tat) > 2:
            tat = tat.split('_')[0]
        # subject index is 7 digit combination before word "TAT"
        subj = file.split('-TAT')[0][-7:]
        #
    #
    #
    tat = '{0:02d}'.format(int(tat))
    tat = pic_to_tat[tat]
    #
    picfilename = op.join(
        '/Users/CN/Dropbox/speech_graphs/stimuli/ground_truth/one_sentence', 'TAT' + tat + '.txt')
    #
    # import file that contains participant's speech excerpt:
    speechfile = open(file, 'rt')
    speechtext = speechfile.read()
    speechfile.close()
    # ========= Count words with CoreNLP =========
    #  Clean text
    text = replace_problematic_symbols(speechtext)  # replace ’ with '
    text = expand_contractions(text)  # expand it's to it is
    text = remove_interjections(text)  # remove Ums and Mmms
    text = remove_irrelevant_text(text)
    text = text.strip()  # remove trailing and leading whitespace
    # Count words with CoreNLP
    with CoreNLPClient(properties={
        'annotators': 'tokenize,ssplit,pos,lemma,parse,depparse,coref,openie'
        # 'pos.model': '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/OpenIE-standalone/target/streams/$global/assemblyOption/$global/streams/assembly/8a3bd51fe5c1bb09a51f326fa358947f6dc78463_8e7f18d9ae73e8daf5ee4d4e11167e10f8827888_da39a3ee5e6b4b0d3255bfef95601890afd80709/edu/stanford/nlp/models/pos-tagger/english-bidirectional/english-bidirectional-distsim.tagger'
    }, be_quiet=True) as client:
        ex_stanza = client.annotate(text)
    n_tokens, n_sententences, _ = get_transcript_properties(text, ex_stanza)
    # ========= Count words with nltk =========
    if speechtext is not '':
        #
        # import file that contains 'ground truth' picture description:
        picfile = open(picfilename, 'rt')
        pictext = picfile.read()
        picfile.close()
        #
        # Start by removing any text inside brackets: ([...] etc)
        speechtext = remove_text_inside_brackets(speechtext)
        #
        # calculate NLP measures:
        basic_all = meas_basic(speechtext)
        # concatenate:
        result = basic_all
        #
        result = list(result)
        result.extend([n_tokens, n_sententences])
        result = [filename] + [subj] + [tat] + result
        results.append(result)


# --------------------- Make dataframe ---------------------------------------
# set spoke titles:
spoke_titles = ['No. words', 'No. sent.', 'Sent. length',
                'words', 'sentences']

df = pd.DataFrame(results, columns=['File'] + ['subj'] + ['tat'] +
                  spoke_titles
                  )

# --------------------- Clean Data ---------------------------------------

# Exclude transcripts that were not used to create graphs
# Get list of included graphs
graph_dir = '/Users/CN/Dropbox/speech_graphs/oasis'
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)
included_transcripts = [G.graph['transcript'] for G in graphs]
df = df[df['File'].isin(included_transcripts)]
# Exclude duplicated transcripts
df = df[~df.duplicated(subset=['subj', 'tat'], keep='last')]

No. words  words  subj
48.75       73.75  46.0

No. words       48.75000e+01
words           46.75000e+01
