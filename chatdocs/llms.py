from typing import Any, Callable, Dict, Optional

from langchain.callbacks.base import BaseCallbackHandler
from langchain.llms import CTransformers, HuggingFacePipeline
from langchain.llms.base import LLM

from .utils import merge


def get_llm(
    config: Dict[str, Any],
    *,
    callback: Optional[Callable[[str], None]] = None,
) -> LLM:
    class CallbackHandler(BaseCallbackHandler):
        def on_llm_new_token(self, token: str, **kwargs) -> None:
            callback(token)

    callbacks = [CallbackHandler()] if callback else None
    local_files_only = not config["download"]
    if config["llm"] == "ctransformers":
        config = {**config["ctransformers"]}
        config = merge(config, {"config": {"local_files_only": local_files_only}})
        llm = CTransformers(callbacks=callbacks, **config)
    else:
        config = {**config["huggingface"]}
        config["model_id"] = config.pop("model")
        config = merge(config, {"model_kwargs": {"local_files_only": local_files_only}})
        llm = HuggingFacePipeline.from_model_id(task="text-generation", **config)
    return llm
