from typing import Any, Dict

from .embeddings import get_embeddings
from .llms import get_llm


def download(config: Dict[str, Any]) -> None:
    config = {**config, "download": True}
    get_embeddings(config)
    get_llm(config)
