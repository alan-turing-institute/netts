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
25 28 30 44

for tat in 25 28 30 44 ; do
    python -u ./speech_graph.py ${tat} \
    > /Users/CN/Dropbox/speech_graphs/SpeechGraph_`zeropad ${tat} 4`_`date +%F`.txt 2>&1 # (pipe output and error msgs to text file)
done


# for i in SpeechGraph_*_2021-01-14*; do
#     new=${i%*_2021*}
#     new=${new#*SpeechGraph_*}
#     echo mv $i SpeechGraph_`zeropad ${new} 4`${i#*SpeechGraph_*}
# done