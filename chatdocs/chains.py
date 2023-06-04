from typing import Any, Dict

from langchain.chains import RetrievalQA

from .llms import get_llm
from .vectorstores import get_vectorstore


def get_retrieval_qa(config: Dict[str, Any]) -> RetrievalQA:
    db = get_vectorstore(config)
    retriever = db.as_retriever(**config["retriever"])
    llm = get_llm(config)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )
