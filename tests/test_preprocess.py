from typing import Dict, List

import pytest

from netts.preprocess import (
    expand_contractions,
    remove_interjections,
    replace_problematic_characters,
)

EXAMPLE_MAP = {
    "’": "'",
    "“": "",
    "”": "",
    "…": "...",
    "‘": "'",
    "–": "--",
    "\n": " ",
}

CONTRACTION_MAP = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have",
}

ENGLISH_INTERJECTIONS = [
    "Um",
    "um",
    "Uh",
    "uh",
    "Eh",
    "eh",
    "Ehm",
    "Em",
    "em",
    "Erm",
    "erm",
    "Ehhm",
    "ehhm",
    "Ehm",
    "ehm",
    "Mmm",
    "mmm",
    "Yeah",
    "yeah",
    "ah",
    "Ah",
    "Aah",
    "aah",
    "hmm",
    "hmmm",
    "Hmm",
    "Hmmm",
    "inaudible",
    "Inaudible",
]


@pytest.mark.parametrize(
    "character_map, text, expected",
    [
        ({"e": "p"}, "hello", "hpllo"),
        (
            EXAMPLE_MAP,
            "a man’s farther–wood ",
            "a man's farther--wood ",
        ),
        (
            {"a": "", "e": "", "i": "", "o": "", "u": ""},
            "this has no vowels",
            "ths hs n vwls",
        ),
        ({"a": "rrr"}, "hello", "hello"),
    ],
)
def test_problematic_characters(
    character_map: Dict[str, str], text: str, expected: str
) -> None:

    ret = replace_problematic_characters(text, character_map)
    assert ret == expected


@pytest.mark.parametrize(
    "contraction_map, text, expected",
    [
        (CONTRACTION_MAP, "ain't", "is not"),
        (CONTRACTION_MAP, "I can't wait", "I cannot wait"),
        (CONTRACTION_MAP, "y'all look funny", "you all look funny"),
    ],
)
def test_expand_contractions(
    contraction_map: Dict[str, str], text: str, expected: str
) -> None:

    ret = expand_contractions(text, contraction_map=contraction_map)
    # Test result is the same if we run on result of first run
    ret2 = expand_contractions(ret, contraction_map=contraction_map)

    assert ret == expected
    assert ret2 == expected


@pytest.mark.parametrize("original, expected", CONTRACTION_MAP.items())
def test_expand_contractions_maps(original: str, expected: str) -> None:

    ret = expand_contractions(original, CONTRACTION_MAP)
    assert ret == expected
    # Test result is the same if we run on result of first run
    assert ret == expand_contractions(ret, CONTRACTION_MAP)


@pytest.mark.parametrize(
    "interjections, text, expected",
    [
        (
            ENGLISH_INTERJECTIONS,
            "I'm not sure um, let me see, ah",
            "I am not sure , let me see ,",
        ),
        (ENGLISH_INTERJECTIONS, "Ah Are you sure eh", "Are you sure"),
        (ENGLISH_INTERJECTIONS, "Ah Are you sure, or not eh", "Are you sure , or not"),
    ],
)
def test_remove_interjections(
    interjections: List[str], text: str, expected: str
) -> None:

    assert remove_interjections(text, interjections, CONTRACTION_MAP) == expected
