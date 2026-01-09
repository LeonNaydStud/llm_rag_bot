from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

_vector_store = None


def get_vector_store() -> Chroma:
    global _vector_store

    if _vector_store is None:
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            encode_kwargs={"normalize_embeddings": True},
        )

        _vector_store = Chroma(
            collection_name=settings.chroma_collection,
            embedding_function=embeddings,
            persist_directory=settings.chroma_path,
        )

    return _vector_store
