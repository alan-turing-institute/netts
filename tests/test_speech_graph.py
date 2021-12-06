# pylint: disable=C0114, C0116, R0913, redefined-outer-name, W0613
import logging
import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

import networkx as nx  # type: ignore [import]
import numpy as np
import pytest
from matplotlib import image
from matplotlib import pyplot as plt

import netts
from netts.speech_graph import SpeechGraph

# from pytest_mock import MockerFixture


def test_stanza() -> None:

    settings = netts.get_settings()
    assert settings.core_nlp_dir == Path(
        os.getenv("CORENLP_HOME", "this_dir_doesn't_exist")
    )


@dataclass
class Clients:
    openie_client: netts.OpenIEClient
    corenlp_client: netts.CoreNLPClient


class OnDemandNLPClient(netts.CoreNLPClient):
    """A CoreNLPClient that starts on demand.

    When needed, this client stops the OpenIE server, before starting itself."""

    openie_client: "OnDemandOpenIEClient"

    def annotate(self, *args, **kwargs):  # type: ignore
        logging.debug("in annotate")

        # For memory reasons, we need to stop the other server
        # before starting this one.
        if self.openie_client.process:
            self.openie_client.close()
            logging.debug("closed")

        if not self.server:
            self.start()
            logging.debug("started")

        result = super().annotate(*args, **kwargs)
        logging.debug("annotated")

        return result


class OnDemandOpenIEClient(netts.OpenIEClient):
    """An OpenIEClient that starts on demand.

    When needed, this client stops the CoreNLP server, before starting itself."""

    corenlp_client: OnDemandNLPClient

    def extract(self, *args, **kwargs):  # type: ignore
        logging.debug("in extract")

        # For memory reasons, we need to stop the other server
        # before starting this one.
        if self.corenlp_client.server:
            self.corenlp_client.stop()
            logging.debug("stopped")

        if not self.process:
            self.connect()
            logging.debug("connected")

        result = super().extract(*args, **kwargs)
        logging.debug("extracted")

        return result


@pytest.fixture(scope="module")
def module_clients() -> Generator[Clients, None, None]:

    # This has the side effect of setting the CORENLP_HOME environment variable.
    settings = netts.get_settings()

    openie_port = settings.netts_config.server.openie.port
    corenlp_port = settings.netts_config.server.corenlp.port

    openie_client: netts.OpenIEClient
    corenlp_client: netts.CoreNLPClient

    # https://docs.github.com/en/actions/learn-github-actions/environment-variables#default-environment-variables
    if os.getenv("GITHUB_ACTIONS") == "true":

        running_on_github = True
        logging.warning("Using special clients to conserve memory on GitHub hosted VM.")

        openie_client = OnDemandOpenIEClient(port=openie_port)
        corenlp_client = OnDemandNLPClient(
            port=corenlp_port,
            properties={
                "annotators": "tokenize,ssplit,pos,lemma,parse,depparse,coref,openie",
                "timeout": "50000"
            },
        )

        # The servers need to know about each other so that they can stop each other.
        openie_client.corenlp_client = corenlp_client
        corenlp_client.openie_client = openie_client
    else:
        running_on_github = False
        logging.warning(
            "Using normal clients. Set GITHUB_ACTIONS='true'"
            "to use GitHub style clients."
        )
        openie_client = netts.OpenIEClient(port=openie_port)
        corenlp_client = netts.CoreNLPClient(
            port=corenlp_port,
            properties={
                "annotators": "tokenize,ssplit,pos,lemma,parse,depparse,coref,openie"
            },
        )
        openie_client.connect()
        corenlp_client.start()

    yield Clients(openie_client=openie_client, corenlp_client=corenlp_client)

    if not running_on_github:
        logging.debug("closing and stopping")
        openie_client.close()
        corenlp_client.stop()


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
    """Check that our test data always results in the same speech graphs."""

    def _load_graph(path: str) -> netts.MultiDiGraph:
        return pickle.loads(Path(path).read_bytes())

    file = Path("demo_data") / filename
    with file.open("r", encoding="utf-8") as f:
        transcript = f.read()

    settings = netts.get_settings()

    graph = SpeechGraph(transcript).process(
        openie_client=module_clients.openie_client,
        corenlp_client=module_clients.corenlp_client,
        preprocess_config=settings.netts_config.preprocess,
    )

    assert vars(_load_graph(output_pickle)) == vars(graph)


def test_plot_graph() -> None:

    speech_graph = SpeechGraph("")

    multi_di_graph = nx.MultiDiGraph()
    multi_di_graph.add_edge(1, 2, relation="one->two")
    multi_di_graph.add_edge(2, 3, relation="two->three")
    multi_di_graph.add_edge(3, 1, relation="three->one")

    speech_graph.graph = multi_di_graph

    # Note: We had to hard-code the RNG seed in plot_graph
    speech_graph.plot_graph()

    # Save it somewhere easy to access in case we want to overwrite the
    # expected_test_plot_graph.png with it
    plt.savefig("tests/test_data/actual_test_plot_graph.png")

    actual = image.imread("tests/test_data/actual_test_plot_graph.png")
    expected = image.imread("tests/test_data/expected_test_plot_graph.png")

    mean_squared_error = np.square(np.subtract(actual, expected)).mean()

    # To allow for minor differences, such as node_side increasing by 10.
    # Value found experimentally.
    assert mean_squared_error <= 0.00001


# @pytest.mark.parametrize(
#     "filename,output_pickle",
#     [
#         ("3138838-TAT10.txt", "tests/test_data/3138838-TAT10.pickle"),
#         ("3138838-TAT13.txt", "tests/test_data/3138838-TAT13.pickle"),
#         ("3138838-TAT30.txt", "tests/test_data/3138838-TAT30.pickle"),
#         ("3138849-TAT10.txt", "tests/test_data/3138849-TAT10.pickle"),
#     ],
# )
# def test_mock_speech_pickle(filename: str, output_pickle: str
# ) -> None:

#     def _load_graph(path: str) -> netts.MultiDiGraph:
#         return pickle.loads(Path(path).read_bytes())

#     class MockOpenIEClient:
#         calls = []
#         responses = {}
#         def extract(self, text):
#             calls.append(text)


#     class MockCoreNLPClient:
#         calls = []
#         responses = {}
#         def annotate(self, text):
#             calls.append(text)

#     with file.open("r", encoding="utf-8") as f:
#         transcript = f.read()

#     graph = SpeechGraph(transcript).process(
#         openie_client=MockOpenIEClient(),
#         corenlp_client=MockCoreNLPClient(),
#     )

#     assert vars(_load_graph(output_pickle)) == vars(graph)
