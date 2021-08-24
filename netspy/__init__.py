"""Netspy. A package for constructing semantic speech networks from
speech transcripts.
"""
__version__ = "0.1.0"

from netspy.speech_graph import speech_graph
from netspy.types import MultiDiGraph

__all__ = ["speech_graph", "MultiDiGraph"]
