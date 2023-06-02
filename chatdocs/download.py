from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import CTransformers

from . import config


def download() -> None:
    HuggingFaceInstructEmbeddings(model_name=config.EMBEDDINGS_MODEL)
    CTransformers(model=config.MODEL, model_type=config.MODEL_TYPE)
