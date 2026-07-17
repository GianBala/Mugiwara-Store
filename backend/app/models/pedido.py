"""Models das entidades PEDIDO e ITEM_PEDIDO."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Pedido(Base):
    __tablename__ = "pedido"
    __table_args__ = (
        CheckConstraint("valor_total >= 0", name="ck_pedido_valor_nao_negativo"),
    )

    id_pedido: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data_pedido: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    forma_pagamento: Mapped[str] = mapped_column(String(50), nullable=False)
    status_pagamento: Mapped[str] = mapped_column(String(50), nullable=False, default="APROVADO")
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_funcionario: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("funcionario.id_funcionario")
    )

    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )
    cliente = relationship("Cliente")
    funcionario = relationship("Funcionario")


class ItemPedido(Base):
    __tablename__ = "item_pedido"
    __table_args__ = (
        CheckConstraint("quantidade > 0", name="ck_item_quantidade_positiva"),
        CheckConstraint("preco_unitario_na_venda > 0", name="ck_item_preco_positivo"),
    )

    id_pedido: Mapped[int] = mapped_column(
        Integer, ForeignKey("pedido.id_pedido", ondelete="CASCADE"), primary_key=True
    )
    id_produto: Mapped[int] = mapped_column(
        Integer, ForeignKey("produto.id_produto"), primary_key=True
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_unitario_na_venda: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
    produto = relationship("Produto")
