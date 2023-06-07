from pathlib import Path
from typing import Any, Callable, Dict, Optional

from langchain.callbacks.base import BaseCallbackHandler
from langchain.llms import CTransformers, HuggingFacePipeline
from langchain.llms.base import LLM

from .utils import merge


def get_gptq_llm(config: Dict[str, Any]) -> LLM:
    try:
        from auto_gptq import AutoGPTQForCausalLM
    except ImportError:
        raise ImportError(
            "Could not import `auto_gptq` package. "
            "Please install it with `pip install chatdocs[gptq]`"
        )

    from transformers import AutoTokenizer, TextGenerationPipeline

    local_files_only = not config["download"]
    config = {**config["gptq"]}
    model_name_or_path = config.pop("model")
    model_file = config.pop("model_file", None)
    pipeline_kwargs = config.pop("pipeline_kwargs", None) or {}

    model_basename = None
    use_safetensors = False
    if model_file:
        model_basename = Path(model_file).stem
        use_safetensors = model_file.endswith(".safetensors")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path,
        local_files_only=local_files_only,
    )
    model = AutoGPTQForCausalLM.from_quantized(
        model_name_or_path,
        model_basename=model_basename,
        use_safetensors=use_safetensors,
        local_files_only=local_files_only,
        **config,
    )
    pipeline = TextGenerationPipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        **pipeline_kwargs,
    )
    return HuggingFacePipeline(pipeline=pipeline)


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
    elif config["llm"] == "gptq":
        llm = get_gptq_llm(config)
    else:
        config = {**config["huggingface"]}
        config["model_id"] = config.pop("model")
        config = merge(config, {"model_kwargs": {"local_files_only": local_files_only}})
        llm = HuggingFacePipeline.from_model_id(task="text-generation", **config)
    return llm
