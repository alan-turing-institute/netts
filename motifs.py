#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
import networkx as nx
import numpy as np
import itertools
import matplotlib.pyplot as plt
import os.path as op
# We define each S* motif as a directed graph in networkx
motifs = {
    'm01': nx.DiGraph([(2, 1), (2, 3)]),
    'm02': nx.DiGraph([(2, 1), (3, 2)]),
    'm03': nx.DiGraph([(2, 1), (2, 3), (3, 2)]),
    'm04': nx.DiGraph([(2, 1), (3, 1)]),
    'm05': nx.DiGraph([(2, 1), (3, 1), (2, 3)]),
    'm06': nx.DiGraph([(2, 1), (2, 3), (3, 2), (3, 1)]),
    'm07': nx.DiGraph([(1, 2), (3, 2), (2, 3)]),
    'm08': nx.DiGraph([(1, 2), (2, 1), (3, 2), (2, 3)]),
    'm09': nx.DiGraph([(1, 2), (2, 3), (3, 1)]),
    'm10': nx.DiGraph([(1, 2), (2, 1), (2, 3), (3, 1)]),
    'm11': nx.DiGraph([(1, 2), (2, 1), (3, 2), (3, 1)]),
    'm12': nx.DiGraph([(1, 2), (2, 1), (2, 3), (3, 2), (3, 1)]),
    'm13': nx.DiGraph([(1, 2), (2, 1), (2, 3), (3, 2), (3, 1), (1, 3)]),
}


def check_duplicates(motifs):
    """Checks that all motifs are unique"""
    #
    duplicate_found = False
    for motif_pair in list(itertools.product(*[motifs, motifs])):
        if nx.is_isomorphic(motifs[motif_pair[0]], motifs[motif_pair[1]]) and motif_pair[0] != motif_pair[1]:
            print(motif_pair)
            duplicate_found = True
    #
    if not duplicate_found:
        print('No motif duplicate found')


def rasterplot(motifs, output_dir='/Users/CN/Dropbox/speech_graphs/all_tats/figures/'):
    """Plots all motifs in a rasterplot"""
    # --------------------- Plot all motifs ---------------------------------------
    fig = plt.figure(figsize=(25.6, 20))
    no_motifs = len(motifs)
    for m, (mkey, M) in enumerate(motifs.items()):
        ax = plt.subplot(2, np.ceil(no_motifs / 2), m + 1)
        # ax = plt.subplot(np.ceil(no_motifs / 2), 2, m + 1)
        pos = nx.spring_layout(M)
        plt.axis("off")
        nx.draw_networkx_nodes(M, pos, node_size=20)
        nx.draw_networkx_edges(M, pos, alpha=0.4)
        plt.title(mkey)
    #
    plt.suptitle("Searching for {}-Node Motifs".format(len(M.nodes())))
    # --- Save plot ---
    output = op.join(
        output_dir, 'Rasterplot_{}-Node-Motifs'.format(len(M.nodes())))
    plt.savefig(output)
    plt.show()


def motif_counter(G, motifs):
    """Counts motifs in a directed graph
    :param G: A ``DiGraph`` object
    :param motifs: A ``dict`` of motifs to count
    :returns: A ``dict`` with the number of each motifs, with the same keys as ``motifs``
    This function is actually rather simple. It will extract all 3-grams from
    the original graph, and look for isomorphisms in the motifs contained
    in a dictionary. The returned object is a ``dict`` with the number of
    times each motif was found.::
        >>> print motif_counter(G, motifs)
        {'m1': 4, 'm3': 0, 'm2': 1, 'm5': 0, 'm4': 3}
    """
    # This function will take each possible subgraphs of G of size 3, then
    # compare them to the motifs dict using .subgraph() and is_isomorphic
    #
    # This line simply creates a dictionary with 0 for all values, and the
    # motif names as keys
    #
    motif_count = dict(
        zip(motifs.keys(), list(map(int, np.zeros(len(motifs))))))
    nodes = G.nodes()
    #
    # We use iterools.product to have all combinations of three nodes in the
    # original graph. Then we filter combinations with non-unique nodes, because
    # the motifs do not account for self-consumption.
    #
    # all node combinations
    triplets = list(itertools.product(*[nodes, nodes, nodes]))
    # remove combinations with several entries of same node
    triplets = [trip for trip in triplets if len(list(set(trip))) == 3]
    # make each triplet entry  into list
    triplets = list(map(list, map(np.sort, triplets)))
    # get unique entries
    u_triplets = []
    [u_triplets.append(trip)
     for trip in triplets if not u_triplets.count(trip)]
    #
    # Then for each each of the triplets, take its subgraph, and compare
    # it to all of the possible motifs
    #
    for trip in u_triplets:
        # print(trip)
        sub_G = G.subgraph(trip)
        mot_match = list(map(lambda mot_id: nx.is_isomorphic(
            sub_G, motifs[mot_id]), motifs.keys()))
        match_keys = [list(motifs.keys())[i]
                      for i in range(len(motifs)) if mot_match[i]]
        if len(match_keys) == 1:
            motif_count[match_keys[0]] += 1
    #
    return motif_count

# TODO: Rewrite the motif count function such that it is more readable
# TODO: Test The motif count function with very simple graphs
