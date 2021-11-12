from __future__ import annotations

import atexit
import contextlib
import logging
import os
import socket
import subprocess
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, Optional, Type

import requests
import stanza.server

from netts.config import Settings


class CoreNLPClient(stanza.server.CoreNLPClient):  # type: ignore
    def __init__(self, *args: Any, port: int = 8089, **kwargs: Any) -> None:
        host = "http://localhost"
        endpoint = f"{host}:{port}"

        super().__init__(endpoint=endpoint, *args, **kwargs)


class OpenIEClient:
    def __init__(
        self,
        host: str = "http://localhost",
        port: int = 8099,
        openie_dir: Path = Settings().openie_dir,
        quiet: bool = False,
        memory: int = 20,
    ) -> None:

        self.host = host
        self.port = port
        self.openie_dir = openie_dir

        # Can't type: https://github.com/python/typeshed/issues/4948
        self.process: Any = None
        self.quiet = quiet
        self.memory = memory

        # Check if the port is open
        self.check_port()
        atexit.register(self.atexit_kill)

    def check_port(self) -> None:

        with contextlib.closing(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ) as sock:
            try:
                sock.bind(("localhost", self.port))
            except socket.error:
                raise FailedException(
                    f"Error: unable to start openIE server on port {self.port}"
                    "(possibly something is already running there)"
                )

    def connect(self) -> None:

        iwd = os.getcwd()
        os.chdir(self.openie_dir)

        self.process = subprocess.Popen(  # pylint: disable=consider-using-with
            [
                "java",
                f"-Xmx{self.memory}g",
                "-XX:+UseConcMarkSweepGC",
                "-jar",
                "openie-assembly-5.0-SNAPSHOT.jar",
                "--ignore-errors",
                "--httpPort",
                str(self.port),
            ],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        while True:
            if not self.process.stdout:
                raise IOError("Process can't write to standard out")
            self.process.stdout.flush()
            output = self.process.stdout.readline()
            return_code = self.process.poll()

            if not self.quiet:
                logging.info("OpenIE stdout: %s", output)

            if return_code:
                raise RuntimeError("OpenIE server start up failed", return_code)

            if "Server started at port " + str(self.port) in output:
                break

        os.chdir(iwd)

    def __enter__(self) -> OpenIEClient:
        self.connect()
        return self

    def extract(
        self, sentence: str, properties: Optional[Dict[str, str]] = None
    ) -> Any:

        if not properties:
            properties = {}

        data_payload = sentence.encode("utf-8")

        instruction = f"{self.host}:{self.port}/getExtraction"
        payload = {"properties": str(properties)}
        header_payload = {"Connection": "close"}
        extraction_request = requests.post(
            instruction, params=payload, data=data_payload, headers=header_payload
        )

        return extraction_request.json()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[Type[BaseException]],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    def close(self) -> None:
        if self.process and not self.process.poll():
            # Close the server
            self.process.kill()
            self.process.wait()
            self.process = None

    def atexit_kill(self) -> None:
        if self.process and not self.process.poll():
            self.process.terminate()


class FailedException(Exception):
    pass
