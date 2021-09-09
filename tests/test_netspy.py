# pylint: disable=C0114, C0116

import os
from typing import Any, Dict

from variables_test import (
    expected_degree1,
    expected_degree2,
    expected_degree3,
    expected_degree4,
    expected_dict_adj1,
    expected_dict_adj2,
    expected_dict_adj3,
    expected_dict_adj4,
    expected_dict_graph1,
    expected_dict_graph2,
    expected_dict_graph3,
    expected_dict_graph4,
    expected_dict_node1,
    expected_dict_node2,
    expected_dict_node3,
    expected_dict_node4,
    expected_dict_pred1,
    expected_dict_pred2,
    expected_dict_pred3,
    expected_dict_pred4,
    expected_dict_succ1,
    expected_dict_succ2,
    expected_dict_succ3,
    expected_dict_succ4,
    expected_edges1,
    expected_edges2,
    expected_edges3,
    expected_edges4,
    expected_node_list1,
    expected_node_list2,
    expected_node_list3,
    expected_node_list4,
)

from netspy import __version__
from netspy.config import get_settings
from netspy.speech_graph import plot_graph, speech_graph

import pytest

with open("demo_data/3138838-TAT10.txt", "r", encoding="utf-8") as f:
    transcript = f.read()
graph1 = speech_graph(transcript)
graph1_dict = graph1.__dict__

with open("demo_data/3138838-TAT13.txt", "r", encoding="utf-8") as f:
    transcript = f.read()
graph2 = speech_graph(transcript)
graph2_dict = graph2.__dict__

with open("demo_data/3138838-TAT30.txt", "r", encoding="utf-8") as f:
    transcript = f.read()
graph3 = speech_graph(transcript)
graph3_dict = graph3.__dict__

with open("demo_data/3138849-TAT10.txt", "r", encoding="utf-8") as f:
    transcript = f.read()
graph4 = speech_graph(transcript)
graph4_dict = graph4.__dict__

@pytest.mark.parametrize("go_ip, exp_op",
                        [
                            (list(graph1.nodes()),expected_node_list1),
                            (list(graph1.edges()),expected_edges1),
                            (list(graph1.degree()),expected_degree1),
                            (list(graph2.nodes()),expected_node_list2),
                            (list(graph2.edges()),expected_edges2),
                            (list(graph2.degree()),expected_degree2),
                            (list(graph3.nodes()),expected_node_list3),
                            (list(graph3.edges()),expected_edges3),
                            (list(graph3.degree()),expected_degree3),
                            (list(graph4.nodes()),expected_node_list4),
                            (list(graph4.edges()),expected_edges4),
                            (list(graph4.degree()),expected_degree4)
                            #(graph1_dict.get("graph") == expected_dict_graph1)
                        ]
                        )
def test_lists(go_ip, exp_op):
    assert go_ip == exp_op

@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_stanza() -> None:

    settings = get_settings()

    assert os.getenv("CORENLP_HOME") is not None

def test_speech_graph() -> None:
    assert graph1_dict.get("graph") == expected_dict_graph1
    assert graph1_dict.get("_node") == expected_dict_node1
    assert graph1_dict.get("_adj") == expected_dict_adj1
    assert graph1_dict.get("_pred") == expected_dict_pred1
    assert graph1_dict.get("_succ") == expected_dict_succ1

    assert graph2_dict.get("graph") == expected_dict_graph2
    assert graph2_dict.get("_node") == expected_dict_node2
    assert graph2_dict.get("_adj") == expected_dict_adj2
    assert graph2_dict.get("_pred") == expected_dict_pred2
    assert graph2_dict.get("_succ") == expected_dict_succ2

    assert graph3_dict.get("graph") == expected_dict_graph3
    assert graph3_dict.get("_node") == expected_dict_node3
    assert graph3_dict.get("_adj") == expected_dict_adj3
    assert graph3_dict.get("_pred") == expected_dict_pred3
    assert graph3_dict.get("_succ") == expected_dict_succ3

    assert graph4_dict.get("graph") == expected_dict_graph4
    assert graph4_dict.get("_node") == expected_dict_node4
    assert graph4_dict.get("_adj") == expected_dict_adj4
    assert graph4_dict.get("_pred") == expected_dict_pred4
    assert graph4_dict.get("_succ") == expected_dict_succ4
