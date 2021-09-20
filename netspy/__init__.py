"""Netspy. A package for constructing semantic speech networks from
speech transcripts.
"""

from networkx.classes.multidigraph import MultiDiGraph

from netspy.install_models import install_dependencies
from netspy.speech_graph import speech_graph, plot_graph, pickle_graph

__version__ = "0.1.0"

__all__ = ["install_dependencies", "speech_graph", "plot_graph", "MultiDiGraph", "pickle_graph"]
