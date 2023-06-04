from typing import Any, Dict

import rich
from rich.markup import escape
from deepmerge import always_merger


def merge(a: Dict[Any, Any], b: Dict[Any, Any]) -> Dict[Any, Any]:
    c = {}
    always_merger.merge(c, a)
    always_merger.merge(c, b)
    return c


def print_answer(text: str) -> None:
    rich.print(f"[bright_cyan]{escape(text)}", end="", flush=True)
