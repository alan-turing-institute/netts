# pylint: disable=C0114, C0116
from netspy import __version__


def test_version() -> None:
    assert __version__ == "0.1.0"

def test_break() -> None:

    assert 5 == 2