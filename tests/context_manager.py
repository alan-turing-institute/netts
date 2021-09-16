from pathlib import Path
import subprocess
import logging
import os 
from typing_extensions import runtime
from netspy.config import get_settings
from netspy.speech_graph import speech_graph


class ManageOpenIE():
    settings = get_settings()
    openiepth=settings.openie_dir

    def __init__(self, datapath:Path) -> None:
        self.datapath = datapath
        
        # Get the openie path (again) - I think I should be able to make this a class variable/param?
        settings = get_settings()
        self.openiepth=settings.openie_dir

        # Get the initial working directory
        self.iwd = os.getcwd()

        # Change directory to the openie directory
        os.chdir(self.openiepth)
        
        # Start the server - here we could have more options for users to decide what they want?
        self.process = subprocess.Popen(
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


    def __enter__(self) -> None:
        while True:
            # This is required to keep mypy happy as can be None
            if not self.process.stdout:
                raise IOError("Process can't write to standard out")

            output = self.process.stdout.readline()
            return_code = self.process.poll()

            logging.info("OpenIE stdout: %s", output)
            if return_code is not None:
                raise RuntimeError("OpenIE server start up failed", return_code)

            if "Server started at port 6000" in output:
                break

        assert "Server started at port 6000" in output

        # Change to the data directory for the work
        os.chdir(self.datapath)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # To close change back to the openie directory
        os.chdir(self.openiepth)
        # Close the server
        self.process.kill()
        self.process.wait()
        # Change back to initial working directory
        os.chdir(self.iwd)
        assert os.getcwd() == self.iwd


current=os.getcwd()
upper=os.path.dirname(current)
datapath=upper + "/demo_data"
print(upper, datapath)

# datapath=os.getcwd()+'/tmp'
with ManageOpenIE(datapath):
    with open("3138838-TAT10.txt" , "r" , encoding="utf-8") as f:
        transcript=f.read()
    graph = speech_graph(transcript)
print(graph.__dict__)

with ManageOpenIE(datapath):
    with open("3138849-TAT10.txt", "r",encoding="utf-8") as f:
        transcript=f.read()
    graph2 = speech_graph(transcript)
print(graph2.__dict__)