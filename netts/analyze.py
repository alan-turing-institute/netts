#!//env python
# ------------------------------------------------------------------------------
# Script name:  analyze.py
#
# Description:
#               Functions to analyse semantic speech graphs
#
# Author:       Caroline Nettekoven, 2023
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
import networkx as nx
import os
import pandas as pd
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
import numpy as np
import pickle


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
        A flag indicating if output message should be muted if graph has no bidirectional edges (default is True)

    """
    arr = nx.to_numpy_matrix(G)
    bool_bidirectional_edges = np.logical_and(
        arr != 0, arr == np.transpose(arr)).nonzero()
    n_bidirectional_edges = bool_bidirectional_edges[0].shape[0]
    bidirectional_edges = bool_bidirectional_edges
    if n_bidirectional_edges == 0 and quiet:
        return n_bidirectional_edges
    elif n_bidirectional_edges == 0 and not quiet:
        print(print('\n======= {} =======\nNo bidirectional edges.'.format(
            G.graph['transcript'])))
    nodes = list(G.nodes)
    for e in range(n_bidirectional_edges):
        if bidirectional_edges[0][e] == bidirectional_edges[1][e]:
            return n_bidirectional_edges
        if not quiet:
            print('\n======= {} ======='.format(G.graph['transcript']))
        n1 = nodes[bidirectional_edges[0][e]]
        n2 = nodes[bidirectional_edges[1][e]]
        bidirectional_edge_data_1 = G.get_edge_data(n1, n2)
        bidirectional_edge_data_2 = G.get_edge_data(n2, n1)
        for entry in bidirectional_edge_data_1:
            be = bidirectional_edge_data_1[entry]
            if not quiet:
                print('---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(
                    be['sentence'], n1, be['relation'], n2))
        for entry in bidirectional_edge_data_2:
            be = bidirectional_edge_data_2[entry]
            if not quiet:
                print('---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(
                    be['sentence'], n2, be['relation'], n1))
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
    arr = nx.to_numpy_matrix(G)
    bool_parallel_edges = (arr >= 2)
    n_parallel_edges = np.sum(bool_parallel_edges)
    if n_parallel_edges == 0 and quiet:
        return
    transcript = G.graph['transcript']
    if not quiet:
        print(f"\n======= {transcript} =======")
    for i, j in zip(*np.where(bool_parallel_edges)):
        n1, n2 = list(G.nodes())[i], list(G.nodes())[j]
        for entry in G.get_edge_data(n1, n2):
            pe = G.get_edge_data(n1, n2)[entry]
            if not quiet:
                print('---------------------------------\n{0} \t{1} \t{2} \t{3}'.format(
                    pe['sentence'], n1, pe['relation'], n2))


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
    arr = nx.to_numpy_matrix(G)
    bool_parallel_edges = (arr >= 2)
    n_parallel_edges = np.sum(bool_parallel_edges)
    if n_parallel_edges == 0:
        return
    G_parallel_edges = []
    for i, j in zip(*np.where(bool_parallel_edges)):
        n1, n2 = list(G.nodes())[i], list(G.nodes())[j]
        for entry in G.get_edge_data(n1, n2):
            pe = G.get_edge_data(n1, n2)[entry]
            G_parallel_edges.append(
                [G.graph['transcript'], pe['sentence'], n1, pe['relation'], n2])
    pe_df = pd.DataFrame(G_parallel_edges, columns=[
        'transcript',
        'sent', 'n1',
        'relation', 'n2'])
    if same_sentence:
        pe_df = pe_df[pe_df.duplicated(
            subset=['sent', 'n1', 'n2'], keep=False)]
    return pe_df


def calculate_basic_descriptors(G):
    """
    Calculates basic descriptors of the graph.

    Args:
        G (nx.Graph): A networkx graph.

    Returns:
        Tuple: A tuple containing:
            - n_words (int): The number of words in the graph.
            - n_sents (int): The number of sentences in the graph.
            - n_nodes (int): The number of nodes in the graph.
            - n_edges (int): The number of edges in the graph.
            - n_unconnected_nodes (int): The number of unconnected nodes in the graph.
            - average_total_degree (float): The average total degree of the nodes in the graph.
    """

    n_words = G.graph['tokens']
    n_sents = G.graph['sentences']
    mean_sentence_length = int(n_words) / int(n_sents)
    n_nodes = len(G.nodes())
    n_edges = G.size()
    n_unconnected_nodes = len(G.graph['unconnected_nodes'])
    average_total_degree = (n_edges * 2) / n_nodes
    return (n_words, n_sents, n_nodes, n_edges, n_unconnected_nodes, average_total_degree)


def calculate_edge_properties(G):
    """
    Calculates edge properties of the graph.

    Args:
        G (nx.Graph): A networkx graph.

    Returns:
        Tuple: A tuple containing:
            - parallel_edges (int): The number of parallel edges in the graph.
            - n_bidirectional_edges (int): The number of bidirectional edges in the graph.
    """
    arr = nx.to_numpy_matrix(G)
    parallel_edges = np.sum(arr >= 2)
    n_bidirectional_edges = print_bidirectional_edges(G, quiet=True)
    return (parallel_edges, n_bidirectional_edges)


def calculate_recurrence_measures(G):
    """
    Calculates recurrence measures of the graph.

    Args:
        G (nx.Graph): A networkx graph.

    Returns:
        Tuple: A tuple containing:
            - L1 (int): The number of self-loop edges in the graph.
            - L2 (int): The number of cycles of length 2 in the graph.
            - L3 (int): The number of cycles of length 3 in the graph.
    """
    cycles = list(nx.simple_cycles(G))
    cycle_lengths = [len(cycle) for cycle in cycles]
    L1 = len(list(nx.selfloop_edges(G)))
    L2 = cycle_lengths.count(2)
    L3 = cycle_lengths.count(3)
    return (L1, L2, L3)


def calculate_weakly_connected_components(G):
    """
    Calculates weakly connected components of the graph.

    Args:
        G (nx.Graph): A networkx graph.

    Returns:
        Tuple: A tuple containing:
            - sizes_weakly_conn_components (list): A list of the sizes of the weakly connected components in the graph.
            - number_weakly_conn_components (int): The number of weakly connected components in the graph.
            - cc_size_mean (float): The mean size of the weakly connected components in the graph.
            - cc_size_med (float): The median size of the weakly connected components in the graph.
            - cc_size_sd (float): The standard deviation of the sizes of the weakly connected components in the graph.
            - cc_size_max (int): The size of the largest weakly connected component in the graph.
    """
    sizes_weakly_conn_components = [len(c) for c in sorted(
        nx.weakly_connected_components(G), key=len, reverse=True)]
    number_weakly_conn_components = len(sizes_weakly_conn_components)
    cc_sizes = np.array(sizes_weakly_conn_components)
    cc_size_mean = np.mean(cc_sizes, axis=0)
    cc_size_med = np.median(cc_sizes, axis=0)
    cc_size_sd = np.std(cc_sizes, axis=0)
    cc_size_max = np.max(cc_sizes)
    return (sizes_weakly_conn_components, number_weakly_conn_components, cc_size_mean, cc_size_med, cc_size_sd, cc_size_max)


def calculate_degree_centrality(G):
    """
    Calculates degree centrality of the nodes in the graph.

    Args:
        G (nx.Graph): A networkx graph.

    Returns:
        Tuple: A tuple containing:
            - max_deg_cent (float): The maximum degree centrality value in the graph.
            - max_deg_node (str): The node with the maximum degree centrality value in the graph.
    """
    degree_cents = nx.degree_centrality(G)
    degree_cents = dict(sorted(degree_cents.items(),
                        key=lambda item: item[1], reverse=True))
    max_deg_cent = next(iter(degree_cents.items()))[1]
    max_deg_node = next(iter(degree_cents.items()))[0]
    return (max_deg_cent, max_deg_node)


def calculate_indegree_centrality(G):
    """
    Calculates indegree centrality of the nodes in the graph.

    Args:
        G (nx.Graph): A networkx graph.

    Returns:
        Tuple: A tuple containing:
            - max_indegree_centrality_value (float): The maximum indegree centrality value in the graph.
    """

    in_degree_cents = nx.in_degree_centrality(G)
    in_degree_cents = dict(
        sorted(in_degree_cents.items(), key=lambda item: item[1], reverse=True))
    max_indeg_cent = next(iter(in_degree_cents.items()))
    max_indegree_centrality_value = max_indeg_cent[1]
    return (max_indegree_centrality_value,)


def calculate_outdegree_centrality(G):
    """
    Calculates outdegree centrality of the nodes in the graph.

    Args:
        G (nx.Graph): A networkx graph.

    Returns:
        Tuple: A tuple containing:
            - max_outdegree_centrality_value (float): The maximum outdegree centrality value in the graph.
    """
    out_degree_cents = nx.out_degree_centrality(G)
    out_degree_cents = dict(
        sorted(out_degree_cents.items(), key=lambda item: item[1], reverse=True))
    max_outdeg_cent = next(iter(out_degree_cents.items()))
    max_outdegree_centrality_value = max_outdeg_cent[1]
    return (max_outdegree_centrality_value,)


def calculate_confidence_measures(G):
    """Calculates the mean confidence measure of a given graph.

    Parameters
    ----------
    G : networkx.Graph
        Graph to calculate the mean confidence measure of.

    Returns
    -------
    mean_confidence : float or np.nan
        Mean confidence measure of the graph. Returns np.nan if there are no edges with confidence measures in the graph.
    """
    confidence_vals = [edge[2]['confidence']
                       for edge in G.edges(data=True) if 'confidence' in edge[2]]
    if confidence_vals == []:
        confidence_vals = np.nan
    mean_confidence = np.mean(confidence_vals)
    return mean_confidence


def calculate_all_properties(G):
    """Calculates various properties of a given graph, including basic descriptors, edge properties, recurrence measures, weakly connected components, degree centrality, and confidence measures.

     Parameters
     ----------
     G : networkx.Graph
         Graph to calculate properties of.

     Returns
     -------
     df : pandas.DataFrame
         DataFrame containing the calculated properties of the graph.
     """
    # Calculate basic descriptors
    n_words, n_sents, n_nodes, n_edges, n_unconnected_nodes, average_total_degree = calculate_basic_descriptors(
        G)

    # Calculate edge properties
    parallel_edges, n_bidirectional_edges = calculate_edge_properties(G)

    # Calculate recurrence measures
    L1, L2, L3 = calculate_recurrence_measures(G)

    # Calculate weakly connected components
    sizes_weakly_conn_components, number_weakly_conn_components, cc_size_mean, cc_size_med, cc_size_sd, cc_size_max = calculate_weakly_connected_components(
        G)

    # Calculate degree centrality
    max_deg_cent, max_deg_node = calculate_degree_centrality(G)

    # Calculate indegree centrality
    max_indegree_centrality_value = calculate_indegree_centrality(G)[0]

    # Calculate outdegree centrality
    max_outdegree_centrality_value = calculate_outdegree_centrality(G)[0]

    # Calculate confidence measures
    mean_confidence = calculate_confidence_measures(G)

    # Create data frame
    df = pd.DataFrame({'words': [n_words],
                       'sentences': [n_sents],
                       'nodes': [n_nodes],
                       'edges': [n_edges],
                       'unconnected': [n_unconnected_nodes],
                       'average_total_degree': [average_total_degree],
                       'parallel_edges': [parallel_edges],
                       'bidirectional_edges': [n_bidirectional_edges],
                       'L1': [L1],
                       'L2': [L2],
                       'L3': [L3],
                       'sizes_connected_components': [sizes_weakly_conn_components],
                       'connected_components': [number_weakly_conn_components],
                       'cc_size_mean': [cc_size_mean],
                       'cc_size_med': [cc_size_med],
                       'cc_size_sd': [cc_size_sd],
                       'cc_size_max': [cc_size_max],
                       'max_degree_centrality': [max_deg_cent],
                       'max_degree_node': [max_deg_node],
                       'max_indegree_centrality_value': [max_indegree_centrality_value],
                       'max_outdegree_centrality_value': [max_outdegree_centrality_value],
                       'mean_confidence': [mean_confidence]})

    return df


def import_graphs(filelist):
    """Imports graphs from a list of files.
    Input: list of files
    Output: list of graphs
    """
    graphs = []
    for file in filelist:
        with open(file, "rb") as graph_file:
            graph = pickle.load(graph_file)
            graphs.append(graph)
    return graphs


def graph_properties(filelist):
    """Generates a DataFrame with graph properties for a list of graphs.

    Parameters
    ----------
    filelist : list of str
        List of all graph files.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with graph properties.
    """
    graphs = import_graphs(filelist)

    properties = []
    for G, filename in zip(graphs, filelist):
        # --- Basic graph descriptors ---
        props = calculate_all_properties(G)
        # --- Add filename ---
        props['filename'] = os.path.basename(filename)
        properties.append(props)
    # --- Concatenate dataframes ---
    df = pd.concat(properties, axis=0, ignore_index=True)
    return df
