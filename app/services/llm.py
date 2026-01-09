from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from app.core.config import settings

_llm = None


def get_llm() -> HuggingFacePipeline:
    global _llm

    if _llm is None:
        pipe = pipeline(
            "text2text-generation",
            model=settings.llm_model,
            max_new_tokens=200,
            truncation=True,
        )

        _llm = HuggingFacePipeline(pipeline=pipe)

    return _llm
