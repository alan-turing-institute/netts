import datetime
import logging
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import typer
from matplotlib import pyplot as plt
from stanza.server import CoreNLPClient
from typer import colors

import netspy
from netspy import SpeechGraphFile
from netspy.config import get_settings

app = typer.Typer()
setting = get_settings()


# pylint: disable=C0103
@dataclass
class Color:
    text: str
    fg: Optional[str] = None
    bg: Optional[str] = None
    bold: bool = False
    underline: bool = False
    blink: bool = False

    def dict(self) -> Dict[Any, Any]:
        return self.__dict__


# pylint: disable=R1732
def start_openie() -> Any:
    settings = get_settings()
    curwd = os.getcwd()
    os.chdir(settings.openie_dir)
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

    return process


@app.command()
def install(
    directory: Optional[Path] = typer.Option(
        None, help="Directory to install netspy dependencies to"
    )
) -> None:
    """Install all tool dependencies and langauge models"""

    netspy.install_dependencies(directory)


@app.command()
def home() -> None:
    """Show netspy's dependency directory"""
    typer.echo(f"Netspy directory: {setting.netspy_dir}")


def cprint(*args: Union[Color, str, List[Union[Color, str]]]) -> None:

    all_text = args
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = typer.style(f"{time} Netspy") + ": "

    for text in all_text:
        if isinstance(text, str):
            output += text
        elif isinstance(text, Color):
            output += typer.style(**text.dict())
        else:
            raise TypeError("Must be str of Color")

    typer.echo(output)


# pylint: disable=R0913, W0613
@app.command()
def run(
    input_path: Path,
    output_dir: Path,
    pattern: str = typer.Option(
        "*.txt", "--pattern", help="glob pattern to select files in PATH"
    ),
    config: Optional[Path] = typer.Option(
        None, "--config", help="a netspy configuration file"
    ),
    force: bool = typer.Option(
        False, "--force", help="process even if output already exists"
    ),
    figure: bool = typer.Option(True, "--figure", help="create figure of network"),
    fig_format: str = "png",
) -> None:
    """Process transcript(s) in INPUT_DIR
    and pickle graph objects to OUTPUT_DIR.
    Optionally save a figure of the graph network"""

    if not input_path.exists():
        cprint(
            Color(
                f"INPUT_PATH: '{input_path}' does not exist. Check path",
                fg=typer.colors.RED,
                bold=True,
            )
        )
        raise typer.Abort

    # Get all files
    all_transcript_files = (
        [
            SpeechGraphFile(i, output_dir, load_if_exists=not force)
            for i in input_path.glob(pattern)
        ]
        if input_path.is_dir()
        else [SpeechGraphFile(input_path, output_dir, load_if_exists=not force)]
    )

    n_missing = len([i for i in all_transcript_files if i.missing])
    n_transcripts = len(all_transcript_files)

    cprint(
        "Found ",
        Color(f"{n_transcripts} ", fg=colors.GREEN),
        "transcripts. Unprocessed: ",
        Color(f"{n_missing}", fg=colors.BLUE),
    )

    # Only start the servers if there are files to process
    if force or n_missing > 0:

        openie = start_openie()
        corenlp_client = CoreNLPClient(
            properties={
                "annotators": "tokenize,ssplit,pos,lemma,parse,depparse,coref,openie"
            },
            be_quiet=True,
        )
        corenlp_client.start()

        for transcript_file in all_transcript_files:
            if transcript_file.missing or force:
                transcript_file.process(corenlp_client)
            transcript_file.dump()

        openie.kill()
        openie.wait()
        corenlp_client.stop()

    # Save figures
    if figure:
        for transcript_file in all_transcript_files:

            plot_file = transcript_file.output_graph_file(fig_format)

            if not plot_file.exists() or force:

                cprint(f"Creating figure: {plot_file}")
                transcript_file.plot_graph()
                plt.savefig(transcript_file.output_graph_file(fig_format))


if __name__ == "__main__":
    app()
