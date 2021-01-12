#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  speech_graph.py
#
# Description:
#               Script to visualise sentence using OpenIE5 and Stanford CoreNLP
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
# TO DO
#   - Sanity check: Is each relation represented only once in the edge? (Also check parallel edges in multiedge graph)
#   - Plot graphs coloured by confidence / extraction type

# ------------------------------------------------------------------------------
#
#                                               EXAMPLE TRANSCRIPTS
#                                               ===================
# Property                                  Topic                                       Index       Name
# ________________________________________________________________________________________________________________
# ambiguous coreferencing:                  (two women)                                 0       3138838-TAT10
# ambiguous coreferencing:                  (four men lying on field)                   1       3138838-TAT13
# clear text and very connected network:    (man wearing jacket, hat and hoodie)        2       3138838-TAT30
# network as one long, connected line       (women and child at home)                   3       3138849-TAT10

# many synonyms for picture:                (picture, photograph, photo)                10      3138883-TAT30
# many adjectives:                          (picture, photograph, photo)                11      3138910-TAT24

# many adjectives:                          (snowy day)                                 41      3145067-TAT30
# many self-references                      (history major)                             8       3138883-TAT13
# faulty transcript                         (clasped hands)                             9       3138883-TAT24


import networkx as nx
import os
import os.path as op
import stanza
import pandas as pd
from stanza.server import CoreNLPClient
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
from pyopenie import OpenIE5
import matplotlib.pyplot as plt
from copy import deepcopy
from itertools import chain
import numpy as np
from nlp_helper_functions import expand_contractions, remove_interjections, replace_problematic_symbols, process_sent, files
from visualise_paragraph_functions import create_edges_ollie, create_edges_stanza, get_word_types, get_adj_edges, get_prep_edges, get_obl_edges, add_obl_edges, get_node_synonyms, split_node_synonyms, split_nodes, merge_corefs, clean_nodes, add_adj_edges, add_prep_edges, get_unconnected_nodes
import time
# ------------------------------------------------------------------------------
# Time execution of script
start_time = time.time()
# ------------------------------------------------------------------------------
# Get sentence
selected_file = 6
data_dir = '/Users/CN/Documents/Projects/Cambridge/data'
input_file = op.join(
    data_dir, 'Kings', 'Prolific_pilot_all_transcripts', files[selected_file])
with open(input_file, 'r') as fh:
    orig_text = fh.read()

# ------------------------------------------------------------------------------
# ------- Clean text -------
# Need to replace problematic symbols before ANYTHING ELSE, because other tools cannot work with problematic symbols
text = replace_problematic_symbols(orig_text)  # replace ’ with '
text = expand_contractions(text)  # expand it's to it is
text = remove_interjections(text)  # remove Ums and Mmms
text = text.strip()  # remove trailing and leading whitespace
# ------------------------------------------------------------------------------
# ------- Run Stanford CoreNLP (Stanza) -------
# Annotate and extract with Stanford CoreNLP

with CoreNLPClient(properties={
    'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,coref,openie',
    'pos.model': '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/OpenIE-standalone/target/streams/$global/assemblyOption/$global/streams/assembly/8a3bd51fe5c1bb09a51f326fa358947f6dc78463_8e7f18d9ae73e8daf5ee4d4e11167e10f8827888_da39a3ee5e6b4b0d3255bfef95601890afd80709/edu/stanford/nlp/models/pos-tagger/english-bidirectional/english-bidirectional-distsim.tagger'
}, be_quiet=True) as client:
    ex_stanza = client.annotate(text)

# ------------------------------------------------------------------------------
# ------- Print cleaned text -------
print("\n+++ Paragraph: +++ \n\n %s \n\n+++++++++++++++++++" % (text))

# ------------------------------------------------------------------------------
# ------- Run OpenIE5 (Ollie) -------
# Ollie can handle more than one sentence at a time, but need to loop through sentences to keep track of sentence index
extractorIE5 = OpenIE5('http://localhost:6000')  # Initialize Ollie

ex_ollie = {}
for i, sentence in enumerate(ex_stanza.sentence):
    if len(sentence.token) > 1:
        print(f'====== Submitting sentence {i+1} tokens =======')
        sentence_text = (' ').join(
            [token.originalText for token in sentence.token if token.originalText])
        print('{}'.format(sentence_text))
        extraction = extractorIE5.extract(sentence_text)
        ex_ollie[i] = extraction
    else:
        print('====== Skipping sentence {}: Sentence has too few tokens: "{}" ======='.format(i + 1, (' ').join(
            [token.originalText for token in sentence.token if token.originalText])))
print('+++++++++++++++++++\n')
# --------------------- Create ollie edges ---------------------------------------
ollie_edges, ollie_edges_text_excerpts, ollie_one_node_edges, ollie_one_node_edges_text_excerpts = create_edges_ollie(
    ex_ollie)

edges = ollie_edges
# --------------------- Create stanza edges ---------------------------------------
stanza_edges, stanza_edges_text_excerpts = create_edges_stanza(ex_stanza)
# --------------------- Get word types ---------------------------------------
no_noun, poss_pronouns, dts, nouns, nouns_origtext, adjectives = get_word_types(
    ex_stanza)

adjectives, adjective_edges = get_adj_edges(ex_stanza)

prepositions, preposition_edges = get_prep_edges(ex_stanza)

obliques, oblique_edges = get_obl_edges(ex_stanza)
# --------------------- Add oblique edges ---------------------------------------
edges = add_obl_edges(edges, oblique_edges)
# --------------------- Get node name synonyms ---------------------------------------
node_name_synonyms = get_node_synonyms(ex_stanza, no_noun)
# --------------------- Split nodes connected by preposition ---------------------------------------
edges, node_name_synonyms = split_node_synonyms(
    node_name_synonyms, preposition_edges, edges)

edges = split_nodes(edges, preposition_edges, no_noun)
# --------------------- Merge coreferenced nodes ---------------------------------------
edges, orig_edges = merge_corefs(edges, node_name_synonyms, no_noun)

preposition_edges, orig_preposition_edges = merge_corefs(
    preposition_edges, node_name_synonyms, no_noun)

adjective_edges, orig_adjective_edges = merge_corefs(
    adjective_edges, node_name_synonyms, no_noun)

oblique_edges, orig_oblique_edges = merge_corefs(
    oblique_edges, node_name_synonyms, no_noun)

# --------------------- Clean nodes ---------------------------------------
edges = clean_nodes(edges, nouns, adjectives)
# --------------------- Add adjective edges / preposition edges / unconnected nodes ---------------------------------------
edges = add_adj_edges(edges, adjective_edges, add_adjective_edges=True)

edges = add_prep_edges(edges, preposition_edges,
                       add_all_preposition_edges=True)

unconnected_nodes = get_unconnected_nodes(edges, orig_edges, nouns)
# --------------------- Print execution time ---------------------------------------
print("Process finished in --- %s seconds ---" % (time.time() - start_time))
# --------------------- Speech Graph ---------------------------------------
# Construct Speech Graphs
G = nx.MultiDiGraph()
# G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)
nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()})
edge_labels = dict([((u, v,), d['relation'])
                    for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_color='red')
plt.axis('off')
plt.show()


# # MultiDiGraph
# G = nx.MultiDiGraph()
# G.add_edges_from(edges)
# font_size = 10
# node_size = 2000
# add_unconnected_nodes = False
# if add_unconnected_nodes:
#     G.add_nodes_from(unconnected_nodes)  # Add unconnected nodes

# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True, edge_color='black',
#         node_color='pink', connectionstyle='arc3, rad = 0.1', font_size=font_size, node_size=node_size)
# edge_labels = dict([((u, v,), d['relation'])
#                     for u, v, d in G.edges(data=True)])
# nx.draw_networkx_edge_labels(
#     G, pos, edge_labels=edge_labels, font_color='black', font_size=font_size)
# figure = plt.gcf()
# plt.show()
