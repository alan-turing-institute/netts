#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  compile_graphs_dataset.py
#
# Description:
#               Script to analyse semantic speech graphs
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate

import numpy as np
import networkx as nx
import os
import os.path as op
import re
import pandas as pd
import sys
sys.path.append(
    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
import glob
from graph_analysis_functions import print_bidirectional_edges


def get_graphs(graph_dir='/Users/CN/Dropbox/speech_graphs/all_tats'):
    """Reads all pickled graphs in graph directory.

    Parameters
    ----------
    graph_dir : Directory containing pickled graphs.

    Returns
    -------
    graphs : list containing all graphs
    filelist : list of all graph files

    """
    # --------------------- Import graphs ---------------------------------------
    filelist = sorted(glob.glob(op.join(graph_dir, '*.gpickle')))
    #
    graphs = []
    for file in filelist:
        graph = op.join(graph_dir, file)
        graphs.append(nx.read_gpickle((graph)))
    return graphs, filelist


def exclude_empty_graphs(graphs, filelist, be_quiet=False):
    """Excludes graphs that are empty.
    Finds graphs that have 0 nodes and excludes them from graphs list and filelist.

    Parameters
    ----------
    graphs : list containing all graphs
    filelist : list of all graph files

    """
    # --------------------- Find empty graphs ---------------------------------------
    exclude = []
    for g, G in enumerate(graphs):
        # --- Get basic transcript descriptors ---
        n_words = G.graph['tokens']
        n_sents = G.graph['sentences']
        transcript = G.graph['transcript']
        # --- Get basic graph descriptors ---
        n_nodes = len(G.nodes())
        if n_nodes is 0:
            exclude.append(g)
            if not be_quiet:
                print('Excluding graph {0}. Transcript {1} has {2} sentences and {3} words'.format(
                    g, transcript, n_sents, n_words))
    print('Obtained {} graphs. Excluded {} empty graphs. Kept {} graphs.'.format(
        len(graphs), len(exclude), len(graphs) - len(exclude)))
    graphs = [G for g, G in enumerate(graphs) if g not in exclude]
    filelist = [F for f, F in enumerate(filelist) if f not in exclude]
    return graphs, filelist


def graph_properties(graphs, filelist):
    """

    Parameters
    ----------
    graphs : list containing all graphs
    filelist : list of all graph files

    Returns
    -------
    df : DataFrame with graph descriptions.
        'subj'                          Subject ID
        'tat'                           Picture stimulus
        'words'                         No of words in transcript
        'sentences'                     No of sentences in transcript
        'nodes'                         No of nodes
        'edges'                         No of edges
        'unconnected'                   No of unconnected nodes
        'average_total_degree'          
        'parallel_edges'                No of parallel edges
        'lsc'
        'lcc'
        'L1'
        'L2'
        'L3'
        'sizes_connected_components'    
        'connected_components'
        'max_degree_centrality'
        'max_degree_node'
        'max_indegree_centrality'
        'max_outdegree_centrality'
        'mean_confidence'
        'std_confidence'
        'density'
        'diameter'
        'average_shortest_path'
        'clustering'

    """
    # --------------------- Collect properties ---------------------------------------
    g_properties = []
    for g, G in enumerate(graphs):
        file = filelist[g]
        # --- Get subject and tat identifiers ---
        #
        if 'oasis' in file:
            # +++ For Oasis dataset +++
            # tat index is number between 'pic' and '_'
            tat = re.search('(?<=pic)\w+', file)[0].split('_')[0]
            # subject index is 7 digit combination after '_s'
            subj = file.split('_s')[1].split('_')[0]
        elif 'all_tats' in file:
            # +++ For General Public dataset +++
            # tat index is two-digit combination from 00 to 39 after word "TAT"
            tat = re.search('(?<=TAT)\w+', file)[0]
            if len(tat) > 2:
                tat = tat.split('_')[0]
            # subject index is 7 digit combination before word "TAT"
            subj = file.split('-TAT')[0][-7:]
        # +++ +++ +++ +++ +++ +++ +++ +++ +++
        # --- Get basic transcript descriptors ---
        n_words = G.graph['tokens']
        n_sents = G.graph['sentences']
        mean_sentence_length = int(n_words) / int(n_sents)
        #
        # --- Get basic graph descriptors ---
        n_nodes = len(G.nodes())
        n_edges = G.size()
        n_unconnected_nodes = len(G.graph['unconnected_nodes'])
        #
        # average total degree
        # for a directed graph, this is equivalent to: degrees = list(G.degree()); degree = [d[1] for d in degrees]; sum(degree) / len(degree);
        average_total_degree = (n_edges * 2) / n_nodes
        #
        # number of parallel edges
        arr = nx.to_numpy_matrix(G)
        parallel_edges = np.sum(arr >= 2)
        #
        # number of bidirectional edges
        n_bidirectional_edges = print_bidirectional_edges(G, quiet=True)
        # LSC
        lsc = len(max(nx.strongly_connected_components(G), key=len))
        # LCC
        lcc = len(max(nx.weakly_connected_components(G), key=len))
        #
        # Recurrence measures: L1, L2, L3
        cycles = list(nx.simple_cycles(G))
        cycle_lengths = [len(cycle) for cycle in cycles]
        # equivalent to cycle_lengths.count(1):
        L1 = len(list(nx.selfloop_edges(G)))
        L2 = cycle_lengths.count(2)
        L3 = cycle_lengths.count(3)
        #
        # Weakly connected component sizes
        sizes_weakly_conn_components = [len(c) for c in sorted(
            nx.weakly_connected_components(G), key=len, reverse=True)]
        # Number of weakly connected components
        number_weakly_conn_components = len(sizes_weakly_conn_components)
        # Max, Mean, Median, SD of weakly connected component sizes
        cc_sizes = np.array(sizes_weakly_conn_components)
        cc_size_mean = np.mean(cc_sizes, axis=0)
        cc_size_med = np.median(cc_sizes, axis=0)
        cc_size_sd = np.std(cc_sizes, axis=0)
        cc_size_max = np.max(cc_sizes)
        #
        # Degree centrality
        degree_cents = nx.degree_centrality(G)
        degree_cents = dict(sorted(degree_cents.items(),
                                   key=lambda item: item[1], reverse=True))
        max_deg_cent = next(iter(degree_cents.items()))[1]
        max_deg_node = next(iter(degree_cents.items()))[0]
        #
        # Indegree centrality
        in_degree_cents = nx.in_degree_centrality(G)
        in_degree_cents = dict(sorted(in_degree_cents.items(),
                                      key=lambda item: item[1], reverse=True))
        max_indeg_cent = next(iter(in_degree_cents.items()))
        max_indegree_centrality_value = max_indeg_cent[1]
        #
        # Outdegree centrality
        out_degree_cents = nx.out_degree_centrality(G)
        out_degree_cents = dict(sorted(out_degree_cents.items(),
                                       key=lambda item: item[1], reverse=True))
        max_outdeg_cent = next(iter(out_degree_cents.items()))
        max_outdegree_centrality_value = max_outdeg_cent[1]
        #
        # Confidence measures of relations
        confidence_vals = [edge[2]['confidence']
                           for edge in G.edges(data=True) if 'confidence' in edge[2]]
        if confidence_vals == []:
            confidence_vals = np.nan
        #
        mean_confidence = np.mean(confidence_vals)
        std_confidence = np.std(confidence_vals)
        # --- Properties for undirected version of the graph (w/o self-loops or PEs) ---
        G_basic = nx.Graph(G)
        density = nx.density(G_basic)
        #
        # Get only largest connected component subgraph
        s = sorted(nx.connected_components(G_basic), key=len, reverse=True)[0]
        S = G_basic.subgraph(s).copy()
        #
        diameter = nx.diameter(S)
        #
        average_shortest_path = nx.average_shortest_path_length(S)
        #
        avg_clustering = nx.average_clustering(S)
        #
        # Calculate how many adjacent edges come from the same sentence or consecutive sentences
        consecutive_edges = 0
        for node in list(G.nodes):
            sentence_ids = sorted([edge[2]['sentence']
                                   for edge in G.edges(node, data=True)])
            diffs = np.diff(np.array(sentence_ids))
            if diffs != []:
                consecutive_edges = consecutive_edges + len(
                    [i for i, diff in enumerate(diffs, 1) if diff in [0, 1, -1]])
        #
        # --- Collect Properties ---
        g_properties.append([
            subj,
            tat,
            n_words,
            n_sents,
            n_nodes,
            n_edges,
            n_unconnected_nodes,
            average_total_degree,
            parallel_edges,
            n_bidirectional_edges,
            lsc,
            lcc,
            L1,
            L2,
            L3,
            sizes_weakly_conn_components,
            cc_size_mean,
            cc_size_med,
            cc_size_sd,
            cc_size_max,
            number_weakly_conn_components,
            max_deg_cent,
            max_deg_node,
            max_indeg_cent,
            max_outdeg_cent,
            max_indegree_centrality_value,
            max_outdegree_centrality_value,
            mean_sentence_length,
            mean_confidence,
            std_confidence,
            density,
            diameter,
            average_shortest_path,
            avg_clustering,
            consecutive_edges,
        ])
    #
    # --------------------- Make dataframe ---------------------------------------
    df = pd.DataFrame(g_properties, columns=[
        'subj', 'tat',
        'words', 'sentences',
        'nodes', 'edges',
        'unconnected',
        'average_total_degree',
        'parallel_edges',
        'bidirectional_edges',
        'lsc', 'lcc',
        'L1', 'L2', 'L3',
        'sizes_connected_components',
        'cc_size_mean',
        'cc_size_med',
        'cc_size_sd',
        'cc_size_max',
        'connected_components',
        'max_degree_centrality',
        'max_degree_node',
        'max_indegree_centrality',
        'max_outdegree_centrality',
        'max_indegree_centrality_value',
        'max_outdegree_centrality_value',
        'mean_sentence_length',
        'mean_confidence',
        'std_confidence',
        'density',
        'diameter',
        'average_shortest_path',
        'clustering',
        'consecutive_edges',
    ])
    #
    # --- Make subject and tat index categorical ---
    df.subj = pd.Categorical(df.subj.astype('str'))
    df.tat = pd.Categorical(df.tat.astype('str'))
    if 'all_tats' in file:
        # +++ For General Public dataset +++
        df.tat = df.tat.cat.rename_categories({'8': '08'})
        df.tat = df.tat.cat.reorder_categories(
            ['08', '10', '13', '19', '21', '24', '28', '30'])
    # +++ +++ +++ +++ +++ +++ +++ +++ +++
    #
    return df


def graph_properties_random(graphs):
    """

    Parameters
    ----------
    graphs : list containing all random graphs

    Returns
    -------
    df : DataFrame with graph descriptions.
        'average_total_degree'          
        'parallel_edges'                No of parallel edges
        'lsc'
        'lcc'
        'L1'
        'L2'
        'L3'
        'sizes_connected_components'    
        'connected_components'
        'max_degree_centrality'
        'max_degree_node'
        'max_indegree_centrality'
        'max_outdegree_centrality'
        'mean_confidence'
        'std_confidence'
        'density'
        'diameter'
        'average_shortest_path'
        'clustering'

    """
    # --------------------- Collect properties ---------------------------------------
    g_properties = []
    for g, G in enumerate(graphs):
        #
        # --- Get basic graph descriptors ---
        n_nodes = len(G.nodes())
        n_edges = G.size()
        # average total degree
        # for a directed graph, this is equivalent to: degrees = list(G.degree()); degree = [d[1] for d in degrees]; sum(degree) / len(degree);
        average_total_degree = (n_edges * 2) / n_nodes
        #
        # number of parallel edges
        arr = nx.to_numpy_matrix(G)
        parallel_edges = np.sum(arr >= 2)
        #
        # number of bidirectional edges
        n_bidirectional_edges = print_bidirectional_edges(G, quiet=True)
        # LSC
        lsc = len(max(nx.strongly_connected_components(G), key=len))
        # LCC
        lcc = len(max(nx.weakly_connected_components(G), key=len))
        #
        # Recurrence measures: L1, L2, L3
        cycles = list(nx.simple_cycles(G))
        cycle_lengths = [len(cycle) for cycle in cycles]
        # equivalent to cycle_lengths.count(1):
        L1 = len(list(nx.selfloop_edges(G)))
        L2 = cycle_lengths.count(2)
        L3 = cycle_lengths.count(3)
        #
        # Weakly connected component sizes
        sizes_weakly_conn_components = [len(c) for c in sorted(
            nx.weakly_connected_components(G), key=len, reverse=True)]
        # Number of weakly connected components
        number_weakly_conn_components = len(sizes_weakly_conn_components)
        # Max, Mean, Median, SD of weakly connected component sizes
        cc_sizes = np.array(sizes_weakly_conn_components)
        cc_size_mean = np.mean(cc_sizes, axis=0)
        cc_size_med = np.median(cc_sizes, axis=0)
        cc_size_sd = np.std(cc_sizes, axis=0)
        cc_size_max = np.max(cc_sizes)
        #
        # Degree centrality
        degree_cents = nx.degree_centrality(G)
        degree_cents = dict(sorted(degree_cents.items(),
                                   key=lambda item: item[1], reverse=True))
        max_deg_cent = next(iter(degree_cents.items()))[1]
        #
        # Indegree centrality
        in_degree_cents = nx.in_degree_centrality(G)
        in_degree_cents = dict(sorted(in_degree_cents.items(),
                                      key=lambda item: item[1], reverse=True))
        max_indeg_cent = next(iter(in_degree_cents.items()))
        max_indegree_centrality_value = max_indeg_cent[1]
        #
        # Outdegree centrality
        out_degree_cents = nx.out_degree_centrality(G)
        out_degree_cents = dict(sorted(out_degree_cents.items(),
                                       key=lambda item: item[1], reverse=True))
        max_outdeg_cent = next(iter(out_degree_cents.items()))
        max_outdegree_centrality_value = max_outdeg_cent[1]
        #
        # --- Properties for undirected version of the graph (w/o self-loops or PEs) ---
        G_basic = nx.Graph(G)
        density = nx.density(G_basic)
        #
        # Get only largest connected component subgraph
        s = sorted(nx.connected_components(G_basic), key=len, reverse=True)[0]
        S = G_basic.subgraph(s).copy()
        #
        diameter = nx.diameter(S)
        #
        average_shortest_path = nx.average_shortest_path_length(S)
        #
        avg_clustering = nx.average_clustering(S)
        #
        #
        # --- Collect Properties ---
        g_properties.append([
            n_nodes,
            n_edges,
            average_total_degree,
            parallel_edges,
            n_bidirectional_edges,
            lsc,
            lcc,
            L1,
            L2,
            L3,
            cc_size_mean,
            cc_size_med,
            cc_size_sd,
            cc_size_max,
            number_weakly_conn_components,
            max_deg_cent,
            max_indegree_centrality_value,
            max_outdegree_centrality_value,
            density,
            diameter,
            average_shortest_path,
            avg_clustering,
        ])
    #
    # --------------------- Make dataframe ---------------------------------------
    df = pd.DataFrame(g_properties, columns=[
        'nodes', 'edges',
        'average_total_degree',
        'parallel_edges',
        'bidirectional_edges',
        'lsc', 'lcc',
        'L1', 'L2', 'L3',
        'cc_size_mean',
        'cc_size_med',
        'cc_size_sd',
        'cc_size_max',
        'connected_components',
        'max_degree_centrality',
        'max_indegree_centrality_value',
        'max_outdegree_centrality_value',
        'density',
        'diameter',
        'average_shortest_path',
        'clustering'
    ])
    #
    return df
