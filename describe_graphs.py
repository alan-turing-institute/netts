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
from word_embedding_analysis import central_node_distance, adjacent_node_distance

# --------------------- Set graph path ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/oasis'
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

# --------------------- Calculate word2vec distance between adjacent nodes (distance_mean) --------------

df = adjacent_node_distance(df, graphs)

# --------------------- Save graph measures ---------------------------------------
output_dir = op.join(graph_dir, 'output')
if not os.path.isdir(output_dir):
    print('Creating output directory: {}'.format(output_dir))
    os.mkdir(output_dir)

df.to_csv(op.join(output_dir, 'graph_data.csv'))
