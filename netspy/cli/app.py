from pathlib import Path
from typing import Optional

import typer

import netspy
from netspy.config import get_settings

app = typer.Typer()
setting = get_settings()


@app.command()
def install(
    directory: Optional[Path] = typer.Option(
        None, help="Directory to install netspy dependencies to"
    )
) -> None:
    """Install all tool dependencies and langauge models"""

    netspy.install_models(directory)


@app.command()
def home() -> None:
    typer.echo(f"Netspy directory: {setting.netspy_dir}")


if __name__ == "__main__":
    app()
