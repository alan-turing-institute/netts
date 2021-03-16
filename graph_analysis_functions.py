#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  graph_analysis_functions.py
#
# Description:
#               Functions to analyse semantic speech graphs
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
import networkx as nx
import os
import os.path as op
import pandas as pd
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import datetime
import glob
import re
from pprint import pprint
import seaborn as sns
import word2vec as w2v
import gensim
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import collections
import stanza


def print_bidirectional_edges(G, quiet=True):
    """Prints the bidirectional edges of a directed graph.
        Bidirectional edges are found by:
            # 1) Creating transpose of graph matrix
            # 2) Checking where transpose is equal to original matrix and original matrix has non-zero value

    Parameters
    ----------
    G : MultiDiGraph or DiGraph
        A directed graph class that can store multiedges.
    quiet : bool, optional
        A flag indicating if output message should be muted if graph has no bidirectional edges (default is
        True)

    """
    #
    arr = nx.to_numpy_matrix(G)
    bool_bidirectional_edges = np.logical_and(
        arr != 0, arr == np.transpose(arr)).nonzero()
    n_bidirectional_edges = bool_bidirectional_edges[0].shape[0]
    bidirectional_edges = bool_bidirectional_edges
    if n_bidirectional_edges == 0 and quiet is True:
        return None
    elif n_bidirectional_edges == 0 and quiet is False:
        print(print('\n======= {} =======\nNo bidirectional edges.'.format(
            G.graph['transcript'])))
    nodes = list(G.nodes)
    for e in range(0, n_bidirectional_edges):
        # Ignore self loops
        if bidirectional_edges[0][e] == bidirectional_edges[1][e]:
            return None
        else:
            print('\n======= {} ======='.format(G.graph['transcript']))
            n1 = nodes[bidirectional_edges[0][e]]
            n2 = nodes[bidirectional_edges[1][e]]
            bidirectional_edge_data_1 = G.get_edge_data(n1, n2)
            bidirectional_edge_data_2 = G.get_edge_data(n2, n1)
            for entry in bidirectional_edge_data_1:
                # entry = bidirectional_edge_data[0]
                be = bidirectional_edge_data_1[entry]
                print(
                    '---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(be['sentence'], n1, be['relation'], n2))
            for entry in bidirectional_edge_data_2:
                # entry = bidirectional_edge_data[0]
                be = bidirectional_edge_data_2[entry]
                print(
                    '---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(be['sentence'], n2, be['relation'], n1))


def print_parallel_edges(G, quiet=True):
    """Prints the parallel edges of a directed graph.

    Parameters
    ----------
    G : MultiDiGraph or DiGraph
        A directed graph class that can store multiedges.
    quiet : bool, optional
        A flag indicating if output message should be muted if graph has no parallel edges (default is
        True)

    """
    #
    arr = nx.to_numpy_matrix(G)
    bool_parallel_edges = (arr >= 2)
    n_parallel_edges = np.sum(bool_parallel_edges)
    parallel_edges = np.where(bool_parallel_edges)
    if n_parallel_edges == 0 and quiet is True:
        return
    elif n_parallel_edges == 0 and quiet is not True:
        print(print('\n======= {} =======\nNo parallel edges.'.format(
            G.graph['transcript'])))
    # elif n_parallel_edges == 1:
    #     parallel_edges = np.reshape(parallel_edges, (-1, 2))
    print('\n======= {} ======='.format(G.graph['transcript']))
    nodes = list(G.nodes)
    # parallel_edge = parallel_edges[0]
    for e in range(0, n_parallel_edges):
        n1 = nodes[parallel_edges[0][e]]
        n2 = nodes[parallel_edges[1][e]]
        parallel_edge_data = G.get_edge_data(n1, n2)
        for entry in parallel_edge_data:
            # entry = parallel_edge_data[0]
            pe = parallel_edge_data[entry]
            print(
                '---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(pe['sentence'], n1, pe['relation'], n2))


def get_parallel_edges(G, same_sentence=True):
    """Returns DataFrame with parallel edges of a directed graph.

    Parameters
    ----------
    G : MultiDiGraph or DiGraph
        A directed graph class that can store multiedges.
    same_sentence : bool, optional
        A flag indicating if only parallel edges extracted from the same sentence should be returned (default is
        True)

    Returns
    -------
    pe_df
        A DataFrame including parallel edges and their attributes
            'transcript'    Speech transcript name that graph stems from
            'sent'          Sentence number that edge stems from
            'n1'            Source node
            'relation'      Edge label / Relation
            'n2'            Target node

    """
    #
    # Get parallel edges
    arr = nx.to_numpy_matrix(G)
    bool_parallel_edges = (arr >= 2)
    n_parallel_edges = np.sum(bool_parallel_edges)
    parallel_edges = np.where(bool_parallel_edges)
    if n_parallel_edges == 0:
        return
    # elif n_parallel_edges == 1:
    #     parallel_edges = np.reshape(parallel_edges, (-1, 2))
    nodes = list(G.nodes)
    # parallel_edge = parallel_edges[0]
    G_parallel_edges = []
    for e in range(0, n_parallel_edges):
        n1 = nodes[parallel_edges[0][e]]
        n2 = nodes[parallel_edges[1][e]]
        parallel_edge_data = G.get_edge_data(n1, n2)
        for entry in parallel_edge_data:
            # entry = parallel_edge_data[0]
            pe = parallel_edge_data[entry]
            # print(
            #     '---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(pe['sentence'], n1, pe['relation'], n2))
            G_parallel_edges.append(
                [G.graph['transcript'], pe['sentence'], n1, pe['relation'], n2])
    pe_df = pd.DataFrame(G_parallel_edges, columns=[
        'transcript',
        'sent', 'n1',
        'relation', 'n2'])
    if same_sentence:
        if any(pe_df.duplicated(subset=['sent', 'n1', 'n2'], keep=False)):
            # Return only those parallel edges that have been extracted from the same sentence
            pe_df_same_sentence = pe_df[pe_df.duplicated(
                subset=['sent', 'n1', 'n2'], keep=False)]
            return pe_df_same_sentence
    else:
        # Return all parallel edges
        return pe_df


def central_words(df, tat, ignore_words=['i', 'image', 'picture', 'it']):
    """Returns most frequent word found in the most central node (Node with highest degree centrality) for a specific tat stimulus along with all degree-central node words.

    Parameters
    ----------
    df : DataFrame
        has variables:
            tat                 stimulus picture used for transcript, categorical variable
            max_degree_node     word of node with highest degree centrality, object variable
    tat : int
        stimulus picture used for transcript.
    ignore_words:   words to ignore when filtering the node words, optional

    Returns
    -------
    most_frequent_word
        word that labels the degree-central node most frequently across all graphs for this tat stimulus
    tat_words_filtered
        list of words that label the most degree-central node without stop words (with stop words being superfluous words. So it returns 'man', instead of 'the man')

    """
    # print(tat)
    tat_words = df.query('tat == @tat').max_degree_node
    # ---- Get the most frequent word ---
    stop_words = ['the']
    tat_words_filtered = []
    for i, words in enumerate(tat_words):
        # if len(words[0]) > 1
        for word in words.split(' '):
            filtered = []
            if word not in stop_words:
                filtered.append(word)
            all_filtered = (' ').join(filtered)
        tat_words_filtered.append(all_filtered)
    #
    counted_words = collections.Counter(tat_words_filtered)
    words = []
    counts = []
    for letter, count in counted_words.most_common(10):
        words.append(letter)
        counts.append(count)
    #
    words = [word for word in words if word not in ignore_words]
    most_frequent_word = words[0]
    # frequent_words.append(words[0])
    # return frequent_words
    return most_frequent_word, tat_words_filtered


def calc_vector_distance(most_frequent_word, tat_words_filtered, model):
    """Calculates word2vec distance between most frequent central word and all other central words.

    Parameters
    ----------
    most_frequent_word : str
        Most frequent degree-central node word
    tat_words_filtered : list
        All other degree-central node words in the order at which they appear in the graphs for that tat. 
    model:   word2vec model that was initialised outside the function. Requires word2vec python package and word2vec binary file (setup instructions are in nlp_helper_functions.py)

    Returns
    -------
    distance
        list of distance values

    """
    distance = []
    for current_word in tat_words_filtered:
        try:
            dist = model.distance(most_frequent_word, current_word)
            distance.append(dist[0][2])
        except KeyError:
            print('Word is not in word2vec vocabulary: {}. Setting distance as nan.'.format(
                current_word))
            distance.append(np.nan)
    return distance


def choose_representative_word(edge, nlp, quiet=True):
    """Chooses representative word for both nodes of an edge.
    Representative word is chosen based on a pre-specified upos tag hierarchy.
    Proper nouns are most representative, then come nouns, pronouns, adjectives, etc.


    Parameters
    ----------
    edge : tuple
        Edge for which representative node words should be chosen.
    nlp:   stanza nlp pipeline

    Returns
    -------
    edge
        list containing the two nodes which now consist of their representative word only

    """
    # TODO: Fix representative word choosing. At the moment, some representative words are numbers
    for idx, node in enumerate(edge):
        #
        if len(node.split(' ')) > 1:
            edge = list(edge)
            doc = nlp(node)
            #
            word_types = [
                word.upos for sent in doc.sentences for word in sent.words]
            upos_hierarchy = ['PROPN', 'NOUN', 'PRON', 'ADJ', 'ADV', 'NUM', 'VERB',
                              'AUX', 'DET', 'SCONJ', 'CCONJ', 'ADP', 'PART', 'INTJ', 'PUNCT', 'SYM', 'X']
            for upos in upos_hierarchy:
                # If upos exists in word types of the node, then pick the respective word as the representative one
                if upos in word_types:
                    representative_word_idx = word_types.index(upos)
                    representative_word = doc.sentences[0].words[representative_word_idx].text
                    edge[idx] = representative_word
                    if not quiet:
                        print('Chose {0} as representative word for {1}'.format(
                            representative_word, node))
                    continue
    return edge


def calc_vector_distance_all(G, model, nlp, quiet=True):
    """Calculates word2vec distance between all adjacent nodes in graph.

    Parameters
    ----------
    G : MultiDiGraph or DiGraph
        A directed graph class that can store multiedges.
    model:   word2vec model that was initialised outside the function. Requires word2vec python package and word2vec binary file (setup instructions are in nlp_helper_functions.py)
    nlp:   stanza nlp pipeline for choosing representative node word

    Returns
    -------
    distance
        mean distance value for all adjacent nodes

    Dependencies
    -------
    choose_representative_word
        Requires function that chooses representative words for each node.

    """
    # Construct basic graph without multi edges
    G_basic = nx.Graph()
    edges = list(G.edges())
    G_basic.add_edges_from(edges)
    # Remove self loops
    G_basic.remove_edges_from(nx.selfloop_edges(G_basic))
    # Get distances
    all_edge_distances = []
    for edge in list(G_basic.edges()):
        edge = choose_representative_word(edge, nlp)
        try:
            dist = model.distance(edge[0], edge[1])
            d = dist[0][2]
            all_edge_distances.append(d)
            if not quiet:
                print('\n{} || {}: \t\t{}'.format(
                    edge[0], edge[1], d))
        except KeyError:
            all_edge_distances.append(np.nan)
            if not quiet:
                print('\n{} || {}: \t\t{}'.format(
                    edge[0], edge[1], 'Not in vocabulary'))
    mean_distance = np.nanmean(all_edge_distances)
    return mean_distance
