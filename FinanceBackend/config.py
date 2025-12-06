from pathlib import Path
from typing import Optional
from pydantic import (
    Field,
    SecretStr,
    AnyHttpUrl,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    SECRET_KEY: SecretStr
    DEBUG: bool = False
    DOMAIN: str = "127.0.0.1:8000"


    PG_NAME: str
    PG_USER: str
    PG_PASSWORD: SecretStr
    PG_HOST: str = "localhost"
    PG_PORT: int = Field(5432, ge=1, le=65535)

    CURRENCY_API_KEY: Optional[SecretStr] = None
    CHEQUE_API_KEY: Optional[SecretStr] = None


    EMAIL_HOST: str
    EMAIL_PORT: int = Field(587, ge=1, le=65535)
    EMAIL_USE_TLS: bool = False
    EMAIL_USE_SSL: bool = False
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: SecretStr
    DEFAULT_FROM_EMAIL: str
    FQDN_FOR_BLACKBOX: str

    @field_validator("EMAIL_USE_SSL", "EMAIL_USE_TLS", mode="before")
    def _normalize_bool(cls, v):
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)

    @field_validator("EMAIL_USE_SSL")
    def check_ssl_tls_exclusive(cls, ssl, info):
        tls = info.data.get("EMAIL_USE_TLS")
        if ssl and tls:
            raise ValueError("EMAIL_USE_SSL and EMAIL_USE_TLS cannot both be True")
        return ssl


    REDIS_ADR: AnyHttpUrl = "http://localhost:6379"


    CLIENT_ID: str
    CL_SECRET: SecretStr = Field(..., alias="CLIENT_SECRET")
    REDIRECT_URI: AnyHttpUrl

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )



settings = Settings()
