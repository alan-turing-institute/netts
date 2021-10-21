# pylint: disable=C0114, C0116, R0913, redefined-outer-name, W0613
import os
import pickle
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

import pytest

import netspy
from netspy.speech_graph import SpeechGraph


@dataclass
class Clients:
    openie_client: netspy.MyOpenIEClient
    corenlp_client: netspy.MyCoreNLPClient


def test_stanza() -> None:

    local_version = str(netspy.config.NETSPY_DIR / "stanza_corenlp")
    github_actions_version = str(Path(".dependencies") / "stanza_corenlp")

    _ = netspy.get_settings()
    assert os.getenv("CORENLP_HOME") in [local_version, github_actions_version]


@pytest.fixture(scope="module")
def module_clients() -> Generator[Any, Any, Any]:

    settings = netspy.get_settings()

    clients = Clients(
        openie_client=netspy.MyOpenIEClient(
            quiet=True, port=settings.netspy_config.server.openie.port
        ),
        corenlp_client=netspy.MyCoreNLPClient(port=9090),
    )

    clients.openie_client.connect()
    clients.corenlp_client.start()

    yield clients

    clients.openie_client.close()
    clients.corenlp_client.stop()


@pytest.mark.parametrize(
    "filename,output_pickle",
    [
        ("3138838-TAT10.txt", "tests/test_data/3138838-TAT10.pickle"),
    ],
)
def test_speech_pickle(filename: str, output_pickle: str) -> None:
    def _load_graph(path: str) -> netspy.MultiDiGraph:
        return pickle.loads(Path(path).read_bytes())

    print(f"os.getcwd() {os.getcwd()}")

    file = Path("demo_data") / filename
    with file.open("r", encoding="utf-8") as f:
        transcript = f.read()

    settings = netspy.get_settings()
    with netspy.MyOpenIEClient(
        quiet=False, port=settings.netspy_config.server.openie.port
    ) as openie_client:
        corenlp_client = netspy.MyCoreNLPClient(port=9090)
        corenlp_client.start()

        graph = SpeechGraph(transcript).process(
            openie_client=openie_client,
            corenlp_client=corenlp_client,
        )

    assert vars(_load_graph(output_pickle)) == vars(graph)

    # Let the openie server shut down
    time.sleep(10)
