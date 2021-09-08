#!/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  speech_graph.py
#
# Description:
#               Script to visualise sentence using OpenIE5 and Stanford CoreNLP
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# source /Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/venv/bin/activate
# Usage: python ./speech_graph.py 3
#        tat=3; python -u ./speech_graph.py ${tat} > figures/SpeechGraph_log_${tat}_`date +%F` # (pipe output to text file)
# ------------------------------------------------------------------------------

# flake8: noqa
# pylint: skip-file

import datetime
import os
import os.path as op
import sys
import time
import typing
from copy import deepcopy
from itertools import chain
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import nltk
import numpy as np
import pandas as pd
import stanza

# from netspy.types import MultiDiGraph
from networkx.classes.multidigraph import MultiDiGraph

# sys.path.append(
#    '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/')
from pyopenie import OpenIE5
from stanza.server import CoreNLPClient

from netspy.config import get_settings

# from netspy.filelists import (
#    all_tat_files,
#    dct_story_files,
#    genpub_files,
#    hbn_movie_files,
#    tat_pilot_files,
# )
from netspy.nlp_helper_functions import (
    expand_contractions,
    get_transcript_properties,
    process_sent,
    remove_bad_transcripts,
    remove_duplicates,
    remove_interjections,
    remove_irrelevant_text,
    replace_problematic_symbols,
)
from netspy.visualise_paragraph_functions import (
    add_adj_edges,
    add_obl_edges,
    add_prep_edges,
    clean_nodes,
    clean_parallel_edges,
    create_edges_ollie,
    create_edges_stanza,
    get_adj_edges,
    get_node_synonyms,
    get_obl_edges,
    get_prep_edges,
    get_unconnected_nodes,
    get_word_types,
    merge_corefs,
    split_node_synonyms,
    split_nodes,
)

settings = get_settings()
nltk.data.path.append(settings.nltk_dir)


def speech_graph(transcript: str) -> MultiDiGraph:

    # ------------------------------------------------------------------------------
    # Time execution of script
    start_time = time.time()
    # ------------------------------------------------------------------------------
    # Get sentence
    # selected_file = 2
    # selected_file = Path(sys.argv[1])
    # if not selected_file.exists():
    #     raise IOError("Cannot find file")
    # data_dir = '/Users/CN/Documents/Projects/Cambridge/data'

    # ++++++++ HBN Data ++++++++
    # hbn_data_dir = op.join(data_dir, 'HBN', 'movie_descriptions')
    # filename = hbn_movie_files[selected_file]
    # input_file = op.join(hbn_data_dir, filename)
    # output_dir = '/Users/CN/Dropbox/speech_graphs/hbn'

    # # ++++++++ DCT Data ++++++++
    # dct_data_dir = op.join(data_dir, 'DCT', 'stories')
    # filename = dct_story_files[selected_file]
    # input_file = op.join(dct_data_dir, filename)
    # output_dir = '/Users/CN/Dropbox/speech_graphs/dct'

    # # ++++++++ All TAT files ++++++++
    # input_file = selected_file
    # output_dir = "/Users/hduncan/Work/NetSpy/netspy"

    # filename = all_tat_files[selected_file]
    # if selected_file < 119:
    #    tat_data_dir = op.join(data_dir, 'Kings', 'Prolific_pilot_all_transcripts')
    #    input_file = op.join(tat_data_dir, filename)
    # else:
    #    genpub_data_dir = op.join(data_dir, 'Kings', 'general_public_tat')
    #    input_file = op.join(genpub_data_dir, filename)

    # # ++++++++ TAT files ++++++++
    # # Make list of all transcripts
    # # Kings Pilot
    # tats = sorted(
    #     Path(op.join(data_dir, 'Kings/Prolific_pilot_all_transcripts')).rglob('*TAT*.txt'))
    # # Kings Study
    # tats.extend(
    #     sorted(Path(op.join(data_dir, 'Kings/Manual_2021-04-18')).rglob('*.txt')))

    # # ++++++++ Oasis files ++++++++
    # # Make list of all transcripts
    # # Oasis study
    # tats = sorted(
    #     Path(op.join(data_dir, 'oasis/TLI_1_min_disfluencies/')).rglob('*.txt'))

    # ++++++++ Ground truth files ++++++++
    # Make list of all transcripts
    # Oasis study
    # tats = sorted(
    #     Path(op.join(data_dir, 'ground_truth_tat')).rglob('*.txt'))

    # Import selected transcript
    # input_file = tats[selected_file]
    # filename = input_file.name
    # filename = str(selected_file)
    # with open(input_file, "r") as fh:
    #     orig_text = fh.read()
    #     print(orig_text)

    # ------------------------------------------------------------------------------
    # ------- Clean text -------
    # Need to replace problematic symbols before ANYTHING ELSE, because other tools cannot work with problematic symbols
    text = replace_problematic_symbols(transcript)  # replace ’ with '
    print(text)
    text = expand_contractions(text)  # expand it's to it is
    print(text)

    text = remove_interjections(text)  # remove Ums and Mmms
    text = remove_irrelevant_text(text)
    text = text.strip()  # remove trailing and leading whitespace

    # ------------------------------------------------------------------------------
    # ------- Print transcript name -------
    # transcript = filename.strip(".txt")
    # print("\n+++ Transcript +++ \n\n %s" % (transcript))

    # ------------------------------------------------------------------------------
    # ------- Print cleaned text -------
    print("\n+++ Paragraph: +++ \n\n %s \n\n+++++++++++++++++++" % (text))

    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
    # ------- Run Stanford CoreNLP (Stanza) -------
    # Annotate and extract with Stanford CoreNLP

    with CoreNLPClient(
        properties={
            "annotators": "tokenize,ssplit,pos,lemma,parse,depparse,coref,openie"
            # 'pos.model': '/Users/CN/Documents/Projects/Cambridge/cambridge_language_analysis/OpenIE-standalone/target/streams/$global/assemblyOption/$global/streams/assembly/8a3bd51fe5c1bb09a51f326fa358947f6dc78463_8e7f18d9ae73e8daf5ee4d4e11167e10f8827888_da39a3ee5e6b4b0d3255bfef95601890afd80709/edu/stanford/nlp/models/pos-tagger/english-bidirectional/english-bidirectional-distsim.tagger'
        },
        be_quiet=True,
    ) as client:
        ex_stanza = client.annotate(text)

    # ------- Basic Transcript Descriptors -------
    n_tokens, n_sententences, _ = get_transcript_properties(text, ex_stanza)
    # ------------------------------------------------------------------------------
    # ------- Run OpenIE5 (Ollie) -------
    # Ollie can handle more than one sentence at a time, but need to loop through sentences to keep track of sentence index
    extractorIE5 = OpenIE5("http://localhost:6000")  # Initialize Ollie

    ex_ollie = {}
    for i, sentence in enumerate(ex_stanza.sentence):
        if len(sentence.token) > 1:
            print(f"====== Submitting sentence {i+1} tokens =======")
            sentence_text = (" ").join(
                [token.originalText for token in sentence.token if token.originalText]
            )
            print("{}".format(sentence_text))
            try:
                extraction = extractorIE5.extract(sentence_text)
            except:
                print(
                    "\n- - - > Unexpected error in Ollie: {} \n\tOllie was unable to handle this sentence.\n\tSetting extraction to empty for this sentence.\n\tContinueing with next sentence.\n".format(
                        sys.exc_info()[0]
                    )
                )
                extraction = []
            ex_ollie[i] = extraction
        else:
            print(
                '====== Skipping sentence {}: Sentence has too few tokens: "{}" ======='.format(
                    i + 1,
                    (" ").join(
                        [
                            token.originalText
                            for token in sentence.token
                            if token.originalText
                        ]
                    ),
                )
            )

    print("+++++++++++++++++++\n")

    # --------------------- Create ollie edges ---------------------------------------
    (
        ollie_edges,
        ollie_edges_text_excerpts,
        ollie_one_node_edges,
        ollie_one_node_edges_text_excerpts,
    ) = create_edges_ollie(ex_ollie)

    edges = ollie_edges
    # --------------------- Create stanza edges ---------------------------------------
    stanza_edges, stanza_edges_text_excerpts = create_edges_stanza(
        ex_stanza, be_quiet=False
    )
    # If Ollie was unable to detect any edges, use stanza edges

    if len(ollie_edges) == 0 and len(stanza_edges) != 0:
        edges = stanza_edges
        print(
            "++++ Ollie detected {} edges, but stanza detected {}. Therefore added edges detected by stanza.  ++++".format(
                len(ollie_edges), len(stanza_edges)
            )
        )
    elif len(ollie_edges) == 0 and len(stanza_edges) == 0:
        print(
            "++++ Ollie detected {} edges and stanza also detected {}. No stanza edges were added. ++++".format(
                len(ollie_edges), len(stanza_edges)
            )
        )
    else:
        print(
            "++++ Ollie detected {} edges, so no stanza edges were added.  ++++".format(
                len(ollie_edges)
            )
        )

    # --------------------- Get word types ---------------------------------------
    no_noun, poss_pronouns, dts, nouns, nouns_origtext, adjectives = get_word_types(
        ex_stanza
    )

    adjectives, adjective_edges = get_adj_edges(ex_stanza)

    prepositions, preposition_edges = get_prep_edges(ex_stanza)

    obliques, oblique_edges = get_obl_edges(ex_stanza)

    # --------------------- Add oblique edges ---------------------------------------
    edges = add_obl_edges(edges, oblique_edges)
    # --------------------- Get node name synonyms ---------------------------------------
    node_name_synonyms = get_node_synonyms(ex_stanza, no_noun)
    # --------------------- Split nodes connected by preposition ---------------------------------------
    edges, node_name_synonyms = split_node_synonyms(
        node_name_synonyms, preposition_edges, edges
    )

    edges = split_nodes(edges, preposition_edges, no_noun)
    # --------------------- Merge coreferenced nodes ---------------------------------------
    edges, orig_edges = merge_corefs(edges, node_name_synonyms, no_noun, poss_pronouns)

    preposition_edges, orig_preposition_edges = merge_corefs(
        preposition_edges, node_name_synonyms, no_noun, poss_pronouns
    )

    adjective_edges, orig_adjective_edges = merge_corefs(
        adjective_edges, node_name_synonyms, no_noun, poss_pronouns
    )

    oblique_edges, orig_oblique_edges = merge_corefs(
        oblique_edges, node_name_synonyms, no_noun, poss_pronouns
    )

    # --------------------- Add adjective edges / preposition edges / unconnected nodes ---------------------------------------
    edges = add_adj_edges(edges, adjective_edges, add_adjective_edges=True)

    edges = add_prep_edges(edges, preposition_edges, add_all_preposition_edges=True)

    unconnected_nodes = get_unconnected_nodes(edges, orig_edges, nouns)

    # --------------------- Clean nodes & edges ---------------------------------------
    edges = clean_nodes(edges, nouns, adjectives)

    edges = clean_parallel_edges(edges)

    # --------------------- Speech Graph ---------------------------------------
    fig = plt.figure(figsize=(25.6, 9.6))

    # Construct Speech Graph with properties: number of tokens, number of sentences, unconnected nodes as graph property
    G = nx.MultiDiGraph(
        transcript=transcript,
        sentences=n_sententences,
        tokens=n_tokens,
        unconnected_nodes=unconnected_nodes,
    )
    # Add Edges
    G.add_edges_from(edges)
    return G


def plot_graph(graph: MultiDiGraph, ext: str = None) -> None:
    # Plot Graph and add edge labels
    pos = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos,
        edge_color="black",
        width=1,
        linewidths=1,
        node_size=500,
        node_color="pink",
        alpha=0.9,
        labels={node: node for node in graph.nodes()},
    )
    edge_labels = dict(
        [
            (
                (
                    u,
                    v,
                ),
                d["relation"],
            )
            for u, v, d in graph.edges(data=True)
        ]
    )
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red")

    # Get current working directory to output the png and gpickle files
    output_dir = Path().resolve()
    output = output_dir / "output_filename"
    if ext == None or ext == "png":
        # Save as png in folder script is run from
        plt.savefig(output, transparent=True)
    if ext == "gpickle":
        # Ditto as gpickle
        output = str(output) + ".gpickle"
        nx.write_gpickle(graph, output)

    # plt.axis("off")
    # # Print resulting edges
    # print("\n+++ Edges: +++ \n\n %s \n\n+++++++++++++++++++" % (edge_labels))
    # # Print execution time
    # print(
    #     "Processing transcript %s finished in --- %s seconds ---"
    #     % (filename, time.time() - start_time)
    # )

    # # Dont have this output dir so just exiting here for now
    # quit()

    # # --- Save graph image ---
    # # Initialize output
    # output_dir = "/Users/CN/Dropbox/speech_graphs/tool_demo/"
    # # # output_dir = '/Users/CN/Dropbox/speech_graphs/all_tats/'
    # # stripping '.txt' is not sufficient since some files have a dot in their filename (i.e. '22895-20-task-7g47-6377612-TAT10-9-1_otter.ai (1).txt') which throws an error when trying to save
    # valid_filename = filename.split(".")[0]
    # output = op.join(
    #     output_dir,
    #     "SpeechGraph_{0:04d}_{1}_{2}".format(
    #         selected_file, valid_filename, str(datetime.date.today())
    #     ),
    # )
    # plt.savefig(output, transparent=True)
    # # --- Save graph object ---
    # nx.write_gpickle(graph, output + ".gpickle")
    # # --- Show graph ---
    # # plt.show(block=False)
