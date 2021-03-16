#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  graph_tats.sh
#
# Description:  Script to construct speech graphs for batch of TAT transcripts
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

## Navigate to working directory
cd /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/

# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
# Usage: python ./speech_graph.py 3
#        tat=3; python -u ./speech_graph.py ${tat} > figures/SpeechGraph_log_${tat}_`date +%F` # (pipe output to text file)
# ------------------------------------------------------------------------------B
# for tat in `seq -s ' ' 0 118`; do
# 25 28 30 44

# for tat in `seq -s ' ' 51 175`; do
#     n=$(( tat + 119))
#     python -u ./speech_graph.py ${tat} \
#     > /Users/CN/Dropbox/speech_graphs/general_public_tat/SpeechGraph_`zeropad ${n} 4`_`date +%F`.txt 2>&1 # (pipe output and error msgs to text file)
# done
# 295
for tat in `seq -s ' ' 0 294`; do
    n=$(( tat ))
    python -u ./speech_graph.py ${tat} \
    > /Users/CN/Dropbox/speech_graphs/all_tats/SpeechGraph_`zeropad ${n} 4`_`date +%F`.txt 2>&1 # (pipe output and error msgs to text file)
done



# Confirm all tats are processed
ls /Users/CN/Dropbox/speech_graphs/all_tats/*.txt |wc

for i in /Users/CN/Dropbox/speech_graphs/all_tats/*.txt; do
    sed -n '/^++++ Obtained unconnected nodes/,/^++++ Cleaned parallel edges from duplicates/p' $i
done

# TODO: 3143876-TAT24 has adjective edges ('sad person') that are not getting extracted. Why?
