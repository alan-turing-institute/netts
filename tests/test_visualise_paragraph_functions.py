"""Unit tests for the nlp_helper_functions module."""
from pytest_mock import MockerFixture

from netts.visualise_paragraph_functions import (
    clean_parallel_edges,
    get_node_synonyms,
    get_word_types,
)


def test_clean_parallel_edges() -> None:
    edge_one = (
        "girl",
        "maid",
        {"relation": "to be", "confidence": 0.5, "extractor": "ollie"},
    )
    edge_two = (
        "i",
        "it",
        {"relation": "am not", "confidence": 0.3, "extractor": "ollie"},
    )
    graph = [edge_one, edge_two]

    # We don't expect the function to change this graph at all
    expected = graph
    actual = clean_parallel_edges(graph)  # type: ignore[no-untyped-call]
    assert actual == expected

    edge_three = (
        "girl",
        "maid",
        {"relation": "to be", "confidence": 0.99, "extractor": "ollie"},
    )
    edge_four = ("girl", "maid", {"relation": "to be", "extractor": "ollie"})

    graph = [edge_one, edge_three, edge_four]  # type: ignore[list-item]

    # We expect duplicates to be removed and only the highest confidence edges to remain
    expected = [edge_three]
    actual = clean_parallel_edges(graph)  # type: ignore[no-untyped-call]
    assert actual == expected


def test_get_word_types(mocker: MockerFixture) -> None:
    stanza = mocker.Mock()
    sentence = mocker.Mock()
    token = mocker.Mock()
    token.pos = "NNS"
    token.lemma = "lemma"
    token.word = "WORD"
    sentence.token = [token]
    stanza.sentence = [sentence]

    no_noun, poss_pronouns, dts, nouns, nouns_origtext, adjectives = get_word_types(  # type: ignore[no-untyped-call]
        stanza
    )
    del no_noun, poss_pronouns, dts, adjectives
    assert nouns == ["lemma"]
    assert nouns_origtext == ["word"]


def test_get_node_synonyms(mocker: MockerFixture) -> None:
    stanza = mocker.Mock()
    coref = mocker.Mock()
    mention = mocker.Mock()
    sentence = mocker.Mock()
    token = mocker.Mock()
    token.word.lower.return_value = "word"

    mention.mentionType = "NOMINAL"
    mention.sentenceIndex = 0
    mention.beginIndex = 0
    mention.endIndex = 1

    sentence.token = [token]
    coref.mention = [mention]
    stanza.corefChain = [coref]
    stanza.sentence = [sentence]

    node_name_synonyms = get_node_synonyms(stanza, [])  # type: ignore[no-untyped-call]
    assert node_name_synonyms == {"word": [(0, "word")]}
