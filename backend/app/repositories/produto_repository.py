"""Repositório de acesso a dados de PRODUTO."""
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.produto import Produto


class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(
        self,
        *,
        busca: str | None = None,
        categoria: str | None = None,
        preco_min: Decimal | None = None,
        preco_max: Decimal | None = None,
    ) -> list[Produto]:
        stmt = select(Produto)
        if busca:
            stmt = stmt.where(Produto.nome.ilike(f"%{busca}%"))
        if categoria:
            stmt = stmt.where(Produto.categoria == categoria)
        if preco_min is not None:
            stmt = stmt.where(Produto.preco >= preco_min)
        if preco_max is not None:
            stmt = stmt.where(Produto.preco <= preco_max)
        stmt = stmt.order_by(Produto.id_produto)
        return list(self.db.scalars(stmt).all())

    def obter(self, id_produto: int) -> Produto | None:
        return self.db.get(Produto, id_produto)

    def obter_para_atualizar(self, id_produto: int) -> Produto | None:
        """Obtém o produto com lock de linha (FOR UPDATE) para operações de estoque."""
        stmt = select(Produto).where(Produto.id_produto == id_produto).with_for_update()
        return self.db.scalars(stmt).first()

    def listar_categorias(self) -> list[str]:
        stmt = select(Produto.categoria).distinct().order_by(Produto.categoria)
        return [c for c in self.db.scalars(stmt).all() if c]

    def listar_estoque_baixo(self, limite: int) -> list[Produto]:
        stmt = (
            select(Produto)
            .where(Produto.quantidade_estoque < limite)
            .order_by(Produto.quantidade_estoque)
        )
        return list(self.db.scalars(stmt).all())

    def criar(self, produto: Produto) -> Produto:
        self.db.add(produto)
        self.db.flush()
        return produto

    def remover(self, produto: Produto) -> None:
        self.db.delete(produto)
        self.db.flush()
