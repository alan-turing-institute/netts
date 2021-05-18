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
import numpy as np


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
        return n_bidirectional_edges
    elif n_bidirectional_edges == 0 and quiet is False:
        print(print('\n======= {} =======\nNo bidirectional edges.'.format(
            G.graph['transcript'])))
    nodes = list(G.nodes)
    for e in range(0, n_bidirectional_edges):
        # Ignore self loops
        if bidirectional_edges[0][e] == bidirectional_edges[1][e]:
            return n_bidirectional_edges
        else:
            if quiet is not True:
                print('\n======= {} ======='.format(G.graph['transcript']))
            n1 = nodes[bidirectional_edges[0][e]]
            n2 = nodes[bidirectional_edges[1][e]]
            bidirectional_edge_data_1 = G.get_edge_data(n1, n2)
            bidirectional_edge_data_2 = G.get_edge_data(n2, n1)
            for entry in bidirectional_edge_data_1:
                # entry = bidirectional_edge_data[0]
                be = bidirectional_edge_data_1[entry]
                if quiet is not True:
                    print(
                        '---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(be['sentence'], n1, be['relation'], n2))
            for entry in bidirectional_edge_data_2:
                # entry = bidirectional_edge_data[0]
                be = bidirectional_edge_data_2[entry]
                if quiet is not True:
                    print(
                        '---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(be['sentence'], n2, be['relation'], n1))
    return n_bidirectional_edges


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
    if quiet is not True:
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
            if quiet is not True:
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
