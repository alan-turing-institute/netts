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
import matplotlib.pyplot as plt


example_sentence = 'A boy is sitting in a barn.'

with CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma',
                    'ner', 'parse', 'depparse', 'coref', 'openie'],
        timeout=30000,
        memory='16G') as client:
    ann = client.annotate(example_sentence)

# Create empty graph
G = nx.Graph()

# Add nodes
G.add_nodes_from([(1, 2)])

# Add nodes from iterable container
G.add_nodes_from([
    ('boy', {"color": "red"}),
    ('barn', {"color": "green"}),
])

# Add edge
G.add_edge('boy', 'barn')
G.add_edge('boy', 'is sitting in')
G.add_edge('boy', 'barn', label='is sitting in')


# Test drawing
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

# Plot example sentence: I see a boy sitting in a barn.
edges = [['a boy', 'a barn'], ['I', 'a boy']]
G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)
plt.figure()
nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()})
nx.draw_networkx_edge_labels(G, pos, edge_labels={('a boy', 'a barn'): 'sitting in',
                                                  ('I', 'a boy'): 'I see'}, font_color='red')
plt.axis('off')
plt.show()

# Plot example sentence from TAT: I see a man in the dark standing against a light post.
