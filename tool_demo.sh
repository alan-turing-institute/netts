#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  graph_tats.sh
#
# Description:  Script to construct speech graphs for batch of TAT transcripts
#
# Author:       Caroline Nettekoven, 2021
#
# Usage:        python ./speech_graph.py 3
#               To pipe output to text file
#               tat=3; python -u ./speech_graph.py ${tat} > figures/SpeechGraph_log_${tat}_`date +%F`
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
## Navigate to working directory
cd /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/
# ========================== Process single transcript ====================================================================

# --- Process transcripts as described in README --------------------------------------------
python -u ./speech_graph.py 30

# --- Process transcripts and pipe output to txt file --------------------------------------------
transcript_no = 30
output_dir=/Users/CN/Dropbox/speech_graphs/tool_demo
python -u ./speech_graph.py ${transcript_no} > ${output_dir}/SpeechGraph_`zeropad ${transcript_no} 4`_`date +%F`.txt 2>&1 # (pipe output and error msgs to text file)