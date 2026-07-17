"""Model da entidade ENDERECO_CEP."""
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class EnderecoCep(Base):
    __tablename__ = "endereco_cep"

    cep: Mapped[str] = mapped_column(String(9), primary_key=True)
    logradouro: Mapped[str | None] = mapped_column(String(255))
    bairro: Mapped[str | None] = mapped_column(String(100))
    cidade: Mapped[str | None] = mapped_column(String(100))
    estado: Mapped[str | None] = mapped_column(String(2))
