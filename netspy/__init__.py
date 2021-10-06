"""Netspy. A package for constructing semantic speech networks from
speech transcripts.
"""
from networkx.classes.multidigraph import MultiDiGraph
from stanza.server import CoreNLPClient

from netspy import preprocess  # noqa: F401 # pylint: disable=E0012,F401
from netspy import config_file
from netspy.config import get_settings
from netspy.context_manager import OpenIEClient
from netspy.install_models import install_dependencies, set_netspy_home
from netspy.speech_graph import SpeechGraph, SpeechGraphFile
from netspy.version import __version__

__all__ = [
    "install_dependencies",
    "set_netspy_home",
    "SpeechGraph",
    "SpeechGraphFile",
    "get_settings",
    "MultiDiGraph",
    "config_file",
    "OpenIEClient",
    "CoreNLPClient",
]
