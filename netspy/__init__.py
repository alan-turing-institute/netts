"""Netspy. A package for constructing semantic speech networks from
speech transcripts.
"""

from netspy.install_models import install_dependencies

__version__ = "0.1.0"

from netspy.speech_graph import speech_graph
from netspy.types import MultiDiGraph

__all__ = ["install_dependencies","speech_graph", "MultiDiGraph"]
