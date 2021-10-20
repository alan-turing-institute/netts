from pathlib import Path
from typing import Optional

import typer

import netspy
from netspy.cli.util import Color, cprint

app = typer.Typer()

CONFIG_FILE = Path("netspy.toml")


@app.command()
def init(
    overwrite: bool = typer.Option(
        False, "--overwrite", help="If already exists overwrite"
    )
) -> None:
    "Create a default configuration file in the current directory"

    if (not CONFIG_FILE.exists()) or overwrite:

        CONFIG_FILE.write_text(netspy.Config.default(), encoding="utf-8")

    else:
        cprint(
            Color("Config file already exists. Pass argument: ", fg="red"),
            Color("--overwrite", fg="blue"),
        )
        raise typer.Abort


@app.command()
def verify(
    config_file: Optional[Path] = typer.Option(
        None, help="path to file, otherwise uses 'netspy.toml' in current directory"
    )
) -> None:
    """Verify a configuration file."""

    if not config_file and (not CONFIG_FILE.exists()):
        cprint(
            Color(
                "'netspy.toml' not found in current directory and --config-file not provided",
                fg="red",
            )
        )
        raise typer.Abort

    # This will raise an exception if config is invalid (i.e missing values or incorrect syntax)
    netspy.Config.load(config_file if config_file else CONFIG_FILE)

    cprint(
        Color(
            "Configuration is valid",
            fg="green",
        )
    )
