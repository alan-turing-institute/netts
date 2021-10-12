"""Netspy. A package for constructing semantic speech networks from
speech transcripts.
"""
from networkx.classes.multidigraph import MultiDiGraph
from stanza.server import CoreNLPClient

from netspy import preprocess  # noqa: F401 # pylint: disable=E0012,F401
from netspy.config import get_settings
from netspy.config_file import Config
from netspy.clients import OpenIEClient
from netspy.install_models import install_dependencies
from netspy.speech_graph import SpeechGraph, SpeechGraphFile
from netspy.version import __version__

__all__ = [
    "install_dependencies",
    "SpeechGraph",
    "SpeechGraphFile",
    "Config",
    "get_settings",
    "MultiDiGraph",
    "OpenIEClient",
    "CoreNLPClient",
]
