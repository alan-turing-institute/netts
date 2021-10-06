import os

import pytest


@pytest.fixture(scope="function")
def tmp_path_netspy(tmp_path) -> None:

    expected_dir = tmp_path / "netspy"
    os.environ["netspy_dir"] = str(expected_dir)

    yield tmp_path

    del os.environ["netspy_dir"]
