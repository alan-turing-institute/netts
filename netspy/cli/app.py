import datetime
from dataclasses import dataclass
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import typer
from matplotlib import pyplot as plt
from typer import colors

import netspy
from netspy import SpeechGraphFile
from netspy.clients import CoreNLPClient, OpenIEClient
from netspy.config import Settings, get_settings

app = typer.Typer()


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


@app.command()
def install() -> None:
    """Install all tool dependencies and langauge models"""

    netspy.install_dependencies()


@app.command()
def home() -> None:
    """Show netspy's dependency directory"""
    typer.echo(f"Netspy directory: {get_settings().netspy_dir}")


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
    config_file: Optional[Path] = typer.Option(
        None, "--config", help="a netspy configuration file"
    ),
    force: bool = typer.Option(
        False, "--force", help="process even if output already exists"
    ),
    figure: bool = typer.Option(True, help="create figure of network"),
    fig_format: str = "png",
) -> None:
    """Process transcript(s) in INPUT_DIR
    and pickle graph objects to OUTPUT_DIR.
    Optionally save a figure of the graph network"""

    if config_file:
        settings = Settings(config_file=config_file)
    else:
        settings = Settings()

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

        corenlp_client = CoreNLPClient(
            properties={
                "annotators": "tokenize,ssplit,pos,lemma,parse,depparse,coref,openie"
            },
            be_quiet=True,
            port=settings.netspy_config.server.corenlp.port,
        )

        # Doesn't block
        corenlp_client.start()

        cprint(Color(f"Stanza PID: {corenlp_client.get_pid()}", fg="red"))

        openie_client = OpenIEClient(
            quiet=True, port=settings.netspy_config.server.openie.port
        )
        # Blocks
        openie_client.connect()

        for transcript_file in all_transcript_files:
            if transcript_file.missing or force:
                transcript_file.process(corenlp_client, openie_client)
            transcript_file.dump()

        corenlp_client.stop()
        openie_client.close()

    # Save figures
    if figure:
        for transcript_file in all_transcript_files:

            plot_file = transcript_file.output_graph_file(fig_format)

            if not plot_file.exists() or force:

                cprint(f"Creating figure: {plot_file}")
                transcript_file.plot_graph()
                plt.savefig(transcript_file.output_graph_file(fig_format))


@app.command()
def config() -> None:
    """Create a defauly configuration file"""

    typer.echo(netspy.Config.default())


@app.command()
def config_verify(config_file: Path) -> None:
    """Verify a configuration file"""

    # This will raise an exception if config is invalid (i.e missing values or incorrect syntax)
    netspy.Config.load(config_file)

    typer.echo("Configuration is valid")


if __name__ == "__main__":
    app()
