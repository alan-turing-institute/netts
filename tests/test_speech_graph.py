# pylint: disable=C0114, C0116, R0913, redefined-outer-name, W0613

import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple

import pytest
import netspy
import variables_test as vt

from netspy import __version__
from netspy.config import get_settings
from netspy.speech_graph import SpeechGraphFile, SpeechGraph
import pickle


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_stanza() -> None:
    assert os.getenv("CORENLP_HOME") is not None


@pytest.fixture(scope="session")
def openie_start() -> Generator[None, None, None]:

    settings = get_settings()
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
            raise RuntimeError("OpenIE server start up failed", return_code)

        if "Server started at port 6000" in output:
            break

    os.chdir(curwd)
    yield

    # Shut down server
    process.kill()
    process.wait()

@pytest.mark.parametrize(
    "filename,output_pickle",
    [
        ("3138838-TAT10.txt", "tests/test_data/3138838-TAT10.pickle"),
        ("3138838-TAT13.txt", "tests/test_data/3138838-TAT13.pickle"),
        (
            "3138838-TAT30.txt",
            "tests/test_data/3138838-TAT30.pickle",
        ),
        (
            "3138849-TAT10.txt",
            "tests/test_data/3138849-TAT10.pickle",
        ),
    ],
)
def test_speech_pickle(openie_start: Any, filename, output_pickle):

    def _load_graph(path: str) -> netspy.MultiDiGraph:
        return pickle.loads(Path(path).read_bytes())

    file = Path("demo_data") / filename
    with file.open("r", encoding="utf-8") as f:
        transcript = f.read()

    graph = SpeechGraph(transcript).process()
    
    assert vars(_load_graph(output_pickle)) == vars(graph)