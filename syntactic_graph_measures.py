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
#               PDF of tool documentation (which includes description of the params_table.txt
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
import re
import os
import os.path as op
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')

# Data Processing
import pandas as pd

# Graph functions
from compile_graphs_dataset import get_graphs, exclude_empty_graphs

# --------------------- Move syntactic graph measure tables to common folder and rename ---------------------------------------
project = 'oasis'  # project = 'all_tats'
orig_path = '/Users/CN/Documents/Projects/Cambridge/data/oasis/TLI_1_min_disfluencies/'
syntactic_data_path = op.join(
    '/Users/CN/Dropbox/speech_graphs/', project, 'output/syntactic_measures')

all_raw_files = sorted(glob.glob(op.join(orig_path,
                                         '*/*table*.txt')))

for n, orig_file in enumerate(all_raw_files):
    # Move files in individual subject folders into common folder and enumerate files
    os.rename(orig_file, op.join(syntactic_data_path, '{}_{}.txt'.format(
        orig_file.split('/')[-1].split('.txt')[0], n + 1)))

# Important: Find the file that has the header information in the first line and rename it to end in _0, so that it gets fed in first and the header information gets stored
# --------------------- Import syntactic graph measures ---------------------------------------
# ++++ Import hub info ++++
# Find all hub files
all_files = sorted(glob.glob(op.join(syntactic_data_path,
                                     'hub_table_dir*.txt')))

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
all_files = sorted(glob.glob(op.join(syntactic_data_path,
                                     'params_table*')))

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
graph_dir = op.join('/Users/CN/Dropbox/speech_graphs/', project)

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
# Change columns names to differentiate syntactic graph measures from semantic graph measures
params.columns = 'syn_' + params.columns
hub.columns = 'syn_' + hub.columns

# +++ Add subject and tat info +++
hub['subj'] = None
hub['tat'] = None
# Add subject and tat info to merge on later
for f, file in enumerate(hub.syn_File):
    if 'oasis' in project:
        # +++ For Oasis dataset +++
        # tat index is number between 'pic' and '_'
        tat = re.search('(?<=pic)\w+', file)[0].split('_')[0]
        # subject index is 7 digit combination after '_s'
        subj = file.split('s')[1].split('_')[0]
    elif 'all_tats' in project:
        # +++ For General Public dataset +++
        # tat index is two-digit combination from 00 to 39 after word "TAT"
        tat = re.search('(?<=TAT)\w+', file)[0]
        if len(tat) > 2:
            tat = tat.split('_')[0]
        # subject index is 7 digit combination before word "TAT"
        subj = file.split('-TAT')[0][-7:]
    # Assign value to variable in subject row
    hub['subj'][f] = int(subj)
    hub['tat'][f] = int(tat)

params['subj'] = None
params['tat'] = None
# Add subject and tat info to merge on later
for f, file in enumerate(params.syn_File):
    if 'oasis' in project:
        # +++ For Oasis dataset +++
        # tat index is number between 'pic' and '_'
        tat = re.search('(?<=pic)\w+', file)[0].split('_')[0]
        # subject index is 7 digit combination after '_s'
        subj = file.split('s')[1].split('_')[0]
    elif 'all_tats' in project:
        # +++ For General Public dataset +++
        # tat index is two-digit combination from 00 to 39 after word "TAT"
        tat = re.search('(?<=TAT)\w+', file)[0]
        if len(tat) > 2:
            tat = tat.split('_')[0]
        # subject index is 7 digit combination before word "TAT"
        subj = file.split('-TAT')[0][-7:]
    # Assign value to variable in subject row
    params['subj'][f] = int(subj)
    params['tat'][f] = int(tat)

syntactic_data = pd.merge(params, hub, how='left', on=[
                          'subj', 'tat', 'syn_File'])


syntactic_data.subj = pd.Categorical(syntactic_data.subj.astype('str'))
syntactic_data.tat = pd.Categorical(syntactic_data.tat.astype('str'))

if 'all_tats' in file:
    # +++ For General Public dataset +++
    syntactic_data.tat = syntactic_data.tat.cat.rename_categories({'8': '08'})
    syntactic_data.tat = syntactic_data.tat.cat.reorder_categories(
        ['08', '10', '13', '19', '21', '24', '28', '30'])

# --------------------- Save syntactic graph measures ---------------------------------------
syntactic_data.to_csv(op.join(graph_dir, 'output/syntactic_graph_data.csv'))

# --------------------- Save syntactic graph measures averaged across pictures (i.e. TATs) ---------------------------------------
# Make numeric columns numeric
syntactic_data.dtypes
non_numeric_cols = ['syn_File', 'subj', 'tat',
                    'syn_Hub', 'syn_2nd Hub', 'syn_Pair',
                    'syn_LSCHub']
numeric_cols = [
    col for col in syntactic_data.columns if col not in non_numeric_cols]
for col in numeric_cols:
    syntactic_data[col] = syntactic_data[col].astype('float64')

syntactic_data_avg = (syntactic_data.groupby((syntactic_data.subj != syntactic_data.subj.shift()).cumsum())
                      .mean()
                      .reset_index())

syntactic_data_avg.to_csv(
    op.join(graph_dir, 'output/syntactic_graph_data_avg.csv'))
