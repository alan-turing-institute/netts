"""
visualise_paragraph_functions.py

Description:
               Functions to visualise sentence using OpenIE5 and Stanford CoreNLP

Author:       Caroline Nettekoven, 2020
"""
# pylint: disable=logging-format-interpolation
from netts.logger import logger

from copy import deepcopy
from itertools import chain

import numpy as np
import pandas as pd




def create_edges_ollie(ex_ollie):
    """Find edges and edge labels extracted by OpenIE5"""
    ollie_edges = []
    ollie_edges_text_excerpts = []
    ollie_one_node_edges = []
    ollie_one_node_edges_text_excerpts = []
    # Create nodes and edges
    for e, extract_val in enumerate(list(ex_ollie.values())):
        if extract_val != []:
            for extract in extract_val:
                # Get node 1
                node1 = extract["extraction"]["arg1"]["text"]
                node1 = node1.lower().strip()
                # Get relation
                relation = extract["extraction"]["rel"]["text"].lower().strip()
                # Get additional info
                context = extract["extraction"]["context"]
                if context is not None:
                    context = context["text"]
                # Get node 2
                node2 = ""
                node2_args = []
                #
                # Concatenate all text of argument 2
                for arg2 in extract["extraction"]["arg2s"]:
                    node2_args.append(arg2["text"])
                edge_text = (" ").join([node1, relation])
                if not node2_args:
                    ollie_one_node_edges_text_excerpts.append(edge_text)
                    a = (
                        node1,
                        "",
                        {
                            "relation": relation,
                            "confidence": extract["confidence"],
                            "context": context,
                            "negated": extract["extraction"]["negated"],
                            "passive": extract["extraction"]["passive"],
                            "extractor": "ollie",
                            "sentence": e,
                        },
                    )
                    ollie_one_node_edges.append(a)
                else:
                    node2 = node2_args[0]
                    node2_args.pop(0)
                    # Add nodes (arg1, arg2 and relationship)
                    node2 = node2.lower().strip()
                    edge_text = (" ").join([node1, relation, node2])
                    # If edge has two nodes and is not duplicate of previous edge, add edge
                    if edge_text not in ollie_edges_text_excerpts:
                        # ollie_edges.append([node1, node2])
                        ollie_edges_text_excerpts.append(edge_text)
                        a = (
                            node1,
                            node2,
                            {
                                "relation": relation,
                                "confidence": extract["confidence"],
                                "context": context,
                                "negated": extract["extraction"]["negated"],
                                "passive": extract["extraction"]["passive"],
                                "extractor": "ollie",
                                "sentence": e,
                                "node2_args": node2_args,
                            },
                        )
                        ollie_edges.append(a)
                        logger.info("  {} | {} | {}".format(node1, relation, node2))
    logger.info("++++ Created {} edges (ollie) ++++".format(len(ollie_edges)))
    return (
        ollie_edges,
        ollie_edges_text_excerpts,
        ollie_one_node_edges,
        ollie_one_node_edges_text_excerpts,
    )


def create_edges_stanza(ex_stanza):
    """Find edges and edge labels extracted by Stanza OpeniIE"""
    stanza_edges = []
    stanza_edges_text_excerpts = []
    for sentence in ex_stanza.sentence:
        for triple in sentence.openieTriple:
            node1 = triple.subject.lower()
            node2 = triple.object.lower()
            relation = triple.relation.lower()
            sentence_idx = triple.subjectTokens[0].sentenceIndex
            a = (
                node1,
                node2,
                {
                    "relation": relation,
                    # 'confidence': extract['confidence'],
                    # 'context': context,
                    # 'negated': extract['extraction']['negated'],
                    # 'passive': extract['extraction']['passive'],
                    "extractor": "stanza",
                    "sentence": sentence_idx,
                },
            )
            stanza_edges.append(a)
            stanza_edges_text_excerpts.append((" ").join([node1, relation, node2]))

            logger.info("  {} | {} | {}".format(node1, relation, node2))

    logger.info("++++ Created {} edges (stanza).  ++++".format(len(stanza_edges)))
    return stanza_edges, stanza_edges_text_excerpts


def get_word_types(ex_stanza):

    # First extract a list of determiners present in the text that need to be ignored when matching
    # (You don't want to match "the picture" and "the dog" on "the")
    no_noun = []
    poss_pronouns = []
    dts = []
    nouns = []
    nouns_origtext = []
    adjectives = []
    for sentence in ex_stanza.sentence:
        for token in sentence.token:
            # get nouns (proxy for nodes)
            if token.pos in ("PRP", "NN", "NNS"):
                if token.lemma not in nouns:
                    nouns.append(token.lemma)
                    nouns_origtext.append(token.word.lower())
            # Add everything that is not noun to list of words that should not get merged on later
            else:
                if token.lemma not in no_noun:
                    # get words that are not proper nouns (includes pronouns)
                    if token.pos == "PRP$":
                        # Lemma for poss pronoun 'his' is 'he', but 'he' counts as noun, therefore add orginial text for poss pronoun
                        no_noun.append(token.word.lower())
                        poss_pronouns.append(token.word.lower())
                    else:
                        no_noun.append(token.lemma)
                # get determiners
                if token.pos == "DT" and token.lemma not in dts:
                    dts.append(token.lemma)
                # get adjectives
                elif token.pos == "JJ" and token.lemma not in adjectives:
                    adjectives.append(token.lemma)
    logger.info("++++ Obtained word types ++++")
    return no_noun, poss_pronouns, dts, nouns, nouns_origtext, adjectives


def get_adj_edges(ex_stanza):
    """Extract adjective relations"""
    adjectives = []
    adjective_edges = []
    for idx_sentence, sentence in enumerate(ex_stanza.sentence):
        for word in sentence.enhancedDependencies.edge:
            if word.dep.split(":")[0] == "amod":
                # elif word.dep.split(':')[0] == 'advmod':
                source_idx = word.source - 1
                target_idx = word.target - 1
                # Test if source word is plural
                if (
                    sentence.token[source_idx].lemma
                    == sentence.token[source_idx].word.lower()
                ):
                    relation = "is"
                else:
                    relation = "are"
                relation = "(" + relation + ")"
                source_word = sentence.token[source_idx].word.lower()
                target_word = sentence.token[target_idx].word.lower()
                # if sentence.token[target_idx].pos == ""
                # logger.warning('{}'.format((' ').join(
                #     [token.word.lower() for token in sentence.token if token.word.lower()])))
                logger.info(
                    " {} | {} | {}".format(source_word, relation, target_word)
                )
                adjective_info = (
                    source_word,
                    target_word,
                    {
                        "relation": relation,
                        #    'confidence': None,
                        #    'context': None,
                        #    'negated': None,
                        #    'passive': None,
                        "extractor": "adjective",
                        "sentence": idx_sentence,
                    },
                )
                if target_word not in adjectives:
                    adjectives.append(target_word)
                adjective_edges.append(adjective_info)
        logger.info("++++ Created {} adj edges ++++".format(len(adjective_edges)))
        return adjectives, adjective_edges


# ------------------------------------------------------------------------------
# ------- Extract preposition relations -------
# Separate any preposition relations in node name synonyms


def get_prep_edges(ex_stanza):
    """Get a list of prepositions and track where they point to"""
    prepositions = []
    preposition_edges = []
    for idx_sentence, sentence in enumerate(ex_stanza.sentence):
        for word in sentence.enhancedDependencies.edge:
            if word.dep.split(":")[0] == "nmod" and len(word.dep.split(":")) > 1:
                source_idx = word.source - 1
                target_idx = word.target - 1
                extractor_type = "preposition"
                preposition = word.dep.split(":")[1]
                if preposition == "poss":
                    preposition = "(of) [poss]"
                    extractor_type = "possession"
                source_word = sentence.token[source_idx].word.lower()
                target_word = sentence.token[target_idx].word.lower()
                # logger.warning('{}'.format((' ').join(
                #     [token.word.lower() for token in sentence.token if token.word.lower()])))
                # logger.warning('  {} | {} | {}'.format(
                #     sentence.token[source_idx].word.lower(), preposition, sentence.token[target_idx].word.lower()))
                # Do not extract "kind of". Leads to cluttering.
                logger.info(
                    "  {} | {} | {}".format(source_word, preposition, target_word)
                )
                invalid_preposition_edges = ["kind of", "sort of", "type of"]
                if (" ").join(
                    [source_word, preposition]
                ) not in invalid_preposition_edges:
                    preposition_info = (
                        source_word,
                        target_word,
                        {
                            "relation": preposition,
                            #    'confidence': None,
                            #    'context': None,
                            #    'negated': None,
                            #    'passive': None,
                            "extractor": extractor_type,
                            "sentence": idx_sentence,
                        },
                    )
                    prepositions.append(preposition)
                    preposition_edges.append(preposition_info)
    logger.info(
        "++++ Created {} preposition edges ++++".format(len(preposition_edges))
    )
    return prepositions, preposition_edges


def get_obl_edges(ex_stanza):
    """Extract oblique relations.

    Get a list of obliques and track where they point to
    N.B. The oblique relation is used for a nominal (noun, pronoun, noun phrase) functioning as a non-core (oblique) argument or adjunct.
    This means that it functionally corresponds to an adverbial attaching to a verb, adjective or other adverb.
    More info: https://universaldependencies.org/u/dep/obl.html
    Example: 'The cat was chased by the dog.' Cat --obl--> dog
    """
    obliques = []
    oblique_edges = []
    for idx_sentence, sentence in enumerate(ex_stanza.sentence):
        for word in sentence.enhancedDependencies.edge:
            if word.dep.split(":")[0] == "obl" and len(word.dep.split(":")) > 1:
                target_idx = word.target - 1
                extractor_type = "oblique"
                oblique = word.dep.split(":")[1]
                target_word = sentence.token[target_idx].word.lower()
                # Find word that points to oblique edge source - that's the actual source word of this edge ("man[source] leaning against[oblique relation]
                # wall[target]")
                intermediate_source_idx = word.source
                source_word = [
                    sentence.token[dependency.target - 1].word.lower()
                    for dependency in sentence.enhancedDependencies.edge
                    if dependency.source == intermediate_source_idx
                    and dependency.dep == "nsubj"
                ]
                # and (sentence.token[dependency.target].pos == "PRP"
                # or sentence.token[dependency.target].pos == "NN"
                # or sentence.token[dependency.target].pos == "NNS")
                if source_word == []:
                    continue

                source_word = source_word[0]
                logger.info(
                    " {} | {} | {}".format(source_word, oblique, target_word)
                )
                oblique_info = (
                    source_word,
                    target_word,
                    {
                        "relation": oblique,
                        #    'confidence': None,
                        #    'context': None,
                        #    'negated': None,
                        #    'passive': None,
                        "extractor": extractor_type,
                        "sentence": idx_sentence,
                    },
                )
                obliques.append(oblique)
                oblique_edges.append(oblique_info)
    logger.info("++++ Created {} oblique edges ++++".format(len(oblique_edges)))
    return obliques, oblique_edges


def add_obl_edges(edges, oblique_edges):
    """Add oblique relations that were also extracted by ollie."""
    for oblique_edge in oblique_edges:
        oblique_edge_text = (" ").join([oblique_edge[2]["relation"], oblique_edge[1]])
        # logger.warning(oblique_edge_text)
        for edge_info in edges:
            if "node2_args" in edge_info[2] and edge_info[2]["node2_args"] != []:
                # logger.warning(oblique_edge[0])
                # logger.warning(edge_info[2]['node2_args'][0])
                if (
                    edge_info[2]["relation"] == oblique_edge[0]
                    and edge_info[2]["node2_args"][0] == oblique_edge_text
                ):
                    logger.info(
                        "{} : {} \t {} : {}".format(
                            edge_info[2]["relation"],
                            oblique_edge[0],
                            edge_info[2]["node2_args"][0],
                            oblique_edge_text,
                        )
                    )
                    new_oblique_edge = (
                        edge_info[1],
                        oblique_edge[1],
                        {
                            "relation": oblique_edge[2]["relation"],
                            #    'confidence': None,
                            #    'context': None,
                            #    'negated': None,
                            #    'passive': None,
                            "extractor": "oblique",
                            "sentence": oblique_edge[2]["sentence"],
                        },
                    )
                    if new_oblique_edge not in edges:
                        edges.append(new_oblique_edge)
    logger.info(
        "++++ Added {} oblique edges. Total edges: {} ++++".format(
            len(oblique_edges), len(edges)
        )
    )
    return edges


def get_node_synonyms(ex_stanza, no_noun):
    """Find node name synonyms in coreference chain.

    Extract proper node name and alternative node names"""
    # pylint: disable=too-many-branches

    node_name_synonyms = {}
    for coreference in ex_stanza.corefChain:
        proper_nn = []
        alt_nn = []
        for mention in coreference.mention:
            mention_info = ex_stanza.sentence[mention.sentenceIndex].token[
                mention.beginIndex : mention.endIndex  # noqa: E203
            ]

            if mention.mentionType in ("NOMINAL", "PROPER"):
                # Make the "proper" or "nominal" mention the node label
                node_name_list = [
                    node_part.word.lower()
                    for node_part in mention_info
                    if not node_part.pos == "PRP$"
                ]
                # Concatenate node names that consist of several tokens
                if len(node_name_list) > 1:
                    node_name = (" ").join(node_name_list)
                else:
                    node_name = node_name_list[0]
                #
                # Append proper node name only if it is different from all other proper node names
                if node_name not in proper_nn:
                    proper_nn.append(node_name)
                    alt_nn.append((mention.sentenceIndex, node_name))
            else:
                alternative_node_name = [
                    node_part.word.lower()
                    for node_part in mention_info
                    if node_part.word.lower() not in no_noun
                ]
                if len(alternative_node_name) > 1:
                    alternative_node_name = (" ").join(alternative_node_name)
                elif alternative_node_name != []:
                    alternative_node_name = alternative_node_name[0]
                elif (
                    alternative_node_name == []
                    and len(mention_info) == 1
                    and (
                        mention_info[0].pos[0:3] == "PRP"
                        or mention_info[0].pos[0:3] == "DT"
                    )
                ):
                    # Mentions that only consist of one possessive pronoun are still valid mentions ("my"/"me" should be merged with "I").
                    # (But mentions that consist of a pronoun plus another noun should be cleaned of the pronoun ("his hands" should only be merged with
                    # another mention of "hands", and not with another mention of "him").)
                    alternative_node_name = mention_info[0].word.lower()
                #
                # Keep track of sentence the reference appeared in
                alt_nn.append((mention.sentenceIndex, alternative_node_name))
        if not proper_nn:
            for mention in coreference.mention:
                mention_info = ex_stanza.sentence[mention.sentenceIndex].token[
                    mention.beginIndex : mention.endIndex  # noqa: E203
                ]
                for token in mention_info:
                    if token.lemma.lower() == token.word.lower():
                        proper_nn.append(token.lemma.lower())
                        continue
            if not proper_nn:
                # If no proper node name could be found (either as noun or as lemma), set first mention of node as proper node name
                proper_nn.append(alt_nn[0][1])
        node_name_synonyms[proper_nn[0]] = alt_nn
    logger.info(node_name_synonyms)
    logger.info(
        "++++ Obtained {} node synonyms ++++".format(len(node_name_synonyms))
    )
    return node_name_synonyms


def split_node_synonyms(node_name_synonyms, preposition_edges, edges):
    """Split nodes in node_name_synonyms

    splits nodes that are joined by preposition and adds preposition edge to graph
    """
    # pylint: disable=too-many-nested-blocks

    for preposition_edge in preposition_edges:
        preposition = preposition_edge[2]["relation"]
        keys = list(node_name_synonyms.keys())
        values = list(node_name_synonyms.values())
        for proper_nn in keys:
            if preposition in proper_nn.split(" "):
                part1 = proper_nn.split(preposition)[0].strip()
                # part2 = proper_nn.split(preposition)[1].strip()
                node_name_synonyms[part1] = node_name_synonyms.pop(
                    proper_nn
                )  # Set first part of preposition-joined node name as name
                for n, key in enumerate(keys):
                    if key == proper_nn:
                        keys[n] = part1
                if preposition_edge not in edges:
                    edges.append(preposition_edge)
        for synonym_idx, alt_nns in enumerate(values):
            # logger.warning(synonym_idx, alt_nns)
            for a, (sentence_idx, alt_nn) in enumerate(alt_nns):
                # logger.warning(sentence_idx, alt_nn)
                if (
                    preposition in alt_nn.split(" ")
                    and sentence_idx == preposition_edge[2]["sentence"]
                ):
                    part1 = alt_nn.split(preposition)[0].strip()
                    alt_nns_new = (
                        alt_nns[:a]
                        + [(sentence_idx, part1)]
                        + alt_nns[a + 1 :]  # noqa: E203
                    )
                    # part2 = alt_nn.split(preposition)[1].strip()
                    node_name_synonyms[keys[synonym_idx]] = alt_nns_new
                    for n, value in enumerate(values):
                        if value == alt_nns:
                            values[n] = alt_nns_new
                    if preposition_edge not in edges:
                        edges.append(preposition_edge)
    logger.info("++++ Split node name synonyms on prepositions. ++++")
    return edges, node_name_synonyms


def split_nodes(edges, preposition_edges, no_noun):
    """Split nodes in edges

    Find nodes that include preposition-joined nouns and split the nodes if the second noun appears in any other edge but the current
    """
    # pylint: disable=too-many-locals, invalid-name, too-many-nested-blocks
    for e, edge_info in enumerate(edges):
        edge = edge_info[:2]
        new_edge = list(edge_info)  # Make edge into list to ammend it
        # Make list of nodes that are not current node
        other_edges = [list(x[:2]) for i, x in enumerate(edges) if i != e]
        other_edges = list(chain.from_iterable(other_edges))
        for n, node in enumerate(edge):
            # Test if node includes preposition
            for preposition_edge in preposition_edges:
                preposition = preposition_edge[2]["relation"]
                # preposition_match_idx = [m for m, match in enumerate(
                #     node.split(' ')) if preposition == match]
                match_idx = []
                # Split on preposition
                match_idx = [
                    m
                    for m, match in enumerate(node.split(" "))
                    if preposition == match and m > 1
                ]
                if match_idx != []:
                    m = match_idx[0]
                    part1 = (" ").join(node.split(" ")[:m]).strip()
                    part2 = (" ").join(node.split(" ")[m:]).strip()
                    # If second part of node is anywhere else in edges, then split
                    # Find where part1 does not appear in node but part2 appears (something other than prepositions or no_noun element)
                    p2_words = [
                        w for w in part2.split(" ") if w not in no_noun
                    ]  # remove stopwords
                    p2_list = []
                    for x in other_edges:
                        for p2 in p2_words:
                            p2_list.append(p2 in x.split(" "))
                    p1_words = [
                        w for w in part1.split(" ") if w not in no_noun
                    ]  # remove stopwords
                    p1_list = []
                    for x in other_edges:
                        for p1 in p1_words:
                            p1_list.append(p1 not in x.split(" "))
                    if any(p1_list and p2_list):
                        logger.info(
                            "{} \t\t|\t {}  -- Adding {}".format(
                                part1, part2, preposition_edge
                            )
                        )
                        new_edge[n] = part1
                # Split on implied preposition (if edge is possessive pronoun edge: 'their hats' => 'their' --(of)[poss]--> 'hats')
                elif (
                    match_idx == []
                    and "[poss]" in preposition
                    and len(node.split(" ")) > 1
                ):
                    match_idx = [
                        m
                        for m, match in enumerate(node.split(" "))
                        if match == preposition_edge[1]
                        and len(node.split(" ")) > m + 1
                        and node.split(" ")[m + 1] == preposition_edge[0]
                    ]
                    if match_idx != []:
                        m = match_idx[0]
                        part1 = (" ").join(node.split(" ")[: m + 1]).strip()
                        part2 = (
                            (" ").join(node.split(" ")[m + 1 :]).strip()  # noqa: E203
                        )
                        new_edge[n] = part2
                        logger.info(
                            "{} \t\t|\t {}  -- Adding {}".format(
                                part1, part2, preposition_edge
                            )
                        )
                edges[e] = tuple(new_edge)
                if preposition_edge not in edges:
                    edges.append(preposition_edge)
    logger.info("++++ Split nodes on prepositions. ++++")
    return edges


def merge_corefs(edges, node_name_synonyms, no_noun, poss_pronouns):
    """Merge nodes that are separate mentions of the same entity.

    Merge nodes that are separate mentions of the same entity using the coreference relations chain
    Replace node name with proper node name and edge_label
    Method: test if node text appears in list of alternative node names or is part of the proper node name and replace with the full proper node name
    """
    # pylint: disable=too-many-branches, too-many-nested-blocks
    orig_edges = deepcopy(edges)
    for e, edge_info in enumerate(edges):
        # logger.warning(e, edge)
        edge = edge_info[:2]
        sentence_idx_edge = edge_info[2]["sentence"]
        new_edge = list(edge_info)  # Make edge into list to ammend it
        for n, node in enumerate(edge):
            #
            found_match = False
            for node_token in node.split(" "):
                if found_match is False:
                    if node_token in no_noun:
                        if node_token in poss_pronouns and len(node.split(" ")) == 1:
                            pass  # Continue searching for match of a non-noun word if this node only consists of a pronoun
                        else:
                            # If token is anything other than a noun or a possessive pronoun, move on to the next token.
                            continue
                    elif node_token in list(node_name_synonyms.keys()):
                        # Replace with proper node name if node is the same as proper node name
                        proper_node_name = list(node_name_synonyms.keys())[
                            list(node_name_synonyms.keys()).index(node_token)
                        ]
                        logger.info(
                            "Replaced '{}' with '{}' in {}".format(
                                node, proper_node_name, edge
                            )
                        )
                        new_edge[n] = proper_node_name
                        found_match = True
                    for ann, alternative_mentions in enumerate(
                        list(node_name_synonyms.values())
                    ):
                        for sentence_idx_mention, mention in alternative_mentions:
                            # logger.warning(sentence_idx_mention, mention)
                            for mention_part in mention.split(" "):
                                if (
                                    mention_part == node_token
                                    and sentence_idx_edge == sentence_idx_mention
                                ):
                                    # Replace with proper node name if node is part of one of the alternative node names
                                    proper_node_name = list(node_name_synonyms.keys())[
                                        ann
                                    ]
                                    logger.info(
                                        "Replaced '{}' with '{}' in {}".format(
                                            node, proper_node_name, edge
                                        )
                                    )
                                    new_edge[n] = proper_node_name
                                    found_match = True
                else:
                    # logger.warning('Moving on...')
                    pass
        edges[e] = tuple(new_edge)
    logger.info("++++ Merged nodes that are referenced several times. ++++")
    return edges, orig_edges


# for mention_part in mention.split(' '):
#     if mention_part == node_token and sentence_idx_edge == sentence_idx_mention:
#         proper_node_name = list(
#             node_name_synonyms.keys())[ann]
#         logger.warning("Replaced '{}' with '{}' in {}".format(
#             node, proper_node_name, edge))
#     else:
#         proper_node_name = list(
#             node_name_synonyms.keys())[ann]
#         logger.warning("Does not match '{}' with '{}' in {}".format(
#             node, proper_node_name, edge))
# --------------------------------------------------------------------------------------------


def clean_nodes(edges, nouns, adjectives):
    """Clean node names from determiners, adjectives and other nouns appearing after first noun in the node."""
    for e, edge_info in enumerate(edges):
        edge = edge_info[:2]
        new_edge = list(edge_info)  # Make edge into list to ammend it
        # Make list of nodes that are not current node
        for n, node in enumerate(edge):
            node_noun = [node_part for node_part in node.split() if node_part in nouns]
            node_adjective = [
                node_part for node_part in node.split() if node_part in adjectives
            ]
            # logger.warning('{} : {}  ======= {}'.format(node, node_noun, node_adjective))
            if node_noun != []:
                new_node_name = node_noun[0]
                new_edge[n] = new_node_name
            elif node_noun == [] and node_adjective != []:
                new_node_name = node_adjective[0]
                new_edge[n] = new_node_name
        edges[e] = tuple(new_edge)
    logger.info("++++ Cleaned nodes. ++++")
    return edges


def clean_parallel_edges(edges):
    """Check parallel edges aren't duplicates.

    Check that each parallel edges (i.e. where node1 and node2 are connected by several relations)
    are not duplicates of each other, but in fact represent different relations of the same pair of nodes.
    """
    # pylint: disable=too-many-locals, unused-variable
    # Loop through parallel edges and leave parallel edges only if they represent different relations
    node1 = [edge[0] for edge in edges]
    node2 = [edge[1] for edge in edges]
    relations = [edge[2]["relation"] for edge in edges]
    extractors = [edge[2]["extractor"] for edge in edges]
    confidence = [
        edge[2]["confidence"] if "confidence" in edge[2].keys() else 0 for edge in edges
    ]

    # Construct dataframe of edges to find duplicate rows
    df = pd.DataFrame(
        {
            "n1": node1,
            "n2": node2,
            "relation": relations,
            "extractor": extractors,
            "confidence": confidence,
        }
    )

    # Find duplicate rows
    boo_similar = np.where(df.duplicated(subset=["n1", "n2", "relation"]).values)

    # Of the duplicate rows, pick the row that most represents the proper relation (highest confidence in Ollie for example)
    all_chosen_rows = []
    logger.info("@@@@%s", {boo_similar[0].shape[0]})
    for b in range(0, boo_similar[0].shape[0]):
        # If both extracted by Ollie, keep the one with the higher confidence

        dupl = df.iloc[boo_similar[0][b]]
        node_one = dupl["n1"]  # noqa: F841
        node_two = dupl["n2"]  # noqa: F841
        relation = dupl["relation"]  # noqa: F841
        extractor = dupl["extractor"]  # noqa: F841

        duplicate_rows = df.query(
            "n1 == @node_one & n2 == @node_two & relation == @relation"
        )

        if len(duplicate_rows) == len(duplicate_rows.query('extractor == "ollie"')):
            # If all duplicate rows were extracted by ollie, take the extraction with the highest confidence

            chosen_row = duplicate_rows.index[
                (duplicate_rows.confidence == max(duplicate_rows.confidence))
            ][0]
            if chosen_row not in all_chosen_rows:
                all_chosen_rows.append(chosen_row)

        elif len(duplicate_rows) == len(duplicate_rows.duplicated(keep=False)):
            # If all duplicate rows have exactly the same values in all of the rows, then choose the last of the rows
            chosen_row = duplicate_rows.index[-1]
            if chosen_row not in all_chosen_rows:
                all_chosen_rows.append(chosen_row)
                logger.info(
                    "\n--- Duplicates ---{}\n --- Chosen --- :\n{}".format(
                        duplicate_rows, duplicate_rows.iloc[-1].to_frame().T
                    )
                )

    # Remove all duplicate edges
    all_duplicate_rows = df.duplicated(subset=["n1", "n2", "relation"], keep=False)
    all_duplicate_rows = np.where(all_duplicate_rows)[0].tolist()
    clean_edges = [edge for e, edge in enumerate(edges) if e not in all_duplicate_rows]

    # Add chosen edges of the duplicate edges
    for row in all_chosen_rows:
        clean_edges.append(edges[row])

    # Return edges without duplicates
    logger.info("++++ Cleaned parallel edges from duplicates. ++++")
    return clean_edges


def add_adj_edges(edges, adjective_edges, add_adjective_edges):
    """Add adjective edges."""
    if add_adjective_edges:
        for adjective_edge in adjective_edges:
            edges.append(adjective_edge)
    logger.info("++++ Added adjective edges: {} ++++".format(add_adjective_edges))
    return edges


def add_prep_edges(edges, preposition_edges, add_all_preposition_edges):
    """Add all other preposition edges."""
    if add_all_preposition_edges:
        for preposition_edge in preposition_edges:
            if preposition_edge not in edges:
                edges.append(preposition_edge)
    logger.info(
        "++++ Added all preposition edges: {} ++++".format(add_all_preposition_edges)
    )
    return edges


def get_unconnected_nodes(edges, orig_edges, nouns):

    # Get list of current and original nodes
    list_of_nodes = []
    for edge in edges:
        list_of_nodes.extend([edge[0], edge[1]])
    for orig_edge in orig_edges:
        list_of_nodes.extend([orig_edge[0], orig_edge[1]])

    # Get list of unconnected nodes
    unconnected_nodes = []
    for noun in nouns:
        node_is_in_network = any(noun.lower() in node.lower() for node in list_of_nodes)
        if not node_is_in_network:
            unconnected_nodes.append(noun)
    logger.info("++++ Obtained unconnected nodes ++++")
    return unconnected_nodes
