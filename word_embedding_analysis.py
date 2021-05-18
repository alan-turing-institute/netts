#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  analyse_graphs.py
#
# Description:
#               Script to analyse semantic speech graphs
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

import warnings
warnings.filterwarnings("ignore")
import os
import os.path as op
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')

# Plotting
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

# Data Processing
import numpy as np
import word2vec as w2v
import collections
import networkx as nx
from stanza.server import CoreNLPClient


# Define functions for word embeddings analysis of semantic speech graphs


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


def find_representative_node_words(graphs, sentence, quiet=True, pos_hierarchy=['NNP', 'NNPS', 'NN', 'NNS', 'PRP', 'PRP$', 'CD', 'PDT', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'DT', 'WDT',
                                                                                'WP', 'WP$', 'WRB', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD', 'UH', 'EX', 'FW', 'IN', 'CC', 'RP', 'TO', 'POS', 'SYM', 'LS']):
    """Finds representative word for all nodes of all graphs.
    Representative word is chosen based on a pre-specified upos tag hierarchy.
    Proper nouns are most representative, then come nouns, pronouns, adjectives, etc.


    Parameters
    ----------
    graphs : list
        list with graph objects
    sentence:   stanza-annotated sentences (equivalent to doc.sentence where doc is an annotated document) 
        each sentence (doc.sentence) contains the concantenated node words of one graph object

    Returns
    -------
    representative_node_words
        dict where the key is the original node words and the value is the representative word for that node

    Dependencies
    -------
    choose_representative_word
        Function that chooses representative words for each node.

    """
    #
    representative_node_words = {}
    for g, G in enumerate(graphs):
        G_node_token_types = [token.pos for token in sentence[g].token]
        G_nodes = list(G.nodes())
        G_nodes_split = []
        for word in G_nodes:
            if len(word.split(' ')) > 1:
                G_nodes_split.extend(word.split(' '))
            else:
                G_nodes_split.append(word)
        for node in G_nodes:
            token_types = []
            if len(node.split(' ')) > 1:
                for node_part in node.split(' '):
                    idx = G_nodes_split.index(node_part)
                    token_types.append(G_node_token_types[idx])
                representative_word = choose_representative_word(
                    node, token_types, pos_hierarchy, quiet)
                representative_node_words[node] = representative_word
    return representative_node_words


def choose_representative_word(node, token_types, pos_hierarchy, quiet=True):
    """Chooses representative word for the node based on the pos tags for each node word.
    Representative word is chosen based on a pre-specified pos tag hierarchy.
    Proper nouns are most representative, then come nouns, pronouns, adjectives, etc.


    Parameters
    ----------
    node : original node words
    token_types: pos tags for each node word in the original node from CoreNLP annotation
    pos_hierarchy : specified hierarchy for pos tags

    Returns
    -------
    representative_word : representative word for that node

    """
    for pos in pos_hierarchy:
        # If upos exists in word types of the node, then pick the respective word as the representative one
        if pos in token_types:
            representative_word_idx = token_types.index(pos)
            representative_word = node.split(' ')[representative_word_idx]
            if not quiet:
                print('{0}\t\t{1}'.format(
                    representative_word, node))
            return representative_word

# word_types = [
#     word.upos for sent in doc.sentences for word in sent.words]
# upos_hierarchy = ['PROPN', 'NOUN', 'PRON', 'ADJ', 'ADV', 'NUM', 'VERB',
#                   'AUX', 'DET', 'SCONJ', 'CCONJ', 'ADP', 'PART', 'INTJ', 'PUNCT', 'SYM', 'X']


def calc_vector_distance_adj(G, model, representative_node_words, quiet=True):
    """Calculates word2vec distance between all adjacent nodes in graph.

    Parameters
    ----------
    G : MultiDiGraph or DiGraph
        A directed graph class that can store multiedges.
    model : word2vec model
        Model was initialised outside the function. Requires word2vec python package and word2vec binary file (setup instructions are in nlp_helper_functions.py)
    representative_node_words : dict
        where the key is the original node words and the value is the representative word for that node


    Returns
    -------
    distance_mean
        mean distance value for all adjacent nodes
    distance_median
        median distance value for all adjacent nodes
    distance_std
        std dev of distances of all adjacent nodes

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
        edge = list(edge)
        # W2v distance can only be calculated between two individual words. If node consists of more than one word, replace with representative node word
        for n, node in enumerate(edge):
            if len(node.split(' ')) > 1:
                edge[n] = representative_node_words[node]
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
    #
    mean_distance = np.nanmean(all_edge_distances)
    median_distance = np.nanmedian(all_edge_distances)
    std_distance = np.nanstd(all_edge_distances)
    return mean_distance, median_distance, std_distance

# --------------------- Central node word2vec distance ---------------------------------------


def central_node_distance(df):
    """Calculates word2vector distance between central node and most frequent central node
        Author: Caroline Nettekoven, crn29@cam.ac.uk

    Parameters
    ----------
    df : pandas dataframe
        Dataframe that holds all graph properties calculated so far.

    Returns
    ----------
    df : pandas dataframe
        Dataframe with distance values added.

    """
    df['distance'] = np.nan
    frequent_words = []
    # Initialise Word2Vec model
    model = w2v.load('word2vec_data/text8.bin')
    for tat in df.tat.cat.categories:
        most_frequent_word, tat_words_filtered = central_words(df, tat)
        frequent_words.append(most_frequent_word)
        # ---- Calculate distance between to most frequent word for all words ---
        distance = calc_vector_distance(
            most_frequent_word, tat_words_filtered, model)
        row_indices = df.index[df.tat == tat].tolist()
        df.loc[row_indices, 'distance'] = distance
    return df


# --------------------- Distance between adjacent nodes (distance_mean) --------------
def adjacent_node_distance(df, graphs):
    """Calculates word2vector distance between all adjacent nodes on 
        Author: Caroline Nettekoven, crn29@cam.ac.uk
        Note: Running this function is not possible when a Jupyter notebook is open at the same time.
        Reason being that CoreNLP tries to run on port 9000, but port 9000 is already taken up by jupyter kernel.
        Setting jupyter to different port does not fix the issue and neither does setting CoreNLP port to a different value.
        This problem appears in several github issues, but none of the suggested fixes has worked so far.
        Workaround for now is to close all open jupyter notebooks and run the function.
        Then save output in pandas dataframe and import dataframe into jupyter notebook for visualisation.

    Parameters
    ----------
    df : pandas dataframe
        Dataframe that holds all graph properties calculated so far.
    graphs: list
        List storing all graph objects

    Returns
    ----------
    df : pandas dataframe
        Dataframe with distance values added.

    """
    df['distance_mean'] = np.nan
    df['distance_median'] = np.nan
    df['distance_std'] = np.nan
    # Initialise Word2Vec model
    model = w2v.load('word2vec_data/text8.bin')
    #
    # --- Find representative word in every node ---
    # concatenate node words of every graph, with graphs seperated by \n\n to be split into seperate sentences by CoreNLP
    nodes_allGraphs = ''
    for G in graphs:
        nodes = list(G.nodes())
        nodes = (' ').join(nodes)
        nodes_allGraphs = nodes_allGraphs + nodes + '\n\n'
    #
    # --- Annotate node words ---
    # Split concatenated nodes into chunks that are manageable by CoreNLP (of max 10000 characters length) while respecting graph boundaries (marked by '\n\n')
    # Step size is chosen somewhat arbitrarily. For our data, the concatenated node labels of 950 graphs are 10000 characters long.
    # To be on the safe side, we chose to concatenate the nodes of 500 graphs in each step.
    # The concatenated node labels of a 500-graph dataset should be well below the character limit of 10000 characters that CoreNLP can handle.
    step = 500
    all_sentences = []
    for i in range(0, len(nodes_allGraphs.split('\n\n')), step):
        # print(i, i+step)
        process_nodes = '\n\n'.join(nodes_allGraphs.split('\n\n')[i:i + step])
        # part-of-speech tag node words
        with CoreNLPClient(properties={'annotators': 'tokenize,ssplit,pos,lemma', 'ssplit.newlineIsSentenceBreak': 'two'}, be_quiet=True) as client:
            doc = client.annotate(process_nodes)
        #
        for sent in doc.sentence:
            all_sentences.append(sent)
    #
    #
    # Get dictionary with one representative words for every node entry on the basis of pos tags
    representative_node_words = find_representative_node_words(
        graphs, all_sentences, quiet=True)
    #
    # ---- Calculate distance between all adjacent nodes in graph ---
    for g, G in enumerate(graphs):
        mean_distance, median_distance, std_distance = calc_vector_distance_adj(
            G, model, representative_node_words, quiet=True)
        df['distance_mean'][g] = mean_distance
        df['distance_median'][g] = median_distance
        df['distance_std'][g] = std_distance
    #
    #
    return df
