#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  visualise_entities.py
#
# Description:
#               Visualise entities from HC example data
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# to activate python environment, run:
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
import networkx as nx
import os
import os.path as op
import stanza
import pandas as pd
from stanza.server import CoreNLPClient
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')

# Import data
data_dir = '/Users/CN/Documents/Projects/Cambridge/data'
f = open(op.join(data_dir, 'Kings',
                 'Prolific_pilot_all_transcripts', '3138838-TAT30.txt'), 'r')
text = f.read()
f.close()

# Create text pipeline
nlp = stanza.Pipeline(lang='en')

doc = nlp(text)

example_sentence = doc.sentences[0].text


with CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma',
                    'ner', 'parse', 'depparse', 'coref', 'openie'],
        timeout=30000,
        memory='16G') as client:
    ann = client.annotate(example_sentence)

sentence = ann.sentence[0]
# get the constituency parse of the first sentence
print('---')
print('constituency parse of first sentence')
constituency_parse = sentence.parseTree
print(constituency_parse)

# get the first subtree of the constituency parse
print('---')
print('first subtree of constituency parse')
print(constituency_parse.child[0])

# get the value of the first subtree
print('---')
print('value of first subtree of constituency parse')
print(constituency_parse.child[0].value)

# get the dependency parse of the first sentence
print('---')
print('dependency parse of first sentence')
dependency_parse = sentence.basicDependencies
print(dependency_parse)

# get the first token of the first sentence
print('---')
print('first token of first sentence')
token = sentence.token[0]
print(token)

# get the part-of-speech tag
print('---')
print('part of speech tag of token')
token.pos
print(token.pos)

# get the named entity tag
print('---')
print('named entity tag of token')
print(token.ner)

# get an entity mention from the first sentence
print('---')
print('first entity mention in sentence')
print(sentence.mentions[0])

# access the coref chain
print('---')
print('coref chains for the example')
print(ann.corefChain)

# Use tokensregex patterns to find who wrote a sentence.
pattern = '([ner: PERSON]+) /wrote/ /an?/ []{0,3} /sentence|article/'
matches = client.tokensregex(text, pattern)
# sentences contains a list with matches for each sentence.
assert len(matches["sentences"]) == 3
# length tells you whether or not there are any matches in this
assert matches["sentences"][1]["length"] == 1
# You can access matches like most regex groups.
matches["sentences"][1]["0"]["text"] == "Chris wrote a simple sentence"
matches["sentences"][1]["0"]["1"]["text"] == "Chris"

# Use semgrex patterns to directly find who wrote what.
pattern = '{word:wrote} >nsubj {}=subject >dobj {}=object'
matches = client.semgrex(text, pattern)
# sentences contains a list with matches for each sentence.
assert len(matches["sentences"]) == 3
# length tells you whether or not there are any matches in this
assert matches["sentences"][1]["length"] == 1
# You can access matches like most regex groups.
matches["sentences"][1]["0"]["text"] == "wrote"
matches["sentences"][1]["0"]["$subject"]["text"] == "Chris"
matches["sentences"][1]["0"]["$object"]["text"] == "sentence"


ann2.to_dict()


# Show PoS tags
print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')


# Extract entities from entire document
print(*[f'entity: {ent.text}\ttype: {ent.type}' for ent in doc.ents], sep='\n')
# Extract entities from sentence
print(
    *[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')


G = nx.Graph()
G.add_edge('A', 'B', weight=4)
G.add_edge('B', 'D', weight=2)
G.add_edge('A', 'C', weight=3)
G.add_edge('C', 'D', weight=4)
nx.shortest_path(G, 'A', 'D', weight='weight')
['A', 'B', 'D']
