#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  motif_helper_functions.py
#
# Description:
#               Functions for counting motifs in semantic speech networks.
#
# Author:       Caroline Nettekoven, 2021
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
import networkx as nx
import numpy as np
import itertools
import matplotlib.pyplot as plt
import os.path as op
import itertools
import seaborn as sns

# Modules to generate 3D Arrow
import numpy as np
from numpy import *
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

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


def biplot(score, coeff, y):
    '''
    Author: Serafeim Loukas, serafeim.loukas@epfl.ch. Modified by Caroline Nettekoven, crn29@cam.ac.uk
    Inputs:
       score: the projected data
       coeff: the eigenvectors (PCs)
       y: the class labels
   '''
    #
    #
    xs = score[:, 0]  # projection on PC1
    ys = score[:, 1]  # projection on PC2
    n = coeff.shape[0]  # number of variables
    plt.figure(figsize=(10, 8), dpi=100)
    classes = np.unique(y)
    if classes[0] is not None:
        colors = sns.diverging_palette(
            max(classes), min(classes), n=len(classes), s=75, l=50, sep=3, center='light', as_cmap=False)
    else:
        colors = 'g'
    # colors = ['g', 'r', 'y']
    # markers = ['o', '^', 'x']
    for s, l in enumerate(classes):
        # color based on group
        plt.scatter(xs[y == l], ys[y == l], c=colors[s])
        for i in range(n):
            # plot as arrows the variable scores (each variable has a score for PC1 and one for PC2)
            plt.arrow(0, 0, coeff[i, 0], coeff[i, 1], color='k',
                      alpha=0.9, linestyle='-', linewidth=1.5, overhang=0.2)
            plt.text(coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, "Var" +
                     str(i + 1), color='k', ha='center', va='center', fontsize=10)
        plt.xlabel("PC{}".format(1), size=14)
        plt.ylabel("PC{}".format(2), size=14)
        limx = int(xs.max()) + 1
        limy = int(ys.max()) + 1
        plt.xlim([-limx, limx])
        plt.ylim([-limy, limy])
        plt.grid()
        plt.tick_params(axis='both', which='both', labelsize=14)


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs
    #

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


def biplot_3d(score, coeff, y):
    '''
    Author: Caroline Nettekoven, crn29@cam.ac.uk
    Inputs:
       score: the projected data
       coeff: the eigenvectors (PCs)
       y: the class labels
   '''
    #
    #
    xs = score[:, 0]  # projection on PC1
    ys = score[:, 1]  # projection on PC2
    zs = score[:, 2]  # projection on PC3
    n = coeff.shape[0]  # number of variables
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection='3d')
    # Define colors
    classes = np.unique(y)
    if classes[0] is not None:
        colors = sns.diverging_palette(
            max(classes), min(classes), n=len(classes), s=75, l=50, sep=3, center='light', as_cmap=False)
    else:
        colors = 'g'
    #
    for s, l in enumerate(classes):
        # color based on group
        ax.scatter(
            xs=xs[y == l],
            ys=ys[y == l],
            zs=zs[y == l],
            c=colors[s]
        )
        #
        ax.set_xlabel("PC{}".format(1), size=14)
        ax.set_ylabel("PC{}".format(2), size=14)
        ax.set_zlabel("PC{}".format(3), size=14)
        # Limes
        limx = (np.percentile(xs, 99), int(xs.min()) - 1)
        limy = (np.percentile(ys, 99), int(ys.min()) - 1)
        limz = (np.percentile(zs, 99), int(zs.min()) - 1)
        #
        # limx = (int(xs.max()) + 1, int(xs.min()) - 1)
        # limy = (int(ys.max()) + 1, int(ys.min()) - 1)
        # limz = (int(zs.max()) + 1, int(zs.min()) - 1)
        #
        ax.set_xlim3d(limx)
        ax.set_ylim3d(limy)
        ax.set_zlim3d(limz)
        ax.grid()
        ax.tick_params(axis='both', which='both', labelsize=14)
    #
    for i in range(n):
        v = coeff[i]
        a = Arrow3D([0, v[0] * 20], [0, v[1] * 20],
                    [0, v[2] * 20], mutation_scale=20,
                    lw=1, arrowstyle="-|>", color="k")
        ax.add_artist(a)
        ax.text(v[0] * 19, v[1] * 19, v[2] * 19, "Var" +
                str(i + 1), color='k', size=10)

# TODO: Scale the arrows such that they are exactly as long as the limes

# TODO: Rewrite the motif count function such that it is more readable
# TODO: Test The motif count function with very simple graphs
