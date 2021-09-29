"""Netspy. A package for constructing semantic speech networks from
speech transcripts.
"""

from networkx.classes.multidigraph import MultiDiGraph

from netspy.config import get_settings
from netspy.install_models import install_dependencies
from netspy.speech_graph import SpeechGraph, SpeechGraphFile
from netspy import config_file
from netspy.version import __version__


__all__ = [
    "install_dependencies",
    "SpeechGraph",
    "SpeechGraphFile",
    "get_settings",
    "MultiDiGraph",
    "config_file",
]
