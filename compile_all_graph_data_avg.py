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
# graph_dir = '/Users/CN/Dropbox/speech_graphs/oasis'
graph_dir = sys.argv[1]

# Output directory for figures
output_figures = op.join(graph_dir, 'figures')
if not os.path.isdir(output_figures):
    print('Creating figures directory: {}'.format(output_figures))
    os.mkdir(output_figures)

output_dir = op.join(graph_dir, 'output')

# +++ Import Data +++
# --------------------- Import graph data ---------------------------------------
graph_data_norm = op.join(graph_dir, 'output/graph_data_normalised_avg.csv')
df = pd.read_csv(graph_data_norm)


# --------------------- Add syntactic graph data ---------------------------------------

# Import
syn = pd.read_csv(
    op.join(output_dir, 'syntactic_graph_data_avg.csv'))
# Add to dataframe
merged = df.merge(syn, how='left', on=[
    'subj'])


# --------------------- Add nlp measures ---------------------------------------

nlp = pd.read_csv(op.join(output_dir, 'nlp_measures_avg.csv'))
# Add to dataframe
merged = merged.merge(nlp, how='left', on=[
    'subj'])

# --------------------- Clean ---------------------------------------
merged = merged.drop(
    columns=['Unnamed: 0_x', 'Unnamed: 0.1', 'tat_x', 'Unnamed: 0_y', 'Unnamed: 0', 'tat_y', 'tat'])

merged = merged.drop(
    columns=['tat_y', 'tat'])
# --------------------- Write Full Dataset ---------------------------------------
# Write Full Dataset
merged.to_csv(op.join(output_dir, 'graph_data_all_avg.csv'))
