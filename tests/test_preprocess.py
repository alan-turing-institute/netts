import pytest
from netspy.preprocess import replace_problematic_characters

EXAMPLE_MAP = {
    "’": "'",
    "“": "",
    "”": "",
    "…": "...",
    "‘": "'",
    "–": "--",
    "\n": " ",
}


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
    ],
)
def test_problematic_characters(character_map, text, expected):

    ret = replace_problematic_characters(text, character_map)
    assert ret == expected
