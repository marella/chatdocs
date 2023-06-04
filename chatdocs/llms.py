from typing import Any, Dict

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import CTransformers, HuggingFacePipeline
from langchain.llms.base import LLM

from .utils import merge, print_answer


class StreamingPrintCallbackHandler(StreamingStdOutCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        print_answer(token)


def get_llm(config: Dict[str, Any]) -> LLM:
    local_files_only = not config["download"]
    if config["llm"] == "ctransformers":
        config = {**config["ctransformers"]}
        config = merge(config, {"config": {"local_files_only": local_files_only}})
        llm = CTransformers(callbacks=[StreamingPrintCallbackHandler()], **config)
    else:
        config = {**config["huggingface"]}
        config["model_id"] = config.pop("model")
        config = merge(config, {"model_kwargs": {"local_files_only": local_files_only}})
        llm = HuggingFacePipeline.from_model_id(task="text-generation", **config)
    return llm
