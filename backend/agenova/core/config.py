from functools import lru_cache
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AgeNova"
    environment: str = Field(default="local", validation_alias=AliasChoices("AGENOVA_ENV", "ENVIRONMENT"))
    llm_provider: str = Field(
        default="mock", validation_alias=AliasChoices("AGENOVA_LLM_PROVIDER", "LLM_PROVIDER")
    )
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        validation_alias=AliasChoices("AGENOVA_EMBEDDING_MODEL", "EMBEDDING_MODEL"),
    )
    use_sentence_transformers: bool = Field(
        default=False,
        validation_alias=AliasChoices("AGENOVA_USE_SENTENCE_TRANSFORMERS", "USE_SENTENCE_TRANSFORMERS"),
    )
    max_chunk_chars: int = 900
    chunk_overlap: int = 120
    retrieval_top_k: int = 5
    openai_api_key: str | None = None
    qdrant_url: str | None = None
    neo4j_uri: str | None = None
    neo4j_user: str | None = None
    neo4j_password: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
