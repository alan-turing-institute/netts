#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  visualise_paragraph.py
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
#   - Add sentence index to Ollie ex_ollie such that I can keep track which sentence an extraction is from
#   - Add MultiGraph functionality
#   - Add Directionality to relations
#   - Fix missing ex_ollie from paragraph
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
from itertools import chain
import numpy as np
from nlp_helper_functions import expand_contractions, remove_interjections, replace_problematic_symbols, process_sent, files

# ------------------------------------------------------------------------------
# Get sentence
data_dir = '/Users/CN/Documents/Projects/Cambridge/data'
# Good example transcript (man wearing jacket) is transcript files[2]
file = files[0]
f = open(op.join(data_dir, 'Kings',
                 'Prolific_pilot_all_transcripts', file), 'r')
orig_text = f.read()
f.close()

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
with CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma',
                    'ner', 'parse', 'depparse', 'coref', 'openie'],
        timeout=30000,
        memory='16G') as client:
    ex_stanza = client.annotate(text)


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


# ------------------------------------------------------------------------------
# Find edges and edge labels extracted by OpenIE5
ollie_edges = []
ollie_edges_text_excerpts = []
# Create nodes and edges
for e, extract_val in enumerate(list(ex_ollie.values())):
    if extract_val != []:
        for extract in extract_val:
            # print(e, extract)
            node1 = extract['extraction']['arg1']['text']
            node2 = ''
            # Concatenate all text of argument 2
            for arg2_no, arg2 in enumerate(extract['extraction']['arg2s']):
                # print(arg2_no, arg2['text'])
                node2 = node2 + ' ' + arg2['text']
                # print(node2)
            # Add nodes (arg1, arg2 and relationship)
            node1 = node1.lower().strip()
            node2 = node2.lower().strip()
            relation = extract['extraction']['rel']['text'].lower().strip()
            edge_text = (' ').join([node1, relation, node2])
            context = extract['extraction']['context']
            if context != None:
                context = context['text']
            # If edge has two nodes and is not duplicate of previous edge, add edge
            if node2 != '' and edge_text not in ollie_edges_text_excerpts:
                # ollie_edges.append([node1, node2])
                ollie_edges_text_excerpts.append(edge_text)
                a = (node1, node2, {'relation': relation,
                                    'confidence': extract['confidence'],
                                    'context': context,
                                    'negated': extract['extraction']['negated'],
                                    'passive': extract['extraction']['passive'],
                                    'extractor': 'ollie',
                                    'sentence': e
                                    })
                ollie_edges.append(a)


edges = ollie_edges


# Find edges and edge labels extracted by Stanza OpeniIE
stanza_edges = []
stanza_edge_labels = {}
stanza_edges_text_excerpts = []
for sentence in ex_stanza.sentence:
    for triple in sentence.openieTriple:
        node1 = triple.subject.lower()
        node2 = triple.object.lower()
        relation = triple.relation.lower()
        stanza_edges.append([node1, node2])
        stanza_edge_labels[(node1, node2)] = relation
        stanza_edges_text_excerpts.append((' ').join([node1, relation, node2]))


# ------------------------------------------------------------------------------
# ------- Get list of determiners -------
# First extract a list of determiners present in the text that need to be ignored when matching (You don't want to match "the picture" and "the dog" on "the")
do_not_match = []
dts = []
for sentence in ex_stanza.sentence:
    for token in sentence.token:
        if token.pos == "DT" or token.pos == "RB" or token.pos == "TO" or token.pos == "IN":
            # print(token.lemma)
            if token.lemma not in do_not_match:
                do_not_match.append(token.lemma)
        if token.pos == "DT":
            if token.lemma not in dts:
                dts.append(token.lemma)

# ------------------------------------------------------------------------------
# ------- Extract all nouns (proxy for entities, i.e. nodes) -------
nouns = []
for sentence in ex_stanza.sentence:
    for token in sentence.token:
        if token.pos == "PRP" or token.pos == "NN":
            # print(token.lemma)
            if token.lemma not in nouns:
                nouns.append(token.lemma)

# ------------------------------------------------------------------------------
# ------- Extract all adjectives -------
adjectives = []
for sentence in ex_stanza.sentence:
    for token in sentence.token:
        if token.pos == "JJ":
            # print(token.lemma)
            if token.lemma not in adjectives:
                adjectives.append(token.lemma)


# ------------------------------------------------------------------------------
# ------- Extract preposition relations -------
# Separate any preposition relations in node name synonyms

# Get a list of prepositions and track where they point to
prepositions = []
preposition_edges = []

for idx_sentence, sentence in enumerate(ex_stanza.sentence):
    for word in sentence.enhancedDependencies.edge:
        if word.dep.split(':')[0] == 'nmod':
            source = word.source - 1
            target = word.target - 1
            preposition = word.dep.split(':')[1]
            source_word = sentence.token[source].originalText
            target_word = sentence.token[target].originalText
            # print('{}'.format((' ').join(
            #     [token.originalText for token in sentence.token if token.originalText])))
            # print(' {} {} {}'.format(
            #     sentence.token[source].originalText, preposition, sentence.token[target].originalText))
            preposition_info = (source_word, target_word, {'relation': preposition,
                                                           #    'confidence': None,
                                                           #    'context': None,
                                                           #    'negated': None,
                                                           #    'passive': None,
                                                           'extractor': 'preposition',
                                                           'sentence': idx_sentence
                                                           })
            prepositions.append(preposition)
            preposition_edges.append(preposition_info)

# ------------------------------------------------------------------------------
# ------- Find node name synonyms in coreference chain -------

# Extract proper node name and alternative node names
node_name_synonyms = {}
for coreference in ex_stanza.corefChain:
    proper_nn = []
    alt_nn = []
    for mention in coreference.mention:
        if mention.mentionType == "NOMINAL" or mention.mentionType == "PROPER":
            # Make the "proper" or "nominal" mention the node label
            node_name_list = [node_part.lemma for node_part in ex_stanza.sentence[mention.sentenceIndex]
                              .token[mention.beginIndex: mention.endIndex]]
            # Concatenate node names that consist of several tokens
            if len(node_name_list) > 1:
                node_name = (' ').join(node_name_list)
            else:
                node_name = node_name_list[0]
            #
            # Append proper node name only if it is different from all other proper node names
            if node_name not in proper_nn:
                proper_nn.append(node_name)
        else:
            alternative_node_name = [node_part.lemma for node_part in ex_stanza.sentence[mention.sentenceIndex]
                                     .token[mention.beginIndex: mention.endIndex] if node_part.lemma not in do_not_match]
            if len(alternative_node_name) > 1:
                alternative_node_name = (' ').join(alternative_node_name)
            else:
                alternative_node_name = alternative_node_name[0]
            #
            # Keep track of sentence the reference appeared in
            alt_nn.append((mention.sentenceIndex, alternative_node_name))
    if proper_nn == []:
        for mention in coreference.mention:
            for token in ex_stanza.sentence[mention.sentenceIndex].token[mention.beginIndex: mention.endIndex]:
                if token.lemma == token.originalText:
                    proper_nn.append(token.originalText)
                    continue
    node_name_synonyms[proper_nn[0]] = alt_nn


# --------------------------------------------------------------------------------------------
# ------- Split nodes that are joined by preposition and add preposition edge to graph -------
for p, preposition_edge in enumerate(preposition_edges):
    preposition = preposition_edge[2]['relation']
    for proper_nn in list(node_name_synonyms.keys()):
        if preposition in proper_nn:
            part1 = proper_nn.split(preposition)[0].strip()
            part2 = proper_nn.split(preposition)[1].strip()
            # print(proper_nn.split(preposition))
            node_name_synonyms[part1] = node_name_synonyms.pop(
                proper_nn)  # Set first part of preposition-joined node name as name
            edges.append(preposition_edge)


for e, edge_info in enumerate(edges):
    edge = edge_info[:2]
    new_edge = list(edge_info)  # Make edge into list to ammend it
    # Make list of nodes that are not current node
    other_edges = [list(x[:2]) for i, x in enumerate(edges) if i != e]
    other_edges = list(chain.from_iterable(other_edges))
    for n, node in enumerate(edge):
        # Test if node includes preposition
        for p, preposition_edge in enumerate(preposition_edges):
            preposition = preposition_edge[2]['relation']
            preposition_match_idx = []
            preposition_match_idx = [m for m, match in enumerate(
                node.split(' ')) if preposition == match]
            match_idx = []
            match_idx = [m for m, match in enumerate(
                node.split(' ')) if preposition == match]
            if match_idx != []:
                m = match_idx[0]
                part1 = (' ').join(node.split(' ')[:m]).strip()
                part2 = (' ').join(node.split(' ')[m:]).strip()
                new_edge[n] = part1
                print(part1, ' \t\t|\t ', part2)
                # If second part of node is anywhere else in edges, then split
                # Find where part1 does not appear in node but part2 appears (something other than prepositions or do_not_match element)
                p2_words = [w for w in part2.split(
                    ' ') if not w in do_not_match]  # remove stopwords
                p2_list = []
                for x in other_edges:
                    for p2 in p2_words:
                        p2_list.append(p2 in x.split(' '))
                p1_words = [w for w in part1.split(
                    ' ') if not w in do_not_match]  # remove stopwords
                p1_list = []
                for x in other_edges:
                    for p1 in p1_words:
                        p1_list.append(p1 not in x.split(' '))
                if any(p1_list and p2_list):
                    print(preposition_edge)
    edges[e] = tuple(new_edge)
    if preposition_edge not in edges:
        edges.append(preposition_edge)

# Clean node names from determiners and other nouns appearing after first noun in the node
for e, edge_info in enumerate(edges):
    edge = edge_info[:2]
    new_edge = list(edge_info)  # Make edge into list to ammend it
    # Make list of nodes that are not current node
    for n, node in enumerate(edge):
        node_noun = [node_part for node_part in node.split()
                     if node_part in nouns]
        node_adjective = [node_part for node_part in node.split()
                          if node_part in adjectives]
        # print('{} : {}  ======= {}'.format(node, node_noun, node_adjective))
        if node_noun != []:
            new_node_name = node_noun[0]
            new_edge[n] = new_node_name
        elif node_noun == [] and node_adjective != []:
            new_node_name = node_adjective[0]
            new_edge[n] = new_node_name
    edges[e] = tuple(new_edge)

# ------------------------------------------------------------------------------
# ------- Merge nodes that are separate mentions of the same entity -------

# Replace node name with proper node name and edge_label
# Method: test if node text appears in list of alternative node names or is part of the proper node name and replace with the full proper node name
orig_edges = deepcopy(edges)

for e, edge_info in enumerate(edges):
    # print(e, edge)
    edge = edge_info[:2]
    sentence_idx_edge = edge_info[2]['sentence']
    new_edge = list(edge_info)  # Make edge into list to ammend it
    for n, node in enumerate(edge):
        #
        found_match = False
        for node_token in node.split(' '):
            if found_match == False:
                if node_token in do_not_match:
                    # If token is a determiner, move on to the next one.
                    continue
                elif node_token in list(node_name_synonyms.keys()):
                    # Replace with proper node name if node is the same as proper node name
                    proper_node_name = list(node_name_synonyms.keys())[
                        list(node_name_synonyms.keys()).index(node_token)]
                    print("Replace \t '{}' \t\t with \t\t'{}' in {}". format(
                        node, proper_node_name, edge))
                    new_edge[n] = proper_node_name
                    found_match = True
                for ann, alternative_mentions in enumerate(list(node_name_synonyms.values())):
                    for sentence_idx_mention, mention in alternative_mentions:
                        # print(sentence_idx_mention, mention)
                        if node_token == mention and sentence_idx_edge == sentence_idx_mention:
                            # Replace with proper node name if node is part of one of the alternative node names
                            proper_node_name = list(
                                node_name_synonyms.keys())[ann]
                            print("Replace \t '{}' \t\t with \t\t'{}' in {}".format(
                                node, proper_node_name, edge))
                            new_edge[n] = proper_node_name
                            found_match = True
            else:
                print('Moving on...')
    edges[e] = tuple(new_edge)


# # ------------------------------------------------------------------------------
# # Save Graphs
# # Initialize output
# output_dir = '/Users/CN/Documents/Projects/Cambridge/data/ex_ollie'
# file_stem = op.splitext(file.split('/')[-1])[0]
# output = op.join(output_dir, 'graph_' + file_stem)
# output_orig = op.join(output_dir, 'graph_orig_' + file_stem)


# # ------------------------------------------------------------------------------
# # Construct Speech Graphs
# G = nx.MultiDiGraph()
G = nx.Graph()
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


# # Original Speech Graph (before merging)
# G = nx.MultiDiGraph()
# G.add_edges_from(orig_edges)
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True,
#         connectionstyle='arc3, rad = 0.1', node_color='white')
# edge_labels = dict([((u, v,), d['relation'])
#                     for u, v, d in G.edges(data=True)])
# nx.draw_networkx_edge_labels(
#     G, pos, edge_labels=edge_labels, font_color='green', font_size=10)
# figure = plt.gcf()
# plt.show()


# # MultiDiGraph
# G = nx.MultiDiGraph()
# G.add_edges_from(edges)
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
# edge_labels = dict([((u, v,), d['relation'])
#                     for u, v, d in G.edges(data=True)])
# nx.draw_networkx_edge_labels(
#     G, pos, edge_labels=edge_labels, font_color='green', font_size=10)
# figure = plt.gcf()
# plt.show()
