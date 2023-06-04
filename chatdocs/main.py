from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from .config import get_config

app = typer.Typer()

ConfigPath = Annotated[
    Optional[Path],
    typer.Option(
        "--config",
        "-c",
        help="The path to a chatdocs.yml configuration file.",
    ),
]


@app.command()
def download(config: ConfigPath = None):
    from .download import download

    config = get_config(config)
    download(config=config)


@app.command()
def add(
    directory: Annotated[
        Path,
        typer.Argument(help="The path to a directory containing documents."),
    ],
    config: ConfigPath = None,
):
    from .add import add

    config = get_config(config)
    add(config=config, source_directory=str(directory))


@app.command()
def chat(
    query: Annotated[
        Optional[str],
        typer.Argument(
            help="The query to use for retrieval. If not specified, runs in interactive mode."
        ),
    ] = None,
    config: ConfigPath = None,
):
    from .chat import chat

    config = get_config(config)
    chat(config=config, query=query)
