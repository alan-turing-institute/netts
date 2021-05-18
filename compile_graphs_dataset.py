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
        'parallel_edges'
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
        # find tat index (two-digit combination from 00 to 39 after word "TAT")
        tat = re.search('(?<=TAT)\w+', file)[0]
        if len(tat) > 2:
            tat = tat.split('_')[0]
        # find subject id (7 digit combination before word "TAT")
        subj = file.split('-TAT')[0][-7:]
        # --- Get basic transcript descriptors ---
        n_words = G.graph['tokens']
        n_sents = G.graph['sentences']
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
        # Number of weakly connected components
        sizes_weakly_conn_components = [len(c) for c in sorted(
            nx.weakly_connected_components(G), key=len, reverse=True)]
        number_weakly_conn_components = len(sizes_weakly_conn_components)
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
        #
        # Outdegree centrality
        out_degree_cents = nx.out_degree_centrality(G)
        out_degree_cents = dict(sorted(out_degree_cents.items(),
                                       key=lambda item: item[1], reverse=True))
        max_outdeg_cent = next(iter(out_degree_cents.items()))
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
            number_weakly_conn_components,
            max_deg_cent,
            max_deg_node,
            max_indeg_cent,
            max_outdeg_cent,
            mean_confidence,
            std_confidence,
            density,
            diameter,
            average_shortest_path,
            avg_clustering,
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
        'connected_components',
        'max_degree_centrality',
        'max_degree_node',
        'max_indegree_centrality',
        'max_outdegree_centrality',
        'mean_confidence',
        'std_confidence',
        'density',
        'diameter',
        'average_shortest_path',
        'clustering',
    ])
    #
    df.subj = pd.Categorical(df.subj.astype('str'))
    df.tat = pd.Categorical(df.tat.astype('str'))
    df.tat = df.tat.cat.rename_categories({'8': '08'})
    df.tat = df.tat.cat.reorder_categories(
        ['08', '10', '13', '19', '21', '24', '28', '30'])
    df.tat.value_counts()
    #
    return df
