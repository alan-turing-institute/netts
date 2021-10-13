import pytest
from devtools import debug

from netspy.clients import CoreNLPClient, OpenIEClient


def test_corenlp_client() -> None:
    client = CoreNLPClient(port=5555)

    debug(client.port)

    assert client.port == 5555


@pytest.mark.skip("Takes too long to run every time.")
def test_openie_client() -> None:
    client = OpenIEClient()

    client.connect()

    text = (
        "It seems to be in the middle of the night ; "
        + "I think because the lightbulb is working "
    )

    extracted = client.extract(text)

    client.close()

    # This isn't very meaningful, it's only to guard against regressions
    assert len(extracted) == 3
