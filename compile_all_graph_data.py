#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  compile_all_graph_data.py
#
# Description:
#               Script to compile graph data:
#               - Basic semantic graph data: LSC, LCC, etc.
#               - Motif counts
#               - Syntactic graph data: LSC, LCC, etc. for *syntactic* graphs
#               - NLP data: Semantic coherence, on-topic score, etc.
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

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

# +++ Set Paths +++
# Input directory for graph and motif data
graph_dir = '/Users/CN/Dropbox/speech_graphs/oasis'
# Output directory for figures
output_dir = op.join(graph_dir, 'figures')

# +++ Import Data +++
# --------------------- Import graph data ---------------------------------------
graph_data = op.join(graph_dir, 'output/graph_data.csv')
df = pd.read_csv(graph_data, index_col=0)

# --------------------- Add motif counts ---------------------------------------
# If already counted and motif_counts.csv exists, imports motif count data
try:
    # Import motif count data
    motif_counts = pd.read_csv(op.join(graph_dir, 'output/motif_counts.csv'))
    # df = pd.read_csv(op.join(graph_data))
except FileNotFoundError:
    print('----- Error: Cannot find {}} -----\nIt seems motifs have not been counted yet.\nRun motifs.py to count motifs before running this cell.'.format(graph_data))

# --- Compile graphs data (basic properties and motifs) and save ---
for column in motif_counts.columns:
    df[column] = motif_counts[column]

# --------------------- Add syntactic graph data ---------------------------------------

# Import
syn = pd.read_csv(op.join(graph_dir, 'output', 'syntactic_graph_data.csv', index_col=0)
# Add to dataframe
df=df.merge(syn, how='inner', on=[
    'subj', 'tat'])


# --------------------- Add nlp measures ---------------------------------------

nlp=pd.read_csv(
    '/Users/CN/Dropbox/speech_graphs/nlp_measures/nlp_measures.csv')
# Add to dataframe
df=df.merge(nlp, how='inner', on=[
    'subj', 'tat'])

# --------------------- Write Full Dataset ---------------------------------------
# Write Full Dataset
df.to_csv(op.join(graph_dir, 'output/graph_data_all.csv'))
