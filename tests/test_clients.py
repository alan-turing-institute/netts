from devtools import debug

from netspy.clients import MyCoreNLPClient


def test_corenlp_client() -> None:
    client = MyCoreNLPClient(port=5555)

    debug(client.port)

    assert client.port == 5555
