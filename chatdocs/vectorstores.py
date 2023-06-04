from typing import Any, Dict, List

from chromadb.config import Settings
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStore

from .embeddings import get_embeddings


def get_vectorstore(config: Dict[str, Any]) -> VectorStore:
    embeddings = get_embeddings(config)
    config = config["chroma"]
    return Chroma(
        persist_directory=config["persist_directory"],
        embedding_function=embeddings,
        client_settings=Settings(**config),
    )


def get_vectorstore_from_documents(
    config: Dict[str, Any],
    documents: List[Document],
) -> VectorStore:
    embeddings = get_embeddings(config)
    config = config["chroma"]
    return Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=config["persist_directory"],
        client_settings=Settings(**config),
    )
