"""Configuração central da aplicação, carregada de variáveis de ambiente."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação (12-factor: tudo via ambiente)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ---- Identidade da aplicação ----
    PROJECT_NAME: str = "Mugiwara Store"
    API_V1_PREFIX: str = "/api"

    # ---- Banco de dados ----
    # Em testes usamos SQLite; em produção/Docker, PostgreSQL.
    DATABASE_URL: str = "sqlite:///./mugiwara_dev.db"

    # ---- Segurança / JWT ----
    SECRET_KEY: str = "dev-secret-key-nao-use-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # ---- Regra de negócio ----
    # Percentual de desconto aplicado a clientes elegíveis (0..1).
    DESCONTO_PERCENTUAL: float = 0.10
    # Limite abaixo do qual um produto é considerado "estoque baixo".
    LIMITE_ESTOQUE_BAIXO: int = 5

    # ---- CORS ----
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:8080,http://localhost"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
