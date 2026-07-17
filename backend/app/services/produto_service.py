"""Regras de negócio de PRODUTO (CRUD do catálogo)."""
from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import RecursoNaoEncontrado
from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


class ProdutoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProdutoRepository(db)

    def listar(
        self,
        busca: str | None = None,
        categoria: str | None = None,
        preco_min: Decimal | None = None,
        preco_max: Decimal | None = None,
    ) -> list[Produto]:
        return self.repo.listar(
            busca=busca, categoria=categoria, preco_min=preco_min, preco_max=preco_max
        )

    def obter(self, id_produto: int) -> Produto:
        produto = self.repo.obter(id_produto)
        if not produto:
            raise RecursoNaoEncontrado(f"Produto {id_produto} não encontrado")
        return produto

    def listar_categorias(self) -> list[str]:
        return self.repo.listar_categorias()

    def criar(self, dados: ProdutoCreate) -> Produto:
        produto = Produto(**dados.model_dump())
        self.repo.criar(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def atualizar(self, id_produto: int, dados: ProdutoUpdate) -> Produto:
        produto = self.obter(id_produto)
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(produto, campo, valor)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def remover(self, id_produto: int) -> None:
        produto = self.obter(id_produto)
        self.repo.remover(produto)
        self.db.commit()
