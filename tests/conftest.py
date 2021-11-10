import os
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(scope="function")
def tmp_path_netts(tmp_path: Path) -> Generator[Path, None, None]:

    expected_dir = tmp_path / "netts"
    os.environ["netts_dir"] = str(expected_dir)

    yield tmp_path

    del os.environ["netts_dir"]
