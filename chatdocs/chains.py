from typing import Any, Callable, Dict, Optional

from langchain.chains import RetrievalQA
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

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
    chain_type_kwargs = {}

    # Prepare and pass custom prompt if provided
    if "retriever" in config and "custom_prompt" in config["retriever"]:
        custom_prompt = config["retriever"]["custom_prompt"]

        messages = [
            SystemMessagePromptTemplate.from_template(custom_prompt),
            HumanMessagePromptTemplate.from_template("{question}")
        ]

        chain_type_kwargs["prompt"] = ChatPromptTemplate.from_messages(messages)

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs
    )
