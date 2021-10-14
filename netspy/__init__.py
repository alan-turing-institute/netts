"""Netspy. A package for constructing semantic speech networks from
speech transcripts.
"""
from networkx.classes.multidigraph import MultiDiGraph


from netspy import preprocess  # noqa: F401 # pylint: disable=E0012,F401
from netspy.clients import OpenIEClient, CoreNLPClient
from netspy.config import get_settings
from netspy.config_file import Config
from netspy.install_models import install_dependencies
from netspy.speech_graph import SpeechGraph, SpeechGraphFile

__all__ = [
    "install_dependencies",
    "preprocess",
    "SpeechGraph",
    "SpeechGraphFile",
    "Config",
    "get_settings",
    "MultiDiGraph",
    "OpenIEClient",
    "CoreNLPClient",
]
