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


# SemanticSpeechGraph functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs

# --------------------- Set graph path ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/oasis'
output_dir = op.join(graph_dir, 'output')

# --------------------- Import basic graph measures ---------------------------------------
oasis = pd.read_csv(op.join(output_dir, 'graph_data_normalised_avg.csv'))

# --------------------- Import syntactic graph measures ---------------------------------------
syntactic = pd.read_csv(op.join(output_dir, 'syntactic_graph_data_avg.csv'))
# Exclude subject 12
syntactic = syntactic[syntactic.subj != 12]

# --------------------- Import semantic coherence measures ---------------------------------------


# # --------------------- Save graph measures averaged across TATs ( = one datapoint per participant ) ---------------------------------------

# df['group_n'] = None
# df.group_n = df.group.cat.codes * 100
# df_avg = (df.groupby((df.subj != df.subj.shift()).cumsum())
#           .mean()
#           .reset_index(drop=True))

# df_avg['group'] = pd.Categorical(df_avg.group_n)

# df_avg.group = df_avg.group.cat.rename_categories(
#     {0: 'CON', -56: 'FEP', 100: 'CHR'})
# df_avg.group.cat.reorder_categories(
#     ['CON', 'CHR', 'FEP'], inplace=True)
# df_avg.group.value_counts()

# df.to_csv(op.join(output_dir, 'graph_data_avg.csv'))
