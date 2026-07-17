"""Model da entidade PRODUTO."""
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import CheckConstraint, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Produto(Base):
    __tablename__ = "produto"
    __table_args__ = (
        CheckConstraint("preco > 0", name="ck_produto_preco_positivo"),
        CheckConstraint("quantidade_estoque >= 0", name="ck_produto_estoque_nao_negativo"),
    )

    id_produto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantidade_estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    fabricado_em_mari: Mapped[bool] = mapped_column(default=False, nullable=False)
    imagem: Mapped[str | None] = mapped_column(String(255))
