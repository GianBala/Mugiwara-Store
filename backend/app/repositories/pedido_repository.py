"""Repositório de acesso a dados de PEDIDO."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.pedido import Pedido


class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.flush()
        return pedido

    def obter(self, id_pedido: int) -> Pedido | None:
        stmt = (
            select(Pedido)
            .where(Pedido.id_pedido == id_pedido)
            .options(selectinload(Pedido.itens))
        )
        return self.db.scalars(stmt).first()

    def listar_por_cliente(self, id_cliente: int) -> list[Pedido]:
        stmt = (
            select(Pedido)
            .where(Pedido.id_cliente == id_cliente)
            .options(selectinload(Pedido.itens))
            .order_by(Pedido.data_pedido.desc())
        )
        return list(self.db.scalars(stmt).all())

    def listar_todos(self) -> list[Pedido]:
        stmt = (
            select(Pedido)
            .options(selectinload(Pedido.itens))
            .order_by(Pedido.data_pedido.desc())
        )
        return list(self.db.scalars(stmt).all())
