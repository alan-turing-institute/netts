"""
netts: Toolbox for constructing semantic speech networks from speech transcripts.

Copyright (C) 2021 Caroline Nettekoven(1), Sarah Morgan(1,2), Oscar Terence Giles(2), Helen Duncan(2), Iain Stenson(2)
(1) University of Cambridge, (2) The Alan Turing Institute

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from networkx.classes.multidigraph import MultiDiGraph

from netts import preprocess  # noqa: F401 # pylint: disable=E0012,F401
from netts.clients import CoreNLPClient, OpenIEClient
from netts.config import get_settings
from netts.config_file import Config
from netts.install_models import install_dependencies
from netts.speech_graph import SpeechGraph, SpeechGraphFile, pickle_graph
from netts.version import __version__

__all__ = [
    "install_dependencies",
    "preprocess",
    "SpeechGraph",
    "pickle_graph",
    "SpeechGraphFile",
    "Config",
    "get_settings",
    "MultiDiGraph",
    "OpenIEClient",
    "CoreNLPClient",
    "__version__",
]
