import datetime
import logging
from rich.logging import RichHandler
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import typer
from matplotlib import pyplot as plt

import netts
from netts import SpeechGraphFile
from netts.clients import CoreNLPClient, OpenIEClient
from netts.config import Settings, get_settings
from netts.logger import logger, stanza_logger

import threading, itertools, sys, time

# Animation so the user knows that something is happening...
done = False
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rRunning transcripts... ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')


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

    netts.install_dependencies()


@app.command()
def home() -> None:
    """Show netts's dependency directory"""
    typer.echo(f"Netts directory: {get_settings().netts_dir}")


def cprint(*args: Union[Color, str, List[Union[Color, str]]]) -> None:

    all_text = args
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = typer.style(f"{time} Netts") + ": "

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
        None, "--config", help="a netts configuration file"
    ),
    force: bool = typer.Option(
        False, "--force", help="process even if output already exists"
    ),
    figure: bool = typer.Option(True, help="create figure of network"),
    fig_format: str = "png",
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Set the logging level to INFO"
    ),
    very_verbose: bool = typer.Option(
        False, "--very-verbose", "-vv", help="Set the logging level to DEBUG"
    ),
) -> None:
    """Process transcript(s) in INPUT_DIR
    and pickle graph objects to OUTPUT_DIR.
    Optionally save a figure of the graph network"""
    
    logger.info(f"For logging information, please check {Path(__file__).resolve().parent.parent.parent}/outputs")

    if config_file:
        settings = Settings(config_file=config_file)
    else:
        settings = Settings()

    stanza_logger.handlers[0].setLevel(logging.INFO)
    logger.handlers[0].setLevel(logging.INFO)

    if very_verbose:
        stanza_logger.handlers[1].setLevel(logging.INFO)
        logger.handlers[1].setLevel(logging.INFO)

    elif verbose:
        stanza_logger.handlers[1].setLevel(logging.WARNING)
        logger.handlers[1].setLevel(logging.INFO)
    else:
        stanza_logger.handlers[1].setLevel(logging.WARNING)
        logger.handlers[1].setLevel(logging.WARNING)
        

    if not input_path.exists():
        logger.warning("INPUT_PATH: '%s' does not exist. Check path", input_path)
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

    if n_missing == 0:
        logger.warning(f"Found {n_transcripts} transcripts. Unprocessed: {n_missing}.\
            \nCannot process files that have already been processed!!\
            \nPlease remove pickled networks and image files from the output directory and try again.")

    # Only start the servers if there are files to process
    elif force or n_missing > 0:
        logger.info(f"Found {n_transcripts} transcripts. Unprocessed: {n_missing}")

        t = threading.Thread(target=animate)
        t.daemon = True
        t.start()

        corenlp_client = CoreNLPClient(be_quiet=True,
            properties={
                "annotators": "tokenize,ssplit,pos,lemma,ner,parse,depparse,coref,natlog,openie",
                "timeout": "50000",
            },
            port=settings.netts_config.server.corenlp.port,
        )
        
        # Doesn't block
        corenlp_client.start()

        openie_client = OpenIEClient(
            quiet=True, port=settings.netts_config.server.openie.port
        )
        # Blocks
        openie_client.connect()

        preprocess_config = settings.netts_config.preprocess

        for transcript_file in all_transcript_files:
            if transcript_file.missing or force:
                transcript_file.process(
                    corenlp_client, openie_client, preprocess_config
                )
            transcript_file.dump()

        corenlp_client.stop()
        openie_client.close()

        done = True

    # Save figures
    if figure:
        for transcript_file in all_transcript_files:

            plot_file = transcript_file.output_graph_file(fig_format)

            if not plot_file.exists() or force:

                logger.info("Creating figure: %s", plot_file)
                transcript_file.plot_graph()
                plt.savefig(transcript_file.output_graph_file(fig_format))
    done = True

@app.command()
def config() -> None:
    """Create a default configuration file"""

    typer.echo(netts.Config.default())


@app.command()
def config_verify(config_file: Path) -> None:
    """Verify a configuration file"""

    # This will raise an exception if config is invalid (i.e missing values or incorrect syntax)
    netts.Config.load(config_file)

    typer.echo("Configuration is valid")


if __name__ == "__main__":
    app()
