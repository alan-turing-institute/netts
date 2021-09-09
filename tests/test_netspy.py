# pylint: disable=C0114, C0116

import os
from typing import Any, Dict
from pathlib import Path
import pytest
import variables_test as vt

from netspy import __version__
from netspy.config import get_settings
from netspy.speech_graph import plot_graph, speech_graph


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_stanza() -> None:

    settings = get_settings()

    assert os.getenv("CORENLP_HOME") is not None


@pytest.mark.parametrize(
    "file_name, expected_node_list, expected_edge_list, expected_degree",
    [
        ("3138838-TAT10.txt", vt.expected_node_list1, vt.expected_edges1, vt.expected_degree1),
        ("3138838-TAT13.txt", vt.expected_node_list2, vt.expected_edges2, vt.expected_degree2),
        ("3138849-TAT10.txt", vt.expected_node_list3, vt.expected_edges3, vt.expected_degree3),
    ],
)
def test_speech_graph(
    file_name, expected_node_list, expected_edge_list, expected_degree
) -> None:

    file = Path("demo_data") / file_name
    with file.open("r", encoding="utf-8") as f:
        transcript = f.read()

    graph = speech_graph(transcript)

    assert list(graph.nodes()) == expected_node_list
    assert list(graph.edges()) == expected_edge_list
    assert list(graph.degree()) == expected_degree

    # graph_dict = graph.__dict__

    # assert graph_dict.get("graph") == expected_dict_graph1
    # assert graph_dict.get("_node") == expected_dict_node1
    # assert graph_dict.get("_adj") == expected_dict_adj1
    # assert graph_dict.get("_pred") == expected_dict_pred1
    # assert graph_dict.get("_succ") == expected_dict_succ1

