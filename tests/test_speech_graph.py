# pylint: disable=C0114, C0116, R0913, redefined-outer-name, W0613
import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

import pytest

import netspy
from netspy.speech_graph import SpeechGraph


@dataclass
class Clients:
    openie_client: netspy.OpenIEClient
    corenlp_client: netspy.CoreNLPClient


def test_stanza() -> None:

    settings = netspy.get_settings()
    assert settings.core_nlp_dir == Path(
        os.getenv("CORENLP_HOME", "this_dir_doesn't_exist")
    )


@pytest.fixture(scope="module")
def module_clients() -> Generator[Clients, None, None]:

    # This has the side effect of setting the CORENLP_HOME environment variable.
    settings = netspy.get_settings()

    clients = Clients(
        openie_client=netspy.OpenIEClient(
            port=settings.netspy_config.server.openie.port,
            # quiet=True
        ),
        corenlp_client=netspy.CoreNLPClient(
            properties={
                "annotators": "tokenize,ssplit,pos,lemma,ner,parse,depparse,coref,openie"
            },
            port=settings.netspy_config.server.corenlp.port,
            # be_quite=True
        ),
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
        ("3138838-TAT13.txt", "tests/test_data/3138838-TAT13.pickle"),
        ("3138838-TAT30.txt", "tests/test_data/3138838-TAT30.pickle"),
        ("3138849-TAT10.txt", "tests/test_data/3138849-TAT10.pickle"),
    ],
)
def test_speech_pickle(
    module_clients: Clients, filename: str, output_pickle: str
) -> None:
    def _load_graph(path: str) -> netspy.MultiDiGraph:
        return pickle.loads(Path(path).read_bytes())

    file = Path("demo_data") / filename
    with file.open("r", encoding="utf-8") as f:
        transcript = f.read()

    graph = SpeechGraph(transcript).process(
        openie_client=module_clients.openie_client,
        corenlp_client=module_clients.corenlp_client,
    )

    assert vars(_load_graph(output_pickle)) == vars(graph)
