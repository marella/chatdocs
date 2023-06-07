from typing import Any, Dict, Optional

from rich import print
from rich.markup import escape
from rich.panel import Panel

from .chains import get_retrieval_qa


def print_answer(text: str) -> None:
    print(f"[bright_cyan]{escape(text)}", end="", flush=True)


def chat(config: Dict[str, Any], query: Optional[str] = None) -> None:
    qa = get_retrieval_qa(config, callback=print_answer)

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
        if config["llm"] != "ctransformers":
            print_answer(res["result"])

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
