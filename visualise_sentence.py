#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  visualise_sentence.py
#
# Description:
#               Script to visualise sentence using OpenIE5 and Stanford CoreNLP
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# Initiliase sentence
# sentence = "But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well."
sentence = "The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture."
"The picture is very mysterious"
"I like about it"
"I would like to understand more concept, context of the picture"

# ------------------------------------------------------------------------------
# Initiliase Stanford CoreNLP server and OpenIE5 server
client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref', 'openie'],
                       timeout=30000,
                       memory='16G')
extractorIE5 = OpenIE5('http://localhost:6000')
# Annotate with Stanford CoreNLP and extract with OpenIE5
extractions = extractorIE5.extract(sentence)
annotations = client.annotate(sentence)
# ------------------------------------------------------------------------------
# Find edges and edge labels
edges = []
edge_labels = {}
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
    node1 = node1.lower()
    node2 = node2.lower()
    if node2 != '':
        edges.append([node1, node2])
        edge_labels[(node1, node2)] = extract['extraction']['rel']['text']


# # ------------------------------------------------------------------------------
# # Construct Speech Graph
# G_orig = nx.Graph()
# G_orig.add_edges_from(edges)
# pos = nx.spring_layout(G_orig)

# # Plot graph
# plt.figure()
# nx.draw(G_orig, pos, edge_color='black', width=1, linewidths=1,
#         node_size=500, node_color='pink', alpha=0.9,
#         labels={node: node for node in G_orig.nodes()})
# nx.draw_networkx_edge_labels(
#     G_orig, pos, edge_labels=edge_labels, font_color='red')
# plt.axis('off')
# plt.show()

# ------------------------------------------------------------------------------
# Merge nodes that are separate mentions of the same entity

# Extract proper node name and alternative node names
proper_nn = []
alt_nn = []
for mention in annotations.corefChain[0].mention:
    if mention.mentionType == "NOMINAL" or mention.mentionType == "PROPER":
        # Make the "proper" or "nominal" mention the node label
        node_name = [node_part.originalText.lower() for node_part in annotations.sentence[mention.sentenceIndex]
                     .token[mention.beginIndex:mention.endIndex]]
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
                                 .token[mention.beginIndex:mention.endIndex]]
        if len(alternative_node_name) > 1:
            alternative_node_name = (' ').join(alternative_node_name)
        else:
            alternative_node_name = alternative_node_name[0]
        #
        # Append alternative node name only if it is different from all other alternative node names
        if alternative_node_name not in alt_nn:
            alt_nn.append(alternative_node_name)


# Replace node name with proper node name and edge_label
# Method: test if node text appears in list of alternative node names or is part of the proper node name and replace with the full proper node name
new_edge_labels = {}
for e, edge in enumerate(edges):
    rel = edge_labels[tuple(edge)]
    for n, node in enumerate(edge):
        for node_token in node.split(' '):
            # Test if node is the same as proper node name
            if node_token in proper_nn:
                # print('{} is in {}'.format(node, proper_nn))
                edges[e][n] = proper_nn[0]
                new_edge_labels[tuple(edges[e])] = rel
            # Test if node is part of the proper node name (do any of the proper node name words match the chosen node)
            elif node_token in proper_nn[0].split(' '):
                edges[e][n] = proper_nn[0]
                new_edge_labels[tuple(edges[e])] = rel
            elif node_token in alt_nn:
                # print('{} is in {}'.format(node, alt_nn))
                edges[e][n] = proper_nn[0]
                new_edge_labels[tuple(edges[e])] = rel
            else:
                print('{} NOT in {}'.format(node, alternative_node_name))
                new_edge_labels[tuple(edges[e])] = rel

# ------------------------------------------------------------------------------
# Construct Speech Graph
G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)

# Plot graph
plt.figure()
nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()})
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=new_edge_labels, font_color='red')
plt.axis('off')
plt.show()


for i, extract in enumerate(extractions):
    print(extract['extraction']['arg1']['text'])
    print(extract['extraction']['rel']['text'])
    print(extract['extraction']['arg2s'][0]['text'])
