from typing import Any, Optional

from chromadb.config import Settings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import CTransformers, HuggingFacePipeline
from langchain.vectorstores import Chroma
from rich import print
from rich.markup import escape
from rich.panel import Panel

from . import config


def print_response(text: str) -> None:
    print(f"[bright_cyan]{escape(text)}", end="", flush=True)


class StreamingPrintCallbackHandler(StreamingStdOutCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        print_response(token)


def chat(
    *,
    persist_directory: str,
    hf: bool,
    download: bool,
    model: str,
    model_type: Optional[str] = None,
    model_file: Optional[str] = None,
    lib: Optional[str] = None,
    query: Optional[str] = None,
) -> None:
    local_files_only = not download
    embeddings = HuggingFaceInstructEmbeddings(model_name=config.EMBEDDINGS_MODEL)
    chroma_settings = Settings(
        chroma_db_impl=config.CHROMA_DB_IMPL,
        persist_directory=persist_directory,
        anonymized_telemetry=False,
    )
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        client_settings=chroma_settings,
    )
    retriever = db.as_retriever(search_kwargs={"k": 4})

    if hf:
        llm = HuggingFacePipeline.from_model_id(
            model_id=model,
            task="text-generation",
            model_kwargs={"local_files_only": local_files_only},
            pipeline_kwargs={"max_new_tokens": 256},
        )
    else:
        llm = CTransformers(
            model=model,
            model_type=model_type,
            model_file=model_file,
            config={"context_length": 1024, "local_files_only": local_files_only},
            lib=lib,
            callbacks=[StreamingPrintCallbackHandler()],
        )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )

    interactive = not query
    print()
    if interactive:
        print("Type your query below and press Enter.")
        print("Type 'exit' or 'quit' or 'q' to exit the application.\n")
    while True:
        print("[bold]Q: ", end="", flush=True)
        if interactive:
            query = input()
        else:
            print(escape(query))
        print()
        if query.strip() in ["exit", "quit", "q"]:
            print("Exiting...\n")
            break
        print("[bold]A:", end="", flush=True)

        res = qa(query)
        if hf:
            print_response(res["result"])

        print()
        for doc in res["source_documents"]:
            source, content = doc.metadata["source"], doc.page_content
            print(
                Panel(
                    f"[bright_blue]{escape(source)}[/bright_blue]\n\n{escape(content)}"
                )
            )
        print()

        if not interactive:
            break
