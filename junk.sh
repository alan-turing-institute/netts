
wbic-gate.vss.cloud.private.cam.ac.uk
ssh crn29@wbic-gate.vss.cloud.private.cam.ac.uk
r4b3nbl4u

for i in `ls /Users/CN/Dropbox/speech_graphs/pilot/*2021-02-08.txt`; do
    last_line=`tail -1 $i | awk '{print $1}'`
    if [ "${last_line}" != "Processing" ]; then
        echo " ";
        echo $i;
        tail -1 $i;
    fi
done

