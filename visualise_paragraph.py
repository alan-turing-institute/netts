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
#   - Instead of merging all of the arg2s text together, take advantage of the separation of the second node into parts: is there an edge between the parts? If so, add that edge
#   - Merge on either plural or singular nodes
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

# ------------------------------------------------------------------------------
# Get sentence
selected_file = 2
data_dir = '/Users/CN/Documents/Projects/Cambridge/data'
input_file = op.join(
    data_dir, 'Kings', 'Prolific_pilot_all_transcripts', files[selected_file])
with open(input_file, 'r') as fh:
    orig_text = fh.read()

# orig_text = 'we show images to patients and ask them to describe them'
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
# with CoreNLPClient(
#         annotators=['tokenize', 'ssplit', 'pos', 'lemma',
#                     'ner', 'parse', 'depparse', 'coref', 'openie'],
#         timeout=30000,
#         memory='16G') as client:
#     ex_stanza = client.annotate(text)

with CoreNLPClient(properties={
    'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,coref,openie',
    'pos.model': '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/OpenIE-standalone/target/streams/$global/assemblyOption/$global/streams/assembly/8a3bd51fe5c1bb09a51f326fa358947f6dc78463_8e7f18d9ae73e8daf5ee4d4e11167e10f8827888_da39a3ee5e6b4b0d3255bfef95601890afd80709/edu/stanford/nlp/models/pos-tagger/english-bidirectional/english-bidirectional-distsim.tagger'
}) as client:
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
ollie_one_node_edges = []
ollie_one_node_edges_text_excerpts = []
# Create nodes and edges
for e, extract_val in enumerate(list(ex_ollie.values())):
    if extract_val != []:
        for extract in extract_val:
            # Get node 1
            node1 = extract['extraction']['arg1']['text']
            node1 = node1.lower().strip()
            # Get relation
            relation = extract['extraction']['rel']['text'].lower().strip()
            # Get additional info
            context = extract['extraction']['context']
            if context != None:
                context = context['text']
            # Get node 2
            node2 = ''
            node2_args = []
            #
            # Concatenate all text of argument 2
            for arg2_no, arg2 in enumerate(extract['extraction']['arg2s']):
                # print(arg2_no, arg2['text'])
                # node2 = node2 + ' ' + arg2['text']
                node2_args.append(arg2['text'])
                # print(node2)
            edge_text = (' ').join([node1, relation])
            if not node2_args:
                ollie_one_node_edges_text_excerpts.append(edge_text)
                a = (node1, '', {'relation': relation,
                                 'confidence': extract['confidence'],
                                 'context': context,
                                 'negated': extract['extraction']['negated'],
                                 'passive': extract['extraction']['passive'],
                                 'extractor': 'ollie',
                                 'sentence': e,
                                 })
                ollie_one_node_edges.append(a)
            else:
                node2 = node2_args[0]
                node2_args.pop(0)
                # Add nodes (arg1, arg2 and relationship)
                node2 = node2.lower().strip()
                edge_text = (' ').join([node1, relation, node2])
                # If edge has two nodes and is not duplicate of previous edge, add edge
                if edge_text not in ollie_edges_text_excerpts:
                    # ollie_edges.append([node1, node2])
                    ollie_edges_text_excerpts.append(edge_text)
                    a = (node1, node2, {'relation': relation,
                                        'confidence': extract['confidence'],
                                        'context': context,
                                        'negated': extract['extraction']['negated'],
                                        'passive': extract['extraction']['passive'],
                                        'extractor': 'ollie',
                                        'sentence': e,
                                        'node2_args': node2_args
                                        })
                    ollie_edges.append(a)
                    # print('Discarding edge without second node: \t  {} || {} '.format(
                    # node1, relation))


edges = ollie_edges


# Find edges and edge labels extracted by Stanza OpeniIE
stanza_edges = []
stanza_edges_text_excerpts = []
for sentence in ex_stanza.sentence:
    for triple in sentence.openieTriple:
        node1 = triple.subject.lower()
        node2 = triple.object.lower()
        relation = triple.relation.lower()
        sentence_idx = triple.subjectTokens[0].sentenceIndex
        a = (node1, node2, {'relation': relation,
                            # 'confidence': extract['confidence'],
                            # 'context': context,
                            # 'negated': extract['extraction']['negated'],
                            # 'passive': extract['extraction']['passive'],
                            'extractor': 'stanza',
                            'sentence': sentence_idx
                            })
        stanza_edges.append(a)
        stanza_edges_text_excerpts.append((' ').join([node1, relation, node2]))

# # Print stanza edges that are not already extracted by Ollie (to see if they add anything):
# for stan in stanza_edges:
#     edge_found = False
#     for oll in ollie_edges:
#         if stan[0] in oll[0] and stan[1] in oll[1] and stan[2]['relation'] in oll[2]['relation']:
#             # print((' ').join([stan[0], stan[1], stan[2]['relation']]), ' \t\t: \t\t', (' ').join(
#             #     [oll[0], oll[1], oll[2]['relation']]))
#             edge_found = True
#     if edge_found == False:
#         print('{} \t==========\t {} \t==========>\t {}'.format(
#             stan[0], stan[2]['relation'], stan[1]))


# ------------------------------------------------------------------------------
# ------- Get word types -------
# First extract a list of determiners present in the text that need to be ignored when matching (You don't want to match "the picture" and "the dog" on "the")
no_noun = []
poss_pronouns = []
dts = []
nouns = []
nouns_origtext = []
adjectives = []

for sentence in ex_stanza.sentence:
    for token in sentence.token:
        # get nouns (proxy for nodes)
        if token.pos == "PRP" or token.pos == "NN" or token.pos == "NNS":
            if token.lemma not in nouns:
                nouns.append(token.lemma)
                nouns_origtext.append(token.originalText)
        # Add everything that is not noun to list of words that should not get merged on later
        else:
            if token.lemma not in no_noun:
                # print(token.lemma, ' \t', token.pos)
                if token.pos == "PRP$":
                    # Lemma for poss pronoun 'his' is 'he', but 'he' counts as noun, therefore add orginial text for poss pronoun
                    no_noun.append(token.originalText)
                    poss_pronouns.append(token.originalText)
                else:
                    no_noun.append(token.lemma)
            # get determiners
            if token.pos == "DT" and token.lemma not in dts:
                dts.append(token.lemma)
            # get adjectives
            elif token.pos == "JJ" and token.lemma not in adjectives:
                adjectives.append(token.lemma)

# # ------- Extract adjective relations -------
# for adjective_edge in adjective_edges:
#     edges.append(adjective_edge)
adjectives = []
adjective_edges = []
for idx_sentence, sentence in enumerate(ex_stanza.sentence):
    for word in sentence.enhancedDependencies.edge:
        if word.dep.split(':')[0] == 'amod':
            # elif word.dep.split(':')[0] == 'advmod':
            source_idx = word.source - 1
            target_idx = word.target - 1
            # Test if source word is plural
            if sentence.token[source_idx].lemma == sentence.token[source_idx].originalText:
                relation = 'is'
            else:
                relation = 'are'
            relation = '(' + relation + ')'
            source_word = sentence.token[source_idx].originalText
            target_word = sentence.token[target_idx].originalText
            # if sentence.token[target_idx].pos == ""
            # print('{}'.format((' ').join(
            #     [token.originalText for token in sentence.token if token.originalText])))
            print(' {} {} {}'.format(
                sentence.token[source_idx].originalText, relation, sentence.token[target_idx].originalText))
            adjective_info = (source_word, target_word, {'relation': relation,
                                                         #    'confidence': None,
                                                         #    'context': None,
                                                         #    'negated': None,
                                                         #    'passive': None,
                                                         'extractor': 'adjective',
                                                         'sentence': idx_sentence
                                                         })
            if target_word not in adjectives:
                adjectives.append(target_word)
            adjective_edges.append(adjective_info)


# ------------------------------------------------------------------------------
# ------- Extract preposition relations -------
# Separate any preposition relations in node name synonyms

# Get a list of prepositions and track where they point to
prepositions = []
preposition_edges = []

for idx_sentence, sentence in enumerate(ex_stanza.sentence):
    for word in sentence.enhancedDependencies.edge:
        if word.dep.split(':')[0] == 'nmod':
            source_idx = word.source - 1
            target_idx = word.target - 1
            extractor_type = 'preposition'
            preposition = word.dep.split(':')[1]
            if preposition == 'poss':
                preposition = '(of) [poss]'
                extractor_type = 'possession'
            source_word = sentence.token[source_idx].originalText
            target_word = sentence.token[target_idx].originalText
            # print('{}'.format((' ').join(
            #     [token.originalText for token in sentence.token if token.originalText])))
            # print(' {} {} {}'.format(
            #     sentence.token[source_idx].originalText, preposition, sentence.token[target_idx].originalText))
            # Do not extract "kind of". Leads to cluttering.
            if source_word != 'kind' and preposition != 'of':
                preposition_info = (source_word, target_word, {'relation': preposition,
                                                               #    'confidence': None,
                                                               #    'context': None,
                                                               #    'negated': None,
                                                               #    'passive': None,
                                                               'extractor': extractor_type,
                                                               'sentence': idx_sentence
                                                               })
                prepositions.append(preposition)
                preposition_edges.append(preposition_info)


# ------------------------------------------------------------------------------
# ------- Extract oblique relations -------
# Get a list of obliques and track where they point to
obliques = []
oblique_edges = []

for idx_sentence, sentence in enumerate(ex_stanza.sentence):
    for word in sentence.enhancedDependencies.edge:
        if word.dep.split(':')[0] == 'obl':
            source_idx = word.source - 1
            target_idx = word.target - 1
            extractor_type = 'oblique'
            oblique = word.dep.split(':')[1]
            source_word = sentence.token[source_idx].originalText
            target_word = sentence.token[target_idx].originalText
            oblique_info = (source_word, target_word, {'relation': oblique,
                                                       #    'confidence': None,
                                                       #    'context': None,
                                                       #    'negated': None,
                                                       #    'passive': None,
                                                       'extractor': extractor_type,
                                                       'sentence': idx_sentence
                                                       })
            obliques.append(oblique)
            oblique_edges.append(oblique_info)


# ------------------------------------------------------------------------------
# ------- Add oblique relations that were also extracted by ollie -------
for o, oblique_edge in enumerate(oblique_edges):
    oblique_edge_text = (' ').join(
        [oblique_edge[2]['relation'], oblique_edge[1]])
    for e, edge_info in enumerate(edges):
        edge = edge_info[:2]
        if edge_info[2]['relation'] == oblique_edge[0] and edge_info[2]['node2_args'][0] == oblique_edge_text:
            print('{} : {} \t {} : {}'.format(
                edge_info[2]['relation'], oblique_edge[0], edge_info[2]['node2_args'][0], oblique_edge_text))
            new_oblique_edge = (edge[1], oblique_edge[1], {
                'relation': oblique_edge[2]['relation'],
                #    'confidence': None,
                #    'context': None,
                #    'negated': None,
                #    'passive': None,
                'extractor': 'oblique',
                'sentence': oblique_edge[2]['sentence']
            })
            if new_oblique_edge not in edges:
                edges.append(new_oblique_edge)

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
                              .token[mention.beginIndex: mention.endIndex] if not node_part.pos == 'PRP$']
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
                                     .token[mention.beginIndex: mention.endIndex] if node_part.lemma not in no_noun]
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
# ------- Split nodes in node_name_synonyms -------
# splits nodes that are joined by preposition and adds preposition edge to graph
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


# --------------------------------------------------------------------------------------------
# ------- Split nodes in edges -------
# Find nodes that include preposition-joined nouns and split the nodes if the second noun appears in any other edge but the current
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
                node.split(' ')) if preposition == match and m > 1]
            if match_idx != []:
                m = match_idx[0]
                part1 = (' ').join(node.split(' ')[:m]).strip()
                part2 = (' ').join(node.split(' ')[m:]).strip()
                new_edge[n] = part1
                print(part1, ' \t\t|\t ', part2)
                # If second part of node is anywhere else in edges, then split
                # Find where part1 does not appear in node but part2 appears (something other than prepositions or no_noun element)
                p2_words = [w for w in part2.split(
                    ' ') if not w in no_noun]  # remove stopwords
                p2_list = []
                for x in other_edges:
                    for p2 in p2_words:
                        p2_list.append(p2 in x.split(' '))
                p1_words = [w for w in part1.split(
                    ' ') if not w in no_noun]  # remove stopwords
                p1_list = []
                for x in other_edges:
                    for p1 in p1_words:
                        p1_list.append(p1 not in x.split(' '))
                if any(p1_list and p2_list):
                    print(preposition_edge)
            edges[e] = tuple(new_edge)
            if preposition_edge not in edges:
                edges.append(preposition_edge)


# ------------------------------------------------------------------------------
# ------- Merge coreferenced nodes -------
# Merge nodes that are separate mentions of the same entity using the coreference relations chain
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
                if node_token in no_noun:
                    # If token is anything other than a noun, move on to the next one.
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


# --------------------------------------------------------------------------------------------
# ------- Clean nodes -------
# Clean node names from determiners, adjectives and other nouns appearing after first noun in the node
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

# --------------------------------------------------------------------------------------------
# ------- Add adjective edges
add_adjective_edges = False
if add_adjective_edges:
    for adjective_edge in adjective_edges:
        edges.append(adjective_edge)

# --------------------------------------------------------------------------------------------
# ------- Add all other preposition edges
add_all_preposition_edges = True
if add_all_preposition_edges:
    for preposition_edge in preposition_edges:
        if preposition_edge not in edges:
            edges.append(preposition_edge)

# # ------------------------------------------------------------------------------
# ------- Get list of current and original nodes -------
list_of_nodes = []
for edge in edges:
    list_of_nodes.extend([edge[0], edge[1]])

for orig_edge in orig_edges:
    list_of_nodes.extend([orig_edge[0], orig_edge[1]])

# # ------------------------------------------------------------------------------
# ------- Get list of unconnected nodes -------
unconnected_nodes = []
for n, noun in enumerate(nouns):
    node_is_in_network = any(noun.lower() in node.lower()
                             for node in list_of_nodes)
    if not node_is_in_network:
        unconnected_nodes.append(noun)


# # ------------------------------------------------------------------------------
# # Construct Speech Graphs
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


# MultiDiGraph
G = nx.MultiDiGraph()
G.add_edges_from(edges)
font_size = 10
node_size = 2000
add_unconnected_nodes = False
if add_unconnected_nodes:
    G.add_nodes_from(unconnected_nodes)  # Add unconnected nodes

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, edge_color='black',
        node_color='pink', connectionstyle='arc3, rad = 0.1', font_size=font_size, node_size=node_size)
edge_labels = dict([((u, v,), d['relation'])
                    for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_color='black', font_size=font_size)
figure = plt.gcf()
plt.show()


# # Colour edges by extractor
# G = nx.MultiDiGraph()
# G.add_edges_from(edges)
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True, edge_color='black',
#         node_color='pink', connectionstyle='arc3, rad = 0.1')
# # edges
# # nx.draw_networkx_edges(G, pos, with_labels = True, width=1.0, alpha=0.5)
# edge_labels = dict([((u, v,), d['relation'])
#                     for u, v, d in G.edges(data=True)])
# extracted_by_ollie =
# nx.draw_networkx_edges(
#     G,
#     pos,
#     edgelist=,
#     width=8,
#     alpha=0.5,
#     edge_color="r",
# )
# edge_labels = dict([((u, v,), d['relation'])
#                     for u, v, d in G.edges(data=True)])
# nx.draw_networkx_edges(
#     G,
#     pos,
#     edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
#     width=8,
#     alpha=0.5,
#     edge_color="b",
#     connectionstyle='arc3, rad = 0.1'
# )


# edge_labels = dict([((u, v,), d['relation'])
#                     for u, v, d in G.edges(data=True)])
# nx.draw_networkx_edge_labels(
#     G, pos, edge_labels=edge_labels, font_color='black', font_size=10)
# figure = plt.gcf()
# plt.show()
# # ------------------------------------------------------------------------------
# # Save Graphs
# # Initialize output
# output_dir = '/Users/CN/Documents/Projects/Cambridge/data/ex_ollie'
# file_stem = op.splitext(file.split('/')[-1])[0]
# output = op.join(output_dir, 'graph_' + file_stem)
# output_orig = op.join(output_dir, 'graph_orig_' + file_stem)
