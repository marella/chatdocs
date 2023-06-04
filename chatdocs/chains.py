from typing import Any, Callable, Dict, Optional

from langchain.chains import RetrievalQA

from .llms import get_llm
from .vectorstores import get_vectorstore


def get_retrieval_qa(
    config: Dict[str, Any],
    *,
    callback: Optional[Callable[[str], None]] = None,
) -> RetrievalQA:
    db = get_vectorstore(config)
    retriever = db.as_retriever(**config["retriever"])
    llm = get_llm(config, callback=callback)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )
