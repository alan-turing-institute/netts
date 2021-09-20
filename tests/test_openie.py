# pylint: disable=C0114, C0116
import logging
import os
import subprocess

import pytest

from netspy.config import get_settings

LOGGER = logging.getLogger(__name__)


@pytest.mark.ci_only
def test_start_openie() -> None:

    settings = get_settings()

    # Set directory to openie_dir
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

        LOGGER.info("OpenIE stdout: %s", output)
        if return_code is not None:
            raise RuntimeError("OpenIE server start up failed")

        if "Server started at port 6000" in output:
            break
    os.chdir(curwd)
    assert "Server started at port 6000" in output

    # Shut down server
    process.kill()
    process.wait()

    assert os.getcwd() == curwd
