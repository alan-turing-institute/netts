# pylint: disable=C0114, C0116

import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest
import signal
import variables_test as vt
import subprocess
import logging

from netspy import __version__
from netspy.config import get_settings
from netspy.speech_graph import plot_graph, speech_graph


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_stanza() -> None:

    settings = get_settings()

    assert os.getenv("CORENLP_HOME") is not None

def test_start_openie() -> None: 
  
    settings = get_settings() 
  
    # Set directory to openie_dir 
    curwd = os.getcwd() 
    os.chdir(settings.openie_dir) 

    # Start the server 
    # pylint: disable=consider-using-with 
    process = subprocess.Popen( 
        [ 
            "java", 
            "-Xmx20g", 
            "-XX:+UseConcMarkSweepGC", 
            "-jar", 
            "openie-assembly-5.0-SNAPSHOT.jar", 
            "--ignore-errors", 
            "--httpPort", 
            "6000", 
        ], 
        stdout=subprocess.PIPE, 
        universal_newlines=True, 
    ) 
    while True: 
        # This is required to keep mypy happy as can be None 
        if not process.stdout: 
            raise IOError("Process can't write to standard out") 
  
        output = process.stdout.readline() 
        return_code = process.poll() 
  
        logging.info("OpenIE stdout: %s", output) 
        if return_code is not None: 
            raise RuntimeError("OpenIE server start up failed" ,return_code) 
  
        if "Server started at port 6000" in output: 
            break 
  
    assert "Server started at port 6000" in output 
  
    # Shut down server 
    pid = process.pid
    ##os.kill(pid,signal.SIGTERM)
    print(pid)
    #process.kill() 
    os.chdir(curwd) 
    assert os.getcwd() == curwd 



@pytest.mark.parametrize(
    "filename, expected_node_list, expected_edges_list, expected_degree_list",
    [
        (
            "3138838-TAT10.txt",
            vt.expected_node_list1,
            vt.expected_edges1,
            vt.expected_degree1,
        ),
        (
            "3138838-TAT13.txt",
            vt.expected_node_list2,
            vt.expected_edges2,
            vt.expected_degree2,
        ),
        (
            "3138838-TAT30.txt",
            vt.expected_node_list3,
            vt.expected_edges3,
            vt.expected_degree3,
        ),
        (
            "3138849-TAT10.txt",
            vt.expected_node_list4,
            vt.expected_edges4,
            vt.expected_degree4,
        ),
    ],
)
def test_speech_graph(
    filename: str,
    expected_node_list: List[str],
    expected_edges_list: List[Tuple[str, str]],
    expected_degree_list: List[Tuple[str, int]],
) -> None:

    file = Path("demo_data") / filename
    with file.open("r", encoding="utf-8") as f:
        transcript = f.read()

    graph = speech_graph(transcript)
    assert list(graph.nodes()) == expected_node_list
    assert list(graph.edges()) == expected_edges_list
    assert list(graph.degree()) == expected_degree_list

@pytest.mark.parametrize(
    "filename, expected_dict_graph, expected_dict_node, expected_dict_adj, expected_dict_pred, expected_dict_succ",
    [
        (
            "3138838-TAT10.txt",
            vt.expected_dict_graph1,
            vt.expected_dict_node1,
            vt.expected_dict_adj1,
            vt.expected_dict_pred1,
            vt.expected_dict_succ1,
        ),
        (
            "3138838-TAT13.txt",
            vt.expected_dict_graph2,
            vt.expected_dict_node2,
            vt.expected_dict_adj2,
            vt.expected_dict_pred2,
            vt.expected_dict_succ2,
        ),
        (
            "3138838-TAT30.txt",
            vt.expected_dict_graph3,
            vt.expected_dict_node3,
            vt.expected_dict_adj3,
            vt.expected_dict_pred3,
            vt.expected_dict_succ3,
        ),
        (
            "3138849-TAT10.txt",
            vt.expected_dict_graph4,
            vt.expected_dict_node4,
            vt.expected_dict_adj4,
            vt.expected_dict_pred4,
            vt.expected_dict_succ4,
        ),
    ],
)
def test_speech_graph_dict(
    filename: str,
    expected_dict_graph: Dict[Any, Any],
    expected_dict_node: Dict[Any, Any],
    expected_dict_adj: Dict[Any, Any],
    expected_dict_pred: Dict[Any, Any],
    expected_dict_succ: Dict[Any, Any],
) -> None:

    file = Path("demo_data") / filename
    with file.open("r", encoding="utf-8") as f:
        transcript = f.read()

    graph = speech_graph(transcript)
    graph_dict = graph.__dict__
    assert graph_dict.get("graph") == expected_dict_graph
    assert graph_dict.get("_node") == expected_dict_node
    assert graph_dict.get("_adj") == expected_dict_adj
    assert graph_dict.get("_pred") == expected_dict_pred
    assert graph_dict.get("_succ") == expected_dict_succ
