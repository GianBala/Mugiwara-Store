"""Configuração da conexão com o banco de dados via SQLAlchemy 2.0."""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

# SQLite (usado em testes) exige `check_same_thread=False` para uso com FastAPI.
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    """Classe base declarativa para todos os models."""


def get_db() -> Generator[Session, None, None]:
    """Dependência FastAPI que fornece uma sessão por requisição."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
