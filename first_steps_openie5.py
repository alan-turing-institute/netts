#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  first_steps_openie5.py
#
# Description:
#               First steps using OpenIE5 (successor to OLLIE): the principal Open Information Extraction (Open IE) system from the University of Washington (UW) and Indian Institute of Technology,Delhi (IIT Delhi)
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# to activate python environment, run:
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
from pyopenie import OpenIE5
extractor = OpenIE5('http://localhost:9000')
extractions = extractor.extract(
    "The U.S. president Barack Obama gave his speech to thousands of people.")
