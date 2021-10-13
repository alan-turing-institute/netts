"""Unit tests for the nlp_helper_functions module."""
from netspy.nlp_helper_functions import (
    remove_interjections,
    replace_problematic_symbols,
)


def test_replace_problematic_symbols() -> None:
    text = "’ “ ” … ‘ – \n"
    expected = "'   ... ' -  "
    actual = replace_problematic_symbols(text)
    assert actual == expected


def test_process_sent() -> None:
    pass


def test_remove_interjections() -> None:
    text = "Hmmm yes aah no"
    expected = "yes no"
    actual = remove_interjections(text)
    assert d nactual == expected
