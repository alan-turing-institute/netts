#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  visualise_paragraph_function.py
#
# Description:
#               Script to visualise sentence using OpenIE5 and Stanford CoreNLP
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
# cd /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/
# python visualise_paragraph_function.py /Users/CN/Documents/Projects/Cambridge/data/Kings/Prolific_pilot_all_transcripts/3138838-TAT10.txt

# TO DO
#   - Add sentence index to Ollie extractions such that I can keep track which sentence an extraction is from
#   - Add MultiGraph functionality
#   - Add Directionality to relations
#   - Fix missing extractions from paragraph
#   - Fix faulty extrcations from paragraph
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
# from nlp_helper_functions import expand_contractions, process_sent

# ------------------------------------------------------------------------------
# Initiliase sentence


file = sys.argv[1]

f = open(file, 'r')
text = f.read()
f.close()


# # To print corenlp to text file if you need to search through it
# sys.stdout = open(op.join(data_dir, 'Kings',
#                           'Prolific_pilot_all_transcripts', file + '_corenlp_extraction.txt'), 'w')
# print(annotations)
# sys.stdout.close()

# sentence = "The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture."
# "The picture is very mysterious"
# "I like about it"
# "I would like to understand more concept, context of the picture"
# text = "I see a man in the dark standing against a light post. It seems to be in the middle of the night; I think because the lightbulb is working. On the picture there seems to be like a park and Or trees but in those trees there are little balls of light reflections as well. I cannot see the Anything else because it’s very dark. But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well. The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture."

# ------------------------------------------------------------------------------
# ------- Clean text of difficult symbols -------
# Ollie cannot handle this symbol ’ so replace with symbol that Ollie can handle '
text_clean = text.replace('’', "'")
text_clean = text_clean.replace('...', " ")

# ------------------------------------------------------------------------------
# ------- Extract relations with Stanford CoreNLP (Stanza) -------

# Initiliase Stanford CoreNLP server
client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref', 'openie'],
                       timeout=30000,
                       memory='16G')
# Annotate with Stanford CoreNLP
annotations = client.annotate(text_clean)

# for i, extract in enumerate(extractions):
#     print('\n {} \t: {} - {} - {}'.format(
#         extract['confidence'],
#         extract['extraction']['arg1']['text'],
#         extract['extraction']['rel']['text'],
#         extract['extraction']['arg2s'][0]['text'],
#     ))

# ------------------------------------------------------------------------------
# ------- Extract relations with OpenIE5 (Ollie) -------

# Initialize Ollie
extractorIE5 = OpenIE5('http://localhost:6000')

# Ollie can handle more than one sentence at a time, but need to loop through sentences to keep track of sentence index
extractions = []
for sentence in text_clean.split('.'):
    sentence = sentence.strip()
    if len(sentence) > 1:
        extraction = extractorIE5.extract(sentence)
        extractions = extractions + extraction


# example = 'On the picture there seems to be a park and trees, but in those trees there are little balls of light reflections'
# ex = extractorIE5.extract(text_clean)
# ------------------------------------------------------------------------------

# Find edges and edge labels extracted by OpenIE5
ollie_edges = []
ollie_edge_labels = {}
ollie_edges_text_excerpts = []
# Create nodes and edges
for e, extract in enumerate(extractions):
    # print(e, extract)
    node1 = extract['extraction']['arg1']['text']
    node2 = ''
    # Concatenate all text of argument 2
    for arg2_no, arg2 in enumerate(extract['extraction']['arg2s']):
        # print(arg_no, arg['text'])
        node2 = node2 + ' ' + arg2['text']
        # print(node2)
    # Add nodes (arg1, arg2 and relationship)
    node1 = node1.lower().strip()
    node2 = node2.lower().strip()
    relation = extract['extraction']['rel']['text'].lower().strip()
    edge_text = (' ').join([node1, relation, node2])
    # If edge has two nodes and is not duplicate of previous edge, add edge
    if node2 != '' and edge_text not in ollie_edges_text_excerpts:
        ollie_edges.append([node1, node2])
        ollie_edge_labels[(node1, node2)
                          ] = extract['extraction']['rel']['text']
        ollie_edges_text_excerpts.append(edge_text)

edges = ollie_edges
edge_labels = ollie_edge_labels


# Find edges and edge labels extracted by Stanza OpeniIE
stanza_edges = []
stanza_edge_labels = {}
stanza_edges_text_excerpts = []
for sentence in annotations.sentence:
    for triple in sentence.openieTriple:
        node1 = triple.subject.lower()
        node2 = triple.object.lower()
        relation = triple.relation.lower()
        stanza_edges.append([node1, node2])
        stanza_edge_labels[(node1, node2)] = relation
        stanza_edges_text_excerpts.append((' ').join([node1, relation, node2]))

# Compare stanza and openie5 edges and add any edges that Openie5 did not pick up


# ------------------------------------------------------------------------------
# ------- Merge nodes that are separate mentions of the same entity -------

# First extract a list of determinants present in the text that need to be ignored when matching (You don't want to match "the picture" and "the dog" on "the")
list_of_DTs = []
for sentence in annotations.sentence:
    for token in sentence.token:
        if token.pos == "DT" or token.pos == "RB" or token.pos == "TO" or token.pos == "IN":
            # print(token.lemma)
            if token.lemma not in list_of_DTs:
                list_of_DTs.append(token.lemma)


# Extract proper node name and alternative node names
node_name_synonyms = {}

for coreference in annotations.corefChain:
    proper_nn = []
    alt_nn = []
    for mention in coreference.mention:
        if mention.mentionType == "NOMINAL" or mention.mentionType == "PROPER":
            # Make the "proper" or "nominal" mention the node label
            node_name = [node_part.originalText.lower() for node_part in annotations.sentence[mention.sentenceIndex]
                         .token[mention.beginIndex: mention.endIndex] if node_part.originalText not in list_of_DTs]
            # Concatenate node names that consist of several tokens
            if len(node_name) > 1:
                node_name = (' ').join(node_name)
            else:
                node_name = node_name[0]
            #
            # Append proper node name only if it is different from all other proper node names
            if node_name not in proper_nn:
                proper_nn.append(node_name)
        else:
            alternative_node_name = [node_part.originalText.lower() for node_part in annotations.sentence[mention.sentenceIndex]
                                     .token[mention.beginIndex: mention.endIndex] if node_part.originalText not in list_of_DTs]
            if len(alternative_node_name) > 1:
                alternative_node_name = (' ').join(alternative_node_name)
            else:
                alternative_node_name = alternative_node_name[0]
            #
            # Append alternative node name only if it is different from all other alternative node names
            if alternative_node_name not in alt_nn:
                alt_nn.append(alternative_node_name)
    if proper_nn == []:
        for mention in coreference.mention:
            for token in annotations.sentence[mention.sentenceIndex].token[mention.beginIndex: mention.endIndex]:
                if token.lemma == token.originalText:
                    proper_nn.append(token.originalText)
                    continue
    node_name_synonyms[proper_nn[0]] = alt_nn


# Clean node names that include more than one node (for example "the man on the picture" make into "man")
for n in range(1, len(node_name_synonyms)):
    node = list(node_name_synonyms)[n]
    if len(node.split(' ')) > 2:
        # get nodes that are not current node
        keys_without_n = [x for i, x in enumerate(
            list(node_name_synonyms)) if i != n]
        for key in keys_without_n:
            match = node.find(key)
            if match != -1:
                matched_key = key
                new_node_name = node.split(matched_key)[0].strip()
                node_name_synonyms[new_node_name] = node_name_synonyms.pop(
                    node)


# Replace node name with proper node name and edge_label
# Method: test if node text appears in list of alternative node names or is part of the proper node name and replace with the full proper node name
orig_edge_labels = deepcopy(edge_labels)
orig_edges = deepcopy(edges)

new_edge_labels = {}
for e, edge in enumerate(edges):
    rel = edge_labels[tuple(edge)]
    for n, node in enumerate(edge):
        #
        found_match = False
        for node_token in node.split(' '):
            if found_match == False:
                if node_token in list_of_DTs:
                    # If token is a determinant, move on to the next one.
                    continue
                elif node_token in list(node_name_synonyms.keys()):
                    # Replace with proper node name if node is the same as proper node name
                    proper_node_name = list(node_name_synonyms.keys())[
                        list(node_name_synonyms.keys()).index(node_token)]
                    print("Replace \t '{}' \t\t with \t\t'{}' in {}". format(
                        node, proper_node_name, edge))
                    edges[e][n] = proper_node_name
                    found_match = True
                for ann, alternative_node_name in enumerate(list(node_name_synonyms.values())):
                    if node_token in alternative_node_name:
                        # Replace with proper node name if node is part of one of the alternative node names
                        proper_node_name = list(node_name_synonyms.keys())[ann]
                        print("Replace \t '{}' \t\t with \t\t'{}' in {}".format(
                            node, proper_node_name, edge))
                        edges[e][n] = proper_node_name
                        found_match = True
            else:
                print('Moving on...')
    new_edge_labels[tuple(edges[e])] = rel

# ------------------------------------------------------------------------------
# Construct Speech Graph and Save plot as output
# Initialize output
output_dir = '/Users/CN/Documents/Projects/Cambridge/extractions'
file_stem = op.splitext(file.split('/')[-1])[0]
output = op.join(output_dir, 'graph_' + file_stem)
output_orig = op.join(output_dir, 'graph_orig_' + file_stem)


G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)
# Plot
plt.figure()
nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()})
edge_labels = dict([((u, v,), d['relation'])
                    for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_color='red')
plt.axis('off')
plt.show()
# plt.savefig(output)

# Original Speech Graph (before merging)
G_orig = nx.Graph()
G_orig.add_edges_from(orig_edges)
pos = nx.spring_layout(G_orig)
# Plot
plt.figure()
nx.draw(G_orig, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()})
edge_labels = dict([((u, v,), d['relation'])
                    for u, v, d in G_orig.edges(data=True)])
nx.draw_networkx_edge_labels(
    G_orig, pos, edge_labels=edge_labels, font_color='red')
plt.axis('off')
# plt.show()
plt.savefig(output_orig)