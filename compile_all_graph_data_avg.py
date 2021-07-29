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


# --------------------- Add residualised graph data ---------------------------------------

# Import
res = pd.read_csv(
    op.join(output_dir, 'graph_data_residualised_avg.csv'))

res = res[['subj', 'connected_components_res',
           'cc_size_med_res', 'cc_size_mean_res', 'max_degree_centrality_abs_res', 'max_indegree_centrality_abs_res', 'max_outdegree_centrality_abs_res']]

merged = df.merge(res, how='left', on=[
    'subj'])

# --------------------- Add syntactic graph data ---------------------------------------

# Import
syn = pd.read_csv(
    op.join(output_dir, 'syntactic_graph_data_avg.csv'))

# syn = syn[syn.subj != 12]
# Add to dataframe
merged = merged.merge(syn, how='left', on=[
    'subj'])


# --------------------- Add nlp measures ---------------------------------------

nlp = pd.read_csv(op.join(output_dir, 'nlp_measures_avg.csv'))
# nlp = nlp[nlp.subj != 12]

# Add to dataframe
merged = merged.merge(nlp, how='left', on=[
    'subj'])

# --------------------- Clean ---------------------------------------
merged = merged.drop(
    columns=['Unnamed: 0_x', 'tat_x', 'Unnamed: 0_y', 'Unnamed: 0', 'tat_y'])

merged = merged.drop(
    columns=['Unnamed: 0.1_y'])  # Unnamed: 0.1_x'
merged = merged.drop(
    columns=['Unnamed: 0.1_x'])  #
# --------------------- Write Full Dataset ---------------------------------------
# Write Full Dataset
merged.to_csv(op.join(output_dir, 'graph_data_all_avg.csv'))
