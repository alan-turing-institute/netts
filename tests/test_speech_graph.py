# pylint: disable=C0114, C0116, R0913, redefined-outer-name, W0613
import os
import pickle

# import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

import pytest

import netspy
from netspy.clients import OpenIEClient
from netspy.config import Settings
from netspy.speech_graph import SpeechGraph


@dataclass
class Clients:
    openie_client: netspy.OpenIEClient
    corenlp_client: netspy.CoreNLPClient


def test_stanza() -> None:

    local_version = str(netspy.config.NETSPY_DIR / "stanza_corenlp")
    github_actions_version = str(Path(".dependencies") / "stanza_corenlp")

    _ = netspy.get_settings()
    assert os.getenv("CORENLP_HOME") in [local_version, github_actions_version]


@pytest.fixture(scope="module")
def module_clients() -> Generator[Any, Any, Any]:

    _ = netspy.get_settings()

    clients = Clients(
        openie_client=netspy.OpenIEClient(quiet=True),
        corenlp_client=netspy.CoreNLPClient(be_quite=True),
    )

    clients.openie_client.connect()
    clients.corenlp_client.start()

    yield clients

    clients.openie_client.close()
    clients.corenlp_client.stop()


def test_speech_pickle() -> None:
    def _load_graph(path: str) -> netspy.MultiDiGraph:
        return pickle.loads(Path(path).read_bytes())

    filename = "3138838-TAT10.txt"
    file = Path("demo_data") / filename
    with file.open("r", encoding="utf-8") as f:
        transcript = f.read()

    settings = Settings()
    with OpenIEClient(
        quiet=True, port=settings.netspy_config.server.openie.port
    ) as client:

        graph = SpeechGraph(transcript).process(openie_client=client)

        assert vars(_load_graph("tests/test_data/3138838-TAT10.pickle")) == vars(graph)

    # Let the openie server shut down
    # time.sleep(5)
