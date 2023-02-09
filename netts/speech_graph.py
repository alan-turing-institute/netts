import pickle
from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import networkx as nx

from netts import MultiDiGraph, preprocess
from netts.clients import CoreNLPClient, OpenIEClient
from netts.config_file import PreProcessing
from netts.logger import logger
from netts.nlp_helper_functions import get_transcript_properties
from netts.visualise_paragraph_functions import (
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


class SpeechGraph:
    def __init__(self, transcript: str) -> None:

        self.transcript = transcript
        self.graph: Optional[MultiDiGraph] = None

    def get_tidy_text(self, preprocess_config: PreProcessing) -> str:
        text = self.transcript

        # ------- Clean text -------
        # Need to replace problematic symbols before ANYTHING ELSE, because other tools cannot work with problematic symbols
        text = preprocess.replace_problematic_characters(
            self.transcript, preprocess_config.problematic_symbols
        )  # replace ’ with '

        text = preprocess.expand_contractions(
            text, preprocess_config.contractions
        )  # expand it's to it is

        text = preprocess.remove_interjections(
            text,
            preprocess_config.interjections,
            preprocess_config.contractions,
        )  # remove Ums and Mmms

        # ToDo: Refactor and add test
        text = preprocess.remove_irrelevant_text(text)

        text = text.strip()  # remove trailing and leading whitespace
        return text

    def process(
        self,
        corenlp_client: CoreNLPClient,
        openie_client: OpenIEClient,
        preprocess_config: PreProcessing,
    ) -> MultiDiGraph:
        # pylint: disable=unused-variable, too-many-locals

        logger.debug("%s", self.transcript)

        text = self.get_tidy_text(preprocess_config)

        # ------------------------------------------------------------------------------
        # ------- Print cleaned text -------
        logger.debug("\n+++ Paragraph: +++ \n\n %s \n\n+++++++++++++++++++", text)

        # ------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------
        # ------- Run Stanford CoreNLP (Stanza) -------
        # Annotate and extract with Stanford CoreNLP
        ex_stanza = corenlp_client.annotate(text)

        # ------- Basic Transcript Descriptors -------
        n_tokens, n_sentences, _ = get_transcript_properties(ex_stanza)

        # ------------------------------------------------------------------------------
        # ------- Run OpenIE5 (Ollie) -------
        # Ollie can handle more than one sentence at a time, but need to loop through sentences to keep track of sentence index

        ex_ollie = {}
        for i, sentence in enumerate(ex_stanza.sentence):
            if len(sentence.token) > 1:
                logger.debug("====== Submitting sentence %s tokens =======", i)
                sentence_text = (" ").join(
                    [
                        token.originalText
                        for token in sentence.token
                        if token.originalText
                    ]
                )
                logger.debug("%s", sentence_text)
                # prinst("{}".format(sentence_text))

                try:
                    extraction = openie_client.extract(sentence_text)
                    ex_ollie[i] = extraction
                except Exception as e:
                    logger.warning(f'====== Skipping sentece {i+1}: Unknown Client Error =======')
                    
            else:
                logger.warning(
                    '====== Skipping sentence %s: Sentence has too few tokens: "%s" =======',
                    i + 1,
                    (" ").join(
                        [
                            token.originalText
                            for token in sentence.token
                            if token.originalText
                        ]
                    ),
                )

        # --------------------- Create ollie edges ---------------------------------------
        (
            ollie_edges,
            ollie_edges_text_excerpts,
            ollie_one_node_edges,
            ollie_one_node_edges_text_excerpts,
        ) = create_edges_ollie(ex_ollie)

        edges = ollie_edges
        # --------------------- Create stanza edges ---------------------------------------
        stanza_edges, stanza_edges_text_excerpts = create_edges_stanza(ex_stanza)
        # If Ollie was unable to detect any edges, use stanza edges

        if len(ollie_edges) == 0 and len(stanza_edges) != 0:
            edges = stanza_edges
            logger.info(
                "++++ Ollie detected %s edges, but stanza detected %s. Therefore added edges detected by stanza.  ++++",
                len(ollie_edges),
                len(stanza_edges),
            )
        elif len(ollie_edges) == 0 and len(stanza_edges) == 0:
            logger.info(
                "++++ Ollie detected %s edges and stanza also detected %s. No stanza edges were added. ++++",
                len(ollie_edges),
                len(stanza_edges),
            )

        else:
            logger.info(
                "++++ Ollie detected %s edges, so no stanza edges were added.  ++++",
                len(ollie_edges),
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
        edges, orig_edges = merge_corefs(
            edges, node_name_synonyms, no_noun, poss_pronouns
        )

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
        # fig = plt.figure(figsize=(25.6, 9.6))

        # Construct Speech Graph with properties: number of tokens, number of sentences, unconnected nodes as graph property
        self.graph = nx.MultiDiGraph(
            transcript=self.transcript,
            sentences=n_sentences,
            tokens=n_tokens,
            unconnected_nodes=unconnected_nodes,
        )
        # Add Edges
        self.graph.add_edges_from(edges)

        return self.graph

    def plot_graph(self, ax=None, **kwargs) -> None:

        if not self.graph:
            raise RuntimeError("self.graph does not exist")

        if not ax:
            _, ax = plt.subplots(figsize=(25.6, 9.6))

        # Plot Graph and add edge labels
        pos = nx.spring_layout(self.graph, seed=20)
        nx.draw(
            self.graph,
            pos,
            ax=ax,
            edge_color="black",
            width=1,
            linewidths=1,
            node_size=500,
            node_color="pink",
            alpha=0.9,
            labels={node: node for node in self.graph.nodes()},
            **kwargs,
        )

        edge_labels = {(u, v): d["relation"] for u, v, d in self.graph.edges(data=True)}

        nx.draw_networkx_edge_labels(
            self.graph, pos, edge_labels=edge_labels, font_color="red"
        )

        return ax


class SpeechGraphFile(SpeechGraph):
    def __init__(
        self,
        file: Path,
        output_dir: Optional[Path] = None,
        load_if_exists: bool = True,
    ) -> None:

        self.file = file
        self.output_dir = output_dir

        if not self.check_input_file_exists():
            raise IOError(f"File {self.file} does not exist")

        super().__init__(
            transcript=self.file.read_text(encoding="utf-8"),
        )

        if load_if_exists:
            self.load_graph()

    def check_input_file_exists(self) -> bool:

        return self.file.exists() and self.file.is_file()

    @property
    def output_file(self) -> Optional[Path]:
        if self.output_dir:
            return self.output_dir / (self.file.stem + ".pickle")
        return None

    def output_graph_file(self, output_format: str = "png") -> Path:
        return self.output_file.parent / (self.output_file.stem + "." + output_format)

    @property
    def missing(self) -> bool:
        return not self.output_file.exists()

    def load_graph(self) -> None:

        if not self.missing:
            self.graph = pickle.loads(self.output_file.read_bytes())

    def dump(self, output_dir: Optional[Union[Path, str]] = None) -> None:

        if not output_dir:

            if not self.output_dir:
                raise IOError(
                    "Either initialise SpeechGraphFile with output_dir or pass output_dir argument to dump"
                )

        if not self.graph:
            raise RuntimeError("Graph does not exist")

        # Ensure directory exists
        self.output_dir.mkdir(exist_ok=True)

        with self.output_file.open(mode="wb") as output_f:
            pickle_graph(self.graph, output_f)


def pickle_graph(graph: MultiDiGraph, file, protocol=pickle.HIGHEST_PROTOCOL) -> None:

    pickle.dump(graph, file, protocol)
