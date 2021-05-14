#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  syntactic_graph_measures.py
#
# Description:
#               Script to import graph descriptions of syntactic speech graphs.
#
#               Syntactic speech graphs are constructed in line with
#               1) Mota, N.B., Furtado, R., Maia, P.P.C., Copelli, M. & Ribeiro, S.
#                  Graph analysis of dream reports is especially informative about
#                  psychosis. Sci. Rep. 4, 3691; DOI:10.1038/srep03691 (2014)
#               2) Mota NB, et al. (2012) Speech Graphs Provide a Quantitative
#                  Measure of Thought Disorder in Psychosis. PLoS ONE 7(4): e34928.
#                  doi: 10.1371 / journal.pone.0034928
#
#               Syntactic graph measures were calculated using the SpeechGraphs program
#               to create and describe syntactic graphs from the transcript data (saved
#               as params_table.txt)
#               Tool is available here: https://neuro.ufrn.br/_tools/speechgraph/
#               Tool documentation: http://www.neuro.ufrn.br/softwares/speechgraphs
#               PDF of tool documentation (which description of the params_table.txt
#               column names): https://neuro.ufrn.br/_pdf/SpeechGraphs_UserGuide.pdf
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

# Data Processing
import pandas as pd
import numpy as np

# Graph functions
from compile_graphs_dataset import get_graphs, exclude_empty_graphs


# --------------------- Import syntactic graph measures ---------------------------------------
# ++++ Import hub info ++++
# Find all hub files
syntactic_data_path = '/Users/CN/Documents/Projects/Cambridge/data/Kings'
all_files = glob.glob(op.join(syntactic_data_path, '**',
                              'hub_table_dir.txt'), recursive=True)

# Import the hub table file that includes a header first
hub = pd.read_csv(all_files[0])

# Import the hub table files that include no header
list_of_datamframes_hub = [hub]
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=None)
    df.columns = hub.columns
    list_of_datamframes_hub.append(df)

hub = pd.concat(list_of_datamframes_hub, axis=0, ignore_index=True)


# ++++ Import params info ++++
# Find all params files
all_files = glob.glob(op.join(syntactic_data_path, '**',
                              'params_table.txt'), recursive=True)

# Import the params table file that includes a header first
params = pd.read_csv(all_files[0])

# Import the params table files that include no header
list_of_datamframes_params = [params]
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=None)
    df.columns = params.columns
    list_of_datamframes_params.append(df)

params = pd.concat(list_of_datamframes_params, axis=0, ignore_index=True)

# --------------------- Clean data ---------------------------------------
# Remove data from excluded graphs
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'

# Get list of included graphs
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)
transcripts = [G.graph['transcript'] for G in graphs]

# Keep only measures for included graphs
params = params[params['File'].isin(transcripts)]
hub = hub[hub['File'].isin(transcripts)]

# Remove duplicate rows of the same graphs (same transcripts appearing in several folders)
hub = hub[~hub.duplicated(subset=['File'], keep='last')]
params = params[~params.duplicated(subset=['File'], keep='last')]

# Reset and drop index
hub = hub.reset_index(drop=True)
params = params.reset_index(drop=True)

# Import other graphs data
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graph_data = pd.read_csv(op.join(graph_dir, 'output/graph_data.csv'))

# Change columns names to differentiate syntactic graph measures from semantic graph measures
params.columns = 'syn_' + params.columns
hub.columns = 'syn_' + hub.columns

# +++ Add subject and tat info +++
hub['subj'] = None
hub['tat'] = None
# Add subject and tat info to merge on later
for f, file in enumerate(hub.syn_File):
    # find tat index (two-digit combination from 00 to 39 after word "TAT")
    tat = re.search('(?<=TAT)\w+', file)[0]
    if len(tat) > 2:
        tat = tat.split('_')[0]
    # find subject id (7 digit combination before word "TAT")
    subj = file.split('-TAT')[0][-7:]
    # Assign value to variable in subject row
    hub['subj'][f] = int(subj)
    hub['tat'][f] = int(tat)

params['subj'] = None
params['tat'] = None
# Add subject and tat info to merge on later
for f, file in enumerate(params.syn_File):
    # find tat index (two-digit combination from 00 to 39 after word "TAT")
    tat = re.search('(?<=TAT)\w+', file)[0]
    if len(tat) > 2:
        tat = tat.split('_')[0]
    # find subject id (7 digit combination before word "TAT")
    subj = file.split('-TAT')[0][-7:]
    # Assign value to variable in subject row
    params['subj'][f] = int(subj)
    params['tat'][f] = int(tat)


syntactic_data = pd.merge(params, hub, how='left', on=[
                          'subj', 'tat', 'syn_File'])

# --------------------- Save syntactic graph measures ---------------------------------------
syntactic_data.to_csv(op.join(graph_dir, 'output/syntactic_graph_data.csv'))
