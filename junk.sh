
wbic-gate.vss.cloud.private.cam.ac.uk
ssh crn29@wbic-gate.vss.cloud.private.cam.ac.uk
r4b3nbl4u

for i in `ls /Users/CN/Dropbox/speech_graphs/general_public_tat/*2021-02-08.txt`; do
    last_line=`tail -1 $i | awk '{print $1}'`
    if [ "${last_line}" != "Processing" ]; then
        echo " ";
        echo $i;
        tail -1 $i;
    fi
done

# Rename text files for general public transcripts.
for i in `ls /Users/CN/Dropbox/speech_graphs/general_public_tat/*2021-02-08.txt`; do
    echo " ";
    echo $i;
    file_id=`tail -1 $i | awk '{print $3}'`
    mv $i ${i%*.txt}_${file_id}.txt
done
# Rename text files for pilot transcripts.
for i in `ls /Users/CN/Dropbox/speech_graphs/pilot/*2021-02-08.txt`; do
    echo " ";
    echo $i;
    file_id=`tail -1 $i | awk '{print $3}'`
    mv $i ${i%*.txt}_${file_id}.txt
done



# Rename all other files for general public & pilot transcripts.
for i in `ls /Users/CN/Dropbox/speech_graphs/pilot/*2021-02-08*.txt`; do
    echo " ";
    # echo $i;
    file_id=`tail -1 $i | awk '{print $3}'`
    image_id=`ls ${i%*2021-02-08*}*.png`
    graph_id=`ls ${i%*2021-02-08*}*.gpickle`
    mv ${image_id} ${image_id%*.png}_${file_id}.png
    mv ${graph_id} ${graph_id%*.gpickle}_${file_id}.gpickle
done

cd /Users/CN/Dropbox/speech_graphs/general_public_tat/
for i in `seq -s ' ' 0 175`; do
    new=$(( i + 119))
    old_n=`zeropad ${i} 4`
    new_n=`zeropad ${new} 4`
    old_file_name=`ls SpeechGraph_${old_n}_*.txt`
    # mv ${old_file_name} SpeechGraph_${new_n}_2021-02-08${old_file_name#*_2021-02-08}
    old_file_name=`ls SpeechGraph_${old_n}_*.gpickle`
    # mv ${old_file_name} SpeechGraph_${new_n}_2021-02-08${old_file_name#*_2021-02-08}
    old_file_name=`ls SpeechGraph_${old_n}_*.png`
    # mv ${old_file_name} SpeechGraph_${new_n}_2021-02-08${old_file_name#*_2021-02-08}
done


# How many transcripts do we have of each TAT?
for i in 8 10 13 19 21 24 27 30; do
    echo "TAT"${i}
    ls /Users/CN/Documents/Projects/Cambridge/data/Kings/*/*TAT${i}*.txt | wc | awk '{print $1}'
    
done