"""Netts. A package for constructing semantic speech networks from
speech transcripts.
"""
from networkx.classes.multidigraph import MultiDiGraph

from netts import preprocess  # noqa: F401 # pylint: disable=E0012,F401
from netts.clients import CoreNLPClient, OpenIEClient
from netts.config import get_settings
from netts.config_file import Config
from netts.install_models import install_dependencies
from netts.speech_graph import SpeechGraph, SpeechGraphFile

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
