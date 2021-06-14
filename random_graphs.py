#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  random_graphs.py
#
# Description:
#               Script to create random graphs
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

import glob
import os
import os.path as op
import sys

from seaborn.palettes import color_palette
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
import scipy


# SemanticSpeechGraph functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs, graph_properties_undirected
# --------------------- Import graphs for which to generate random graphs ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/oasis'
output_figures = op.join(graph_dir, 'figures')

graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)
df = graph_properties(graphs, filelist)

print('Imported and described {0} graphs.\n{1} subjects described {2} ± {3} pictures on average.'.format(
    df.shape[0], len(df.subj.unique()), df.subj.value_counts().mean(), round(df.subj.value_counts().std(), 2)))
df.head()

# --------------------- Find appropriate number of random graphs where graph measures converge ---------------------------------------
# Select largest and smallest graphs (according to number of nodes and number of edges) and one graph each in the middle
# df_sorted = df
# df_sorted['graph'] = graphs
# # Select largest, middle and smallest graphs (according to number of nodes)
# df_sorted.sort_values(by=['nodes'], ascending=[
#                       False], inplace=True, ignore_index=True)
# graph_sizes_selection = [df_sorted.graph.values[0],
#                    df_sorted.graph.values[round(len(df_sorted) / 2)], df_sorted.graph.values[-1]]
# # Select largest, middle and smallest graphs (according to number of edges)
# df_sorted.sort_values(by=['edges'], ascending=[
#                       False], inplace=True, ignore_index=True)
# graph_sizes_selection.extend([df_sorted.graph.values[0],
#                         df_sorted.graph.values[round(len(df_sorted) / 2)], df_sorted.graph.values[-1]])

graph_sizes = [(len(list(G.nodes())), len(list(G.edges()))) for G in graphs]
unique_graph_sizes = list(dict.fromkeys(graph_sizes))

# Choose largest and smallest by node
unique_graph_sizes.sort(key=lambda x: x[0])
graph_sizes_selection = [unique_graph_sizes[0], unique_graph_sizes[round(
    len(unique_graph_sizes) / 2)], unique_graph_sizes[-1]]

# Choose largest and smallest by edge
unique_graph_sizes.sort(key=lambda x: x[1])
graph_sizes_selection.extend([unique_graph_sizes[0], unique_graph_sizes[round(
    len(unique_graph_sizes) / 2)], unique_graph_sizes[-1]])


# Create different number of random graphs for this sample of graph sizes
# steps = [10, 50]
steps = [10, 20, 40, 80, 100, 150, 200, 250, 400]
list_of_dataframes = []
for number_of_nodes, number_of_edges in graph_sizes_selection:
    for step in steps:
        random_graphs = []
        for i in range(0, step):
            random_graphs.append(nx.gnm_random_graph(
                n=number_of_nodes, m=number_of_edges))
        #
        # Collect properties of random graphs
        random_graph_properties = graph_properties_undirected(random_graphs)
        random_graph_properties['step'] = step
        list_of_dataframes.append(random_graph_properties)

random_graph_data = pd.concat(list_of_dataframes)

# --------------------- Plot where graph measures converge ---------------------------------------
# Plot convergence
measures_of_interest = list(random_graph_data.columns)[2:-1]

# for variable in measures_of_interest:
fig = plt.figure(figsize=(25, 10))
for v, variable in enumerate(measures_of_interest):
    #
    ax = plt.subplot(2, np.ceil(len(measures_of_interest) / 2), v + 1)
    sns.lineplot(
        data=random_graph_data,
        x="step", y=variable, hue="nodes", style="nodes",
        markers=True, dashes=False, palette="husl"
    )
    plt.title(variable)

output = op.join(output_figures, 'RandomGraphs_Steps_nodeswise')
plt.savefig(output)
plt.show()


# for variable in measures_of_interest:
fig = plt.figure(figsize=(25, 10))
for v, variable in enumerate(measures_of_interest):
    #
    ax = plt.subplot(2, np.ceil(len(measures_of_interest) / 2), v + 1)
    sns.lineplot(
        data=random_graph_data,
        x="step", y=variable, hue="edges", style="edges",
        markers=True, dashes=False, palette="husl"
    )
    plt.title(variable)

output = op.join(output_figures, 'RandomGraphs_Steps_edgewise')
plt.savefig(output)
plt.show()


# --------------------- Generate undirected random graphs for all graph sizes in dataset ---------------------------------------

no_random_graphs = 100
list_of_dataframes = []
for number_of_nodes, number_of_edges in unique_graph_sizes:
    random_graphs = []
    for i in range(0, no_random_graphs):
        random_graphs.append(nx.gnm_random_graph(
            n=number_of_nodes, m=number_of_edges))
    #
    # Collect properties of random graphs
    random_graph_properties = graph_properties_undirected(random_graphs)
    random_graph_properties['no_random_graphs'] = no_random_graphs
    # Add random graphs to dataframe
    random_graph_properties['graph'] = random_graphs
    list_of_dataframes.append(random_graph_properties)

random_graph_data = pd.concat(list_of_dataframes)

# --------------------- Normalise actual measures by random graph measures ---------------------------------------
measures_of_interest = list(random_graph_data.columns)[2:-2]

# Loop through measures of interest
for v, variable in enumerate(measures_of_interest):
    df[variable + '_normF'] = None
    df[variable + '_normZ'] = None
    for number_of_nodes, number_of_edges in unique_graph_sizes:
        # Calculate mean and std deviation for graph measures of random networks
        mean_random = random_graph_data.query(
            'nodes == @number_of_nodes & edges == @number_of_edges')[variable].mean()
        std_random = random_graph_data.query(
            'nodes == @number_of_nodes & edges == @number_of_edges')[variable].std()
        # Normalise dataset values by mean or mean and std deviation of random network values
        values_normF = df.query(
            'nodes == @number_of_nodes & edges == @number_of_edges')[variable] / mean_random
        values_normZ = (df.query(
            'nodes == @number_of_nodes & edges == @number_of_edges')[variable] - mean_random) / std_random
        # Add normalised values to dataframe
        df.loc[df.eval(
            'nodes == @number_of_nodes & edges == @number_of_edges'), variable + '_normF'] = values_normF
        df.loc[df.eval(
            'nodes == @number_of_nodes & edges == @number_of_edges'), variable + '_normZ'] = values_normZ
    #
    df[variable + '_normF'] = df[variable + '_normF'].astype('float')
    df[variable + '_normZ'] = df[variable + '_normZ'].astype('float')

# --------------------- Average across tats ---------------------------------------
# Make subj and tat categorical
df.subj = pd.Categorical(df.subj.astype('str'))
df.tat = pd.Categorical(df.tat.astype('str'))


id_data = pd.read_csv(
    '/Users/CN/Documents/Projects/Cambridge/data/oasis/ids_oasis.csv', delimiter=';')
df['group'] = np.nan
for s, subj in enumerate(id_data.Subject):
    df.at[df.subj == str(subj), 'group'] = id_data.Group[s]

df.group = pd.Categorical(df.group.astype('str'))
df.group = df.group.cat.rename_categories({'ARMS': 'CHR'})

df.group = df.group.cat.reorder_categories(
    ['CON', 'CHR', 'FEP'])

print('--- Groups ---\n{}'.format(df.group.value_counts()))

# Exclude subject 12 because of bad quality transcripts
df.shape
df = df[df.subj.values != '12']
#  Average across TAT stimuli ( = one datapoint per participant )
df['group_n'] = None
df.group_n = df.group.cat.codes * 100
oasis_avg = (df.groupby((df.subj != df.subj.shift()).cumsum())
             .mean()
             .reset_index(drop=True))

oasis_avg['group'] = pd.Categorical(oasis_avg.group_n)

oasis_avg.group = oasis_avg.group.cat.rename_categories(
    {0: 'CON', -56: 'FEP', 100: 'CHR'})
oasis_avg.group.cat.reorder_categories(
    ['CON', 'CHR', 'FEP'], inplace=True)
oasis_avg.group.value_counts()

# --------------------- Compare groups ---------------------------------------

variable_list = ['clustering_normF', 'clustering_normZ', 'max_degree_centrality_normF',
                 'max_degree_centrality_normZ', 'density_normF', 'density_normZ',
                 'diameter_normF', 'diameter_normZ', 'average_shortest_path_normF',
                 'average_shortest_path_normZ']

group_comparisons = [('CON', 'FEP'), ('CON', 'CHR'), ('CHR', 'FEP')]

fig = plt.figure(figsize=(25, 14))
for v, variable in enumerate(variable_list):
    ax = plt.subplot(2, np.ceil(len(variable_list) / 2), v + 1)
    sns.boxplot(y=variable, x='group',
                data=oasis_avg,
                palette="colorblind",
                )
    results_mwu = []
    results_ttest = []
    stats_summary = ''
    for c, comb in enumerate(group_comparisons):
        a = oasis_avg.query('group == @comb[0]')[variable]
        b = oasis_avg.query('group == @comb[1]')[variable]
        results_mwu.append(scipy.stats.mannwhitneyu(a, b))
        results_ttest.append(scipy.stats.ttest_ind(a, b))
        # print('{0} vs. {1} {2} ({3})'.format(comb[0], comb[1], round(results_mwu[c][0],8), round(results_mwu[c][1],8) ))
        if results_mwu[c][1] < 0.001:
            symbol = '***'
        elif results_mwu[c][1] < 0.01:
            symbol = '**'
        elif results_mwu[c][1] < 0.05:
            symbol = '*'
        else:
            symbol = ''
        stats_summary = stats_summary + '{0} vs. {1} {2} ({3}){4}\n'.format(
            comb[0], comb[1], round(results_mwu[c][0], 8), round(results_mwu[c][1], 8), symbol)
    plt.title(stats_summary)

plt.subplots_adjust(hspace=0.4)
output = op.join(output_figures, 'Hist_normalised_' +
                 '_{}'.format('_'.join(variable_list), str(datetime.date.today())))
plt.savefig(output)
plt.show()
