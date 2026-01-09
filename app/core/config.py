from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Python FAQ RAG"
    api_version: str = "v1"

    chroma_collection: str = "python_faq"
    chroma_path: str = "./chroma_db"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "google/flan-t5-base"

    max_context_chars: int = 1800
    default_top_k: int = 3

    class Config:
        env_file = ".env"


settings = Settings()
