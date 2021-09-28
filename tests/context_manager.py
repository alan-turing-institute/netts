import logging
import os
import subprocess
import contextlib
import socket
import atexit
from types import TracebackType
from typing import Optional, Type

from netspy.config import get_settings
import json
import requests

class ManageOpenIE:
    settings = get_settings()
    openiepth = settings.openie_dir

    def __init__(self) -> None:
        settings = get_settings()
        self.openiepth = settings.openie_dir
        self.process=None
        self.host='localhost'
        self.port = 6000
        # Check if the port is open
        self.check_port()
        atexit.register(self.atexit_kill)

    def check_port(self):
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind((self.host, self.port))
            except socket.error:
                raise FailedException("Error: unable to start openIE server on port %d "
                                 "(possibly something is already running there)" % self.port)

    def connect(self):
        # Get the initial working directory
        iwd = os.getcwd()

        # Change directory to the openie directory
        os.chdir(self.openiepth)

        # Start the server - here we could have more options for users to decide what they want?
        self.process = subprocess.Popen(  # pylint: disable=consider-using-with
            [
                "java",
                "-Xmx20g",
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
            # This is required to keep mypy happy as can be None
            if not self.process.stdout:
                raise IOError("Process can't write to standard out")

            output = self.process.stdout.readline()
            return_code = self.process.poll()

            logging.info("OpenIE stdout: %s", output)
            if return_code is not None:
                raise RuntimeError("OpenIE server start up failed", return_code)

            if "Server started at port "+str(self.port) in output:
                break

        assert "Server started at port "+str(self.port) in output

        # Change to the initial working directory
        os.chdir(iwd)

    def __enter__(self) -> None:
        self.connect()
        return self


    def extract(self, sentence: str, properties: dict):
        assert isinstance(sentence, str) # Ensure a string is passed
        if properties is None:
            properties = {}
        else:
            assert isinstance(properties, dict) # Ensure the properties is a dictionary

        data_payload = sentence.encode('utf-8') # Set the encoding of the text being sent

        # Post: Send instructions
        instruction='http://localhost:'+str(self.port)+'/getExtraction'
        payload={'properties': str(properties)}
        header_payload={'Connection': 'close'}
        extraction_request = requests.post(
                instruction,
                params=payload,
                data=data_payload,
                headers=header_payload)#{'Connection': 'close'})

        return json.loads(extraction_request.text)

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[Type[BaseException]],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    def close(self):
        if self.process and not self.process.poll():
            # Close the server
            self.process.kill()
            self.process.wait()

    def atexit_kill(self):
        """
        If python is forced to close, the process will be terminated
        """
        if self.process and self.process.poll() is None:
            self.process.terminate()

class FailedException(Exception):
    """
    Don't try and force it to run on the speicfied port
    """

sentence_one='There are two ... There is a young girl and who and seems to be maid , sitting on a couch .'
sentence_two='The little girl seems to be upset , she is looking away and she looks very dismissive .'

props={}
openie=ManageOpenIE()
openie.connect()
op=openie.extract(sentence_one, props)
print(op)
op=openie.extract(sentence_two, props)
print(op)
openie.close()
