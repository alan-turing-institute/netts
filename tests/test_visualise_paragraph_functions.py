"""Unit tests for the nlp_helper_functions module."""
from pytest_mock import MockerFixture

from netspy.visualise_paragraph_functions import get_node_synonyms, get_word_types


def test_get_word_types(mocker: MockerFixture) -> None:
    stanza = mocker.Mock()
    sentence = mocker.Mock()
    token = mocker.Mock()
    token.pos = "NNS"
    token.lemma = "lemma"
    token.word = "WORD"
    sentence.token = [token]
    stanza.sentence = [sentence]

    no_noun, poss_pronouns, dts, nouns, nouns_origtext, adjectives = get_word_types(
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

    node_name_synonyms = get_node_synonyms(stanza, [])
    assert node_name_synonyms == {"word": [(0, "word")]}
