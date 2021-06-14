#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  describe_graphs.py
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


# SemanticSpeechGraph functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs
from word_embedding_analysis import central_node_distance, adjacent_node_distance, adjacent_edge_distance

# --------------------- Set graph path ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/oasis'
# graph_dir = sys.argv[1]
# --------------------- Import graphs ---------------------------------------
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)
# --------------------- Calculate basic graph measures ---------------------------------------
df = graph_properties(graphs, filelist)

print('Imported and described {0} graphs.\n{1} subjects described {2} ± {3} pictures on average.'.format(
    df.shape[0], len(df.subj.unique()), df.subj.value_counts().mean(), round(df.subj.value_counts().std(), 2)))
df.head()

# --------------------- Calculate central node word2vec distance ---------------------------------------

df = central_node_distance(df)

# --------------------- Calculate word2vec distance between adjacent nodes (distance_mean) and between nodes seperated by 2 edges (distance_2_mean) --------------

df = adjacent_node_distance(df, graphs)

# --------------------- Calculate word2vec distance between adjacent edges (edge_distance_mean) --------------

# df = adjacent_edge_distance(df, graphs)
# TODO: Create pos hierarchy for edges (verbs first) and debug adjacent_edge_distance

# --------------------- Save graph measures ---------------------------------------
output_dir = op.join(graph_dir, 'output')
if not os.path.isdir(output_dir):
    print('Creating output directory: {}'.format(output_dir))
    os.mkdir(output_dir)

df.to_csv(op.join(output_dir, 'graph_data.csv'))

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
