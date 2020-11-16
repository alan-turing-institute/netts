
#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  extract_entities.py
#
# Description:
#               Extract entities from HC example data
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# to activate python environment, run:
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
import os
import os.path as op
import stanza
import pandas as pd
from stanza.server import CoreNLPClient
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
# Create text pipeline
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
# Import text
doc = nlp("Chris Manning teaches at Stanford University. He lives in the Bay Area.")
# Extract entities from entire document
print(*[f'entity: {ent.text}\ttype: {ent.type}' for ent in doc.ents], sep='\n')
# Extract entities from sentence
print(
    *[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')
# Extract BIOES NER tags
# BIOES consists of the tags B, E, I, S or O
# where S is used to represent a chunk containing a single token.
# Chunks of length greater than or equal to two always start with the B tag and end with the E tag.
print(*[f'token: {token.text}\tner: {token.ner}' for sent in doc.sentences for token in sent.tokens], sep='\n')
