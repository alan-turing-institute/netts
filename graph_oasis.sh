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
# Set output directory
output_dir=/Users/CN/Dropbox/speech_graphs/oasis/

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
number_of_transcripts=430



# # ========================== Check which transcripts are missing ====================================================
# rm ${output_dir}/missing
# for tat in `seq -s ' ' 0 ${number_of_transcripts}`; do
#     if [ ! -f ${output_dir}/SpeechGraph_`zeropad ${tat} 4`_*.txt ]; then
#         printf  '%s\n' "$tat"  >> ${output_dir}/missing
#     fi
# done


# ========================== Process transcripts ====================================================================

# --- Process transcripts from first to last transcript (full dataset) --------------------------------------------
first_tat=0
last_tat=430
for tat in `seq -s ' ' ${first_tat} ${last_tat}`; do
    echo "Processing transcript ${tat}..."
    python -u ./speech_graph.py ${tat} \
    > ${output_dir}/SpeechGraph_`zeropad ${tat} 4`_`date +%F`.txt 2>&1 # (pipe output and error msgs to text file)
done

first_tat=`head -1 ${output_dir}/missing`
last_tat=`tail -1 ${output_dir}/missing`

# ========================== Compile report =========================================================================
rm ${output_dir}/report

# Count errors
errors=0
for tat in ${output_dir}/*.txt; do
    finished_without_error=`tail -1 ${tat} | grep "finished in"`
    if [ $? != 0 ]; then
        errors=$(( errors+1))
    fi
done

total_processed_transcripts=`ls ${output_dir}/*.txt | wc | awk '{print $1}'`
added_processed_transcripts=$(( last_tat - first_tat ))

# Output summary message to report
printf 'Your computing job has finished, wohoooo! \n\nTats %s to %s have been processed. \n------------------------------------------\nAdded: \t\t %s \nTotal: \t\t %s \nErrors: \t\t%s\n' \
"${first_tat}" "${last_tat}" "${added_processed_transcripts}" "${total_processed_transcripts}" "${errors}"\
> ${output_dir}/report

# ------------------------- Error report: set to true to include error msgs in report --------------------------------
if true; then
    # Print error messages
    for tat in ${output_dir}/*.txt; do
        finished_without_error=`tail -1 ${tat} | grep "finished in"` # If no error has occurred, last line should say "...finished in..."
        if [ $? != 0 ]; then
            msg=`tail ${tat}`
            printf  '\n------------------ Error in %s ------------------\n %s \n' "$tat" "$msg" >> ${output_dir}/report
            # printf  '\n------------------ Error in %s ------------------\n %s \n' "$tat" "$msg"
        fi
    done
fi
# ========================== Send notification email ==========================
# Send short email:
# printf "Your computing job has finished, wohoooo! \n\nTats ${first_tat} to ${last_tat} have been processed. \n------------------------------------------\nProcessed: \t$(( last_tat - first_tat ))\nErrors: \t\t${errors}\n" | mail -s "SURPRISE SHAWTY" cnettekoven@web.de

# Send email with error report:
cat ${output_dir}/report | mail -s "netspy finished" cnettekoven@web.de


# # ========================== Troubleshooting ==========================
# # Delete all files where the error occurred because Ollie found no edges
# for tat in `seq -s ' ' 0 ${number_of_transcripts}`; do
#     if [ -f ${output_dir}/SpeechGraph_`zeropad ${tat} 4`_*.txt ]; then
#         tat_id=`zeropad ${tat} 4`
#         file=`ls ${output_dir}/SpeechGraph_${tat_id}_*.txt`
#         ollie_missing=` cat ${file} | grep "Created 0 edges (ollie)" `
#         if [ ! -z "$ollie_missing" ]; then
#             printf  '\n\n------------------ %s ------------------\n' "$tat"
#             sed -n '/+++ Paragraph: +++/,/+++++++++++++++++++/p' ${file}
#             # rm ${output_dir}/SpeechGraph_${tat_id}*
#         fi
#     fi
# done

# # Delete all files where the error occurred the filename had a dot in it
# for tat in `seq -s ' ' 0 ${number_of_transcripts}`; do
#     if [ -f ${output_dir}/SpeechGraph_`zeropad ${tat} 4`_*.txt ]; then
#         tat_id=`zeropad ${tat} 4`
#         file=`ls ${output_dir}/SpeechGraph_${tat_id}_*.txt`
#         dot_error=` tail -1 ${file} | grep "is not supported (supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff)" `
#         if [ ! -z "$dot_error" ]; then
#             # printf  '\n\n------------------ %s ------------------\n' "$tat"
#             # rm ${output_dir}/SpeechGraph_${tat_id}*
#         fi
#     fi
# done

# # Delete all files with errors
# for tat in `seq -s ' ' 0 ${number_of_transcripts}`; do
#     if [ -f ${output_dir}/SpeechGraph_`zeropad ${tat} 4`_*.txt ]; then
#         tat_id=`zeropad ${tat} 4`
#         file=`ls ${output_dir}/SpeechGraph_${tat_id}_*.txt`
#         finished_without_error=` cat ${file} | grep "finished in" `
#         if [ -z "$finished_without_error" ]; then
#             echo rm ${output_dir}/SpeechGraph_${tat_id}*
#         fi
#     fi
# done

# ls -1 *2021-04-1*.txt | sed -n '/SpeechGraph_2700/,/SpeechGraph_2915/p'
# # Delete all files between 2700 and 2915 that were processed on 2021-04-18
# for tat in `seq -s ' ' 2700 2915`; do
#     if [ -f ${output_dir}/SpeechGraph_`zeropad ${tat} 4`_2021-04-18.txt ]; then
#         tat_id=`zeropad ${tat} 4`
#         file=`ls ${output_dir}/SpeechGraph_${tat_id}_*.txt`
#         # finished_without_error=` cat ${file} | grep "finished in" `
#         # if [ -z "$finished_without_error" ]; then
#             echo rm ${output_dir}/SpeechGraph_${tat_id}*
#         # fi
#     fi
# done