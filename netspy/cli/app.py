from pathlib import Path
from typing import IO, Optional
import pickle
import typer
from matplotlib import pyplot as plt
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

    netspy.install_dependencies(directory)


@app.command()
def home() -> None:
    typer.echo(f"Netspy directory: {setting.netspy_dir}")


@app.command()
def run(path: Path, output_dir: Path, pattern: str = "*", force: bool = False, figure: bool = True, fig_format: str = 'png') -> None:
    """Process a single file or directory"""

    if not path.exists():
        raise IOError("path does not exist")

    if path.is_dir():
        all_input_files = list(path.glob(pattern))
    else:
        all_input_files = [path]

    for f in all_input_files:


        output_file = output_dir / f.stem

        if not output_file.exists() or force:

            transcript = f.read_text(encoding="utf-8")
            graph = netspy.speech_graph(transcript)

            output_dir.mkdir(exist_ok=True)
            with output_file.open(mode = "wb") as output_f:
                netspy.pickle_graph(graph, output_f)
        else:
            
            graph = pickle.loads(output_file.read_bytes())

        if figure:

            _, ax = plt.subplots()
            netspy.plot_graph(
                graph,
                ax,
                edge_color="black",
                width=1,
                linewidths=1,
                node_size=500,
                node_color="pink",
                alpha=0.9,
                labels={node: node for node in graph.nodes()},
            )

            plt.savefig(output_file.parent / (output_file.name + '.' + fig_format))


if __name__ == "__main__":
    app()
