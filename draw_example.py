

#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  draw_example.py
#
# Description:
#               Draw example entities
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
import matplotlib.pyplot as plt


# Initialise sentence
# example_sentence = 'A boy is sitting in a barn.'
example_sentence = 'I see a boy sitting in a barn.'

# Annotate
with CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma',
                    'ner', 'parse', 'depparse', 'coref', 'natlog', 'openie'],
        timeout=30000,
        memory='16G') as client:
    ann = client.annotate(example_sentence)

# Step 1: ----- Extract entities -----
# Loop through words in the sentence
# If word is a PRP or a NN, then make the word a node
nodes = []
for token in ann2.sentence[0].token:
    if token.pos == 'NN':
        nodes.append(token.value)
    elif token.pos == 'PRP':
        nodes.append(token.value)

edges = []
edge_labels = []
ann.sentence[0].hasRelationAnnotations
# Step 2: ----- Extract edges -----
# Find openie relations
for triple in ann2.sentence[0].openieTriple:
    edges.append([triple.subject, triple.object])
    edge_labels = {(triple.subject, triple.object): triple.relation}

# Find enhanced dependencies relations
# Map clausal components


# Construct graph object
G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)

# Plot graph object
plt.figure()
nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()})
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
plt.axis('off')
plt.show()
