#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  visualise_paragraph_functions.py
#
# Description:
#               Functions to visualise sentence using OpenIE5 and Stanford CoreNLP
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
# TO DO
#   - Sanity check: Is each relation represented only once in the edge? (Also check parallel edges in multiedge graph)
#   - Plot graphs coloured by confidence / extraction type
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
# Find edges and edge labels extracted by OpenIE5


def create_edges_ollie(ex_ollie):
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
    print('++++ Created {} edges (ollie) ++++'.format(len(ollie_edges)))
    return ollie_edges, ollie_edges_text_excerpts, ollie_one_node_edges, ollie_one_node_edges_text_excerpts


def create_edges_stanza(ex_stanza):
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
            stanza_edges_text_excerpts.append(
                (' ').join([node1, relation, node2]))
    print('++++ Created {} edges (stanza) ++++'.format(len(stanza_edges)))
    return stanza_edges, stanza_edges_text_excerpts

# ------------------------------------------------------------------------------
# ------- Get word types -------
# First extract a list of determiners present in the text that need to be ignored when matching (You don't want to match "the picture" and "the dog" on "the")


def get_word_types(ex_stanza):
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
                    nouns_origtext.append(token.word.lower())
            # Add everything that is not noun to list of words that should not get merged on later
            else:
                if token.lemma not in no_noun:
                    # print(token.lemma, ' \t', token.pos)
                    if token.pos == "PRP$":
                        # Lemma for poss pronoun 'his' is 'he', but 'he' counts as noun, therefore add orginial text for poss pronoun
                        no_noun.append(token.word.lower())
                        poss_pronouns.append(token.word.lower())
                    else:
                        no_noun.append(token.lemma)
                # get determiners
                if token.pos == "DT" and token.lemma not in dts:
                    dts.append(token.lemma)
                # get adjectives
                elif token.pos == "JJ" and token.lemma not in adjectives:
                    adjectives.append(token.lemma)
    print('++++ Obtained word types ++++')
    return no_noun, poss_pronouns, dts, nouns, nouns_origtext, adjectives

# # ------- Extract adjective relations -------


def get_adj_edges(ex_stanza):
    adjectives = []
    adjective_edges = []
    for idx_sentence, sentence in enumerate(ex_stanza.sentence):
        for word in sentence.enhancedDependencies.edge:
            if word.dep.split(':')[0] == 'amod':
                # elif word.dep.split(':')[0] == 'advmod':
                source_idx = word.source - 1
                target_idx = word.target - 1
                # Test if source word is plural
                if sentence.token[source_idx].lemma == sentence.token[source_idx].word.lower():
                    relation = 'is'
                else:
                    relation = 'are'
                relation = '(' + relation + ')'
                source_word = sentence.token[source_idx].word.lower()
                target_word = sentence.token[target_idx].word.lower()
                # if sentence.token[target_idx].pos == ""
                # print('{}'.format((' ').join(
                #     [token.word.lower() for token in sentence.token if token.word.lower()])))
                print(' {} {} {}'.format(
                    sentence.token[source_idx].word.lower(), relation, sentence.token[target_idx].word.lower()))
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
        print('++++ Created {} adj edges ++++'.format(len(adjective_edges)))
        return adjectives, adjective_edges

# ------------------------------------------------------------------------------
# ------- Extract preposition relations -------
# Separate any preposition relations in node name synonyms


def get_prep_edges(ex_stanza):
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
                source_word = sentence.token[source_idx].word.lower()
                target_word = sentence.token[target_idx].word.lower()
                # print('{}'.format((' ').join(
                #     [token.word.lower() for token in sentence.token if token.word.lower()])))
                # print(' {} {} {}'.format(
                #     sentence.token[source_idx].word.lower(), preposition, sentence.token[target_idx].word.lower()))
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
    print('++++ Created {} preposition edges ++++'.format(len(preposition_edges)))
    return prepositions, preposition_edges

# ------------------------------------------------------------------------------
# ------- Extract oblique relations -------
# Get a list of obliques and track where they point to
# N.B. The oblique relation is used for a nominal (noun, pronoun, noun phrase) functioning as a non-core (oblique) argument or adjunct.
# This means that it functionally corresponds to an adverbial attaching to a verb, adjective or other adverb.
# More info: https://universaldependencies.org/u/dep/obl.html
# Example: 'The cat was chased by the dog.' Cat --obl--> dog


def get_obl_edges(ex_stanza):
    obliques = []
    oblique_edges = []
    for idx_sentence, sentence in enumerate(ex_stanza.sentence):
        for word in sentence.enhancedDependencies.edge:
            if word.dep.split(':')[0] == 'obl':
                source_idx = word.source - 1
                target_idx = word.target - 1
                extractor_type = 'oblique'
                oblique = word.dep.split(':')[1]
                source_word = sentence.token[source_idx].word.lower()
                target_word = sentence.token[target_idx].word.lower()
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
    print('++++ Created {} oblique edges ++++'.format(len(oblique_edges)))
    return obliques, oblique_edges

# ------------------------------------------------------------------------------
# ------- Add oblique relations that were also extracted by ollie -------


def add_obl_edges(edges, oblique_edges):
    for oblique_edge in oblique_edges:
        oblique_edge_text = (' ').join(
            [oblique_edge[2]['relation'], oblique_edge[1]])
        # print(oblique_edge_text)
        for edge_info in edges:
            if not edge_info[2]['node2_args'] == []:
                # print(oblique_edge[0])
                # print(edge_info[2]['node2_args'][0])
                if edge_info[2]['relation'] == oblique_edge[0] and edge_info[2]['node2_args'][0] == oblique_edge_text:
                    print('{} : {} \t {} : {}'.format(
                        edge_info[2]['relation'], oblique_edge[0], edge_info[2]['node2_args'][0], oblique_edge_text))
                    new_oblique_edge = (edge_info[1], oblique_edge[1], {
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
    print('++++ Added {} oblique edges. Total edges: {} ++++'.format(len(oblique_edges), len(edges)))
    return edges

# ------------------------------------------------------------------------------
# ------- Find node name synonyms in coreference chain -------
# Extract proper node name and alternative node names


def get_node_synonyms(ex_stanza, no_noun):
    node_name_synonyms = {}
    for coreference in ex_stanza.corefChain:
        proper_nn = []
        alt_nn = []
        for mention in coreference.mention:
            mention_info = ex_stanza.sentence[mention.sentenceIndex].token[mention.beginIndex: mention.endIndex]
            if mention.mentionType == "NOMINAL" or mention.mentionType == "PROPER":
                # Make the "proper" or "nominal" mention the node label
                node_name_list = [
                    node_part.word.lower() for node_part in mention_info if not node_part.pos == 'PRP$']
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
                alternative_node_name = [
                    node_part.word.lower() for node_part in mention_info if node_part.word.lower() not in no_noun]
                if len(alternative_node_name) > 1:
                    alternative_node_name = (' ').join(alternative_node_name)
                elif alternative_node_name != []:
                    alternative_node_name = alternative_node_name[0]
                elif alternative_node_name == [] and len(mention_info) == 1 and mention_info[0].pos[0:3] == 'PRP':
                    # Mentions that only consist of one possessive pronoun are still valid mentions ("my"/"me" should be merged with "I").
                    # (But mentions that consist of a pronoun plus another noun should be cleaned of the pronoun ("his hands" should only be merged with another mention of "hands", and not with another mention of "him").)
                    alternative_node_name = mention_info[0].word.lower()
                #
                # Keep track of sentence the reference appeared in
                alt_nn.append((mention.sentenceIndex, alternative_node_name))
        if proper_nn == []:
            for mention in coreference.mention:
                mention_info = ex_stanza.sentence[mention.sentenceIndex].token[mention.beginIndex: mention.endIndex]
                for token in mention_info:
                    if token.lemma.lower() == token.word.lower():
                        proper_nn.append(token.lemma.lower())
                        continue
        node_name_synonyms[proper_nn[0]] = alt_nn
    print('++++ Obtained {} node synonyms ++++'.format(len(node_name_synonyms)))
    return node_name_synonyms


# --------------------------------------------------------------------------------------------
# ------- Split nodes in node_name_synonyms -------
# splits nodes that are joined by preposition and adds preposition edge to graph
def split_node_synonyms(node_name_synonyms, preposition_edges, edges):
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
    print('++++ Split node name synonyms on prepositions. ++++')
    return edges, node_name_synonyms


# --------------------------------------------------------------------------------------------
# ------- Split nodes in edges -------
# Find nodes that include preposition-joined nouns and split the nodes if the second noun appears in any other edge but the current

def split_nodes(edges, preposition_edges, no_noun):
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
    print('++++ Split nodes on prepositions. ++++')
    return edges


# ------------------------------------------------------------------------------
# ------- Merge coreferenced nodes -------
# Merge nodes that are separate mentions of the same entity using the coreference relations chain
# Replace node name with proper node name and edge_label
# Method: test if node text appears in list of alternative node names or is part of the proper node name and replace with the full proper node name


def merge_corefs(edges, node_name_synonyms, no_noun):
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
                        print("Replace '{}' with '{}' in \t {}". format(
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
                                print("Replace '{}' with '{}' in \t {}".format(
                                    node, proper_node_name, edge))
                                new_edge[n] = proper_node_name
                                found_match = True
                else:
                    print('Moving on...')
        edges[e] = tuple(new_edge)
    print('++++ Merged nodes that are referenced several times. ++++')
    return edges, orig_edges


# --------------------------------------------------------------------------------------------
# ------- Clean nodes -------
# Clean node names from determiners, adjectives and other nouns appearing after first noun in the node


def clean_nodes(edges, nouns, adjectives):
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
    print('++++ Cleaned nodes. ++++')
    return edges


# --------------------------------------------------------------------------------------------
# ------- Add adjective edges


def add_adj_edges(edges, adjective_edges, add_adjective_edges):
    if add_adjective_edges:
        for adjective_edge in adjective_edges:
            edges.append(adjective_edge)
    print('++++ Added adjective edges: {} ++++'.format(add_adjective_edges))
    return edges


# edges = add_adj_edges(edges, adjective_edges, add_adjective_edges=True)

# --------------------------------------------------------------------------------------------
# ------- Add all other preposition edges


def add_prep_edges(edges, preposition_edges, add_all_preposition_edges):
    if add_all_preposition_edges:
        for preposition_edge in preposition_edges:
            if preposition_edge not in edges:
                edges.append(preposition_edge)
    print('++++ Added all preposition edges: {} ++++'.format(add_all_preposition_edges))
    return edges


# --------------------------------------------------------------------------------------------
# ------- Get list of connected and unconnected nodes -------

def get_unconnected_nodes(edges, orig_edges, nouns):
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
    print('++++ Obtained unconnected nodes ++++')
    return unconnected_nodes
