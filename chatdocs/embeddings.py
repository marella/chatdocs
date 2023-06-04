from typing import Any, Dict

from langchain.embeddings import HuggingFaceInstructEmbeddings, HuggingFaceEmbeddings
from langchain.embeddings.base import Embeddings


def get_embeddings(config: Dict[str, Any]) -> Embeddings:
    config = {**config["embeddings"]}
    config["model_name"] = config.pop("model")
    if config["model_name"].startswith("hkunlp/"):
        Provider = HuggingFaceInstructEmbeddings
    else:
        Provider = HuggingFaceEmbeddings
    return Provider(**config)
