#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  start_opien5.sh
#
# Description:  Script to start openie5
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
## Navigate to openie5 folder
cd /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/OpenIE-standalone

## Start standalone version OR HTTP server (For use with python wrapper, you need to start HTTP server)
# Running from a stand-alone jar.
# java -Xmx10g -XX:+UseConcMarkSweepGC -jar openie-assembly-5.0-SNAPSHOT.jar
# Running as HTTP Server
java -Xmx10g -XX:+UseConcMarkSweepGC -jar openie-assembly-5.0-SNAPSHOT.jar  --ignore-errors --httpPort 6000

# To see options, run
# java -jar openie-assembly-5.0-SNAPSHOT.jar --usage