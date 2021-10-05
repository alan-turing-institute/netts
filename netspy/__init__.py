"""Netspy. A package for constructing semantic speech networks from
speech transcripts.
"""
from networkx.classes.multidigraph import MultiDiGraph
from stanza.server import CoreNLPClient

from netspy import preprocess  # noqa: F401 # pylint: disable=E0012,F401
from netspy.config import get_settings
from netspy.context_manager import OpenIEClient
from netspy.install_models import install_dependencies
from netspy.speech_graph import SpeechGraph, SpeechGraphFile

__version__ = "0.1.0"

__all__ = [
    "install_dependencies",
    "SpeechGraph",
    "SpeechGraphFile",
    "get_settings",
    "MultiDiGraph",
    "OpenIEClient",
    "CoreNLPClient",
]
