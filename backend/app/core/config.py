from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env.mc"


class Settings(BaseSettings):
    app_name: str = "Morning Classes Check API"
    app_env: str = Field(default="development", alias="APP_ENV")

    mc_db_host: str = Field(default="127.0.0.1", alias="MC_DB_HOST")
    mc_db_port: int = Field(default=5432, alias="MC_DB_PORT")
    mc_db_name: str = Field(default="morning_classes_check", alias="MC_DB_NAME")
    mc_db_user: str = Field(default="mc_app", alias="MC_DB_USER")
    mc_db_password: str = Field(
        default="change_me_with_a_strong_password", alias="MC_DB_PASSWORD"
    )
    mc_db_schema: str = Field(default="mc_core", alias="MC_DB_SCHEMA")
    mc_meta_schema: str = Field(default="mc_meta", alias="MC_META_SCHEMA")
    mc_default_role: str = Field(default="operator", alias="MC_DEFAULT_ROLE")
    mc_run_lock_ttl_seconds: int = Field(default=1800, alias="MC_RUN_LOCK_TTL_SECONDS")
    mc_transient_retry_count: int = Field(default=1, alias="MC_TRANSIENT_RETRY_COUNT")

    database_url: Optional[str] = Field(default=None, alias="DATABASE_URL")
    alembic_database_url: Optional[str] = Field(default=None, alias="ALEMBIC_DATABASE_URL")
    alembic_version_table: str = Field(
        default="alembic_version_mc", alias="ALEMBIC_VERSION_TABLE"
    )
    alembic_version_schema: str = Field(
        default="mc_meta", alias="ALEMBIC_VERSION_SCHEMA"
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        password = quote_plus(self.mc_db_password)
        return (
            f"postgresql+psycopg://{self.mc_db_user}:{password}"
            f"@{self.mc_db_host}:{self.mc_db_port}/{self.mc_db_name}"
        )

    @property
    def sqlalchemy_alembic_url(self) -> str:
        return self.alembic_database_url or self.sqlalchemy_database_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
