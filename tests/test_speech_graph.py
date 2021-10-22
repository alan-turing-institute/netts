# pylint: disable=C0114, C0116, R0913, redefined-outer-name, W0613
import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

import pytest

import netspy
from netspy.clients import OpenIEClient
from netspy.config import Settings
from netspy.speech_graph import SpeechGraph, pro


@dataclass
class Clients:
    openie_client: netspy.OpenIEClient
    corenlp_client: netspy.CoreNLPClient


@pytest.fixture(scope="module")
def module_clients() -> Generator[Any, Any, Any]:

    settings = Settings()

    clients = Clients(
        openie_client=netspy.OpenIEClient(
            port=settings.netspy_config.server.openie.port
        ),
        corenlp_client=netspy.CoreNLPClient(be_quite=True),
    )

    clients.openie_client.connect()
    clients.corenlp_client.start()

    yield clients

    clients.openie_client.close()
    clients.corenlp_client.stop()


def test_speech_pickle(module_clients) -> None:

    # settings = Settings()
    # with OpenIEClient(
    #     quiet=True, port=settings.netspy_config.server.openie.port
    # ) as client:

    pro(openie_client=module_clients.openie_client)

    # Let the openie server shut down
    # time.sleep(5)
