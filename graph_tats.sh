#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  graph_tats.sh
#
# Description:  Script to construct speech graphs for batch of TAT transcripts
#
# Author:       Caroline Nettekoven, 2021
#
# TODO: 3143876-TAT24 has adjective edges ('sad person') that are not getting extracted. Why?
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
## Navigate to working directory
cd /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/
# Usage: python ./speech_graph.py 3
#        tat=3; python -u ./speech_graph.py ${tat} > figures/SpeechGraph_log_${tat}_`date +%F` # (pipe output to text file)

# ========================== Process transcripts ==========================
first_tat=1000
last_tat=2699
output_dir=/Users/CN/Dropbox/speech_graphs/all_tats
# ------------------------------------------------------------------------------
for tat in `seq -s ' ' ${first_tat} ${last_tat}`; do
    echo "Processing transcript ${tat}..."
    python -u ./speech_graph.py ${tat} \
    > ${output_dir}/SpeechGraph_`zeropad ${tat} 4`_`date +%F`.txt 2>&1 # (pipe output and error msgs to text file)
done

# ========================== Compile report ==========================
output_dir=${output_dir}/
rm ${output_dir}/report

# Count errors
errors=0
for tat in ${output_dir}/*.txt; do
    finished_without_error=`cat ${tat} | grep "finished in"`
    if [ $? != 0 ]; then
        errors=$(( errors+1))
    fi
done

# Print summary message
printf "Your computing job has finished, wohoooo! \n\nTats ${first_tat} to ${last_tat} have been processed. \n------------------------------------------\nProcessed: \t$(( last_tat - first_tat ))\nErrors: \t\t${errors}\n" > ${output_dir}/report

# Print error messages
for tat in ${output_dir}/*.txt; do
    finished_without_error=`cat ${tat} | grep "finished in"`
    if [ $? != 0 ]; then
        msg=`tail ${tat}`
        printf  '\n------------------ Error in %s ------------------\n %s \n' "$tat" "$msg" >> ${output_dir}/report
    fi
done

# ========================== Send notification email ==========================
# Send short email:
# printf "Your computing job has finished, wohoooo! \n\nTats ${first_tat} to ${last_tat} have been processed. \n------------------------------------------\nProcessed: \t$(( last_tat - first_tat ))\nErrors: \t\t${errors}\n" | mail -s "SURPRISE SHAWTY" cnettekoven@web.de

# Send email with error report:
cat ${output_dir}/report | mail -s "SURPRISE SHAWTY" cnettekoven@web.de

