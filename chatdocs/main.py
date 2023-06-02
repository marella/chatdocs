from pathlib import Path
from typing import List, Optional

from typing_extensions import Annotated
import typer

from . import config
from .add import add as add_
from .chat import chat as chat_
from .download import download as download_

app = typer.Typer()


@app.command()
def download():
    download_()


@app.command()
def add(
    directory: Annotated[
        Path, typer.Argument(help="The path to a directory containing documents.")
    ],
    db: Annotated[
        Path,
        typer.Option(help="The path to a directory to store the processed documents."),
    ] = config.PERSIST_DIRECTORY,
):
    add_(
        source_directory=str(directory),
        persist_directory=str(db.resolve()),
    )


@app.command()
def chat(
    query: Annotated[
        Optional[str],
        typer.Argument(
            help="The query to use for retrieval. If not specified, runs in interactive mode."
        ),
    ] = None,
    model: Annotated[
        str,
        typer.Option(
            help="The path to a model file or directory or the name of a Hugging Face Hub model repo."
        ),
    ] = config.MODEL,
    model_type: Annotated[
        Optional[str],
        typer.Option(help="The model type."),
    ] = None,
    model_file: Annotated[
        Optional[str],
        typer.Option(help="The name of the model file in repo or directory."),
    ] = None,
    download: Annotated[
        bool,
        typer.Option(help="Whether to download the model or run offline."),
    ] = False,
    db: Annotated[
        Path,
        typer.Option(
            help="The path to a directory containing the processed documents."
        ),
    ] = config.PERSIST_DIRECTORY,
    hf: Annotated[
        bool,
        typer.Option(help="Whether to use 🤗 Transformers."),
    ] = False,
    lib: Annotated[
        Optional[str],
        typer.Option(
            help="The path to a shared library or one of `avx2`, `avx`, `basic`."
        ),
    ] = None,
):
    if hf and model == config.MODEL:
        raise ValueError(
            "Please specify a compatible model for 🤗 Transformers using the `--model` option."
        )
    if not model_type and model == config.MODEL:
        model_type = config.MODEL_TYPE
    chat_(
        query=query,
        model=model,
        model_type=model_type,
        model_file=model_file,
        download=download,
        persist_directory=str(db.resolve()),
        hf=hf,
        lib=lib,
    )
