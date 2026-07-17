"""Rotas de PRODUTO: catálogo público + CRUD restrito a funcionários."""
from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.deps import requer_funcionario
from app.schemas.produto import ProdutoCreate, ProdutoOut, ProdutoUpdate
from app.services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# ---------------------------------------------------------------------------
#  Público (CA-01): navegação, busca e filtros sem autenticação
# ---------------------------------------------------------------------------
@router.get("", response_model=list[ProdutoOut])
def listar_produtos(
    busca: str | None = None,
    categoria: str | None = None,
    preco_min: Decimal | None = None,
    preco_max: Decimal | None = None,
    db: Session = Depends(get_db),
) -> list[ProdutoOut]:
    return ProdutoService(db).listar(busca, categoria, preco_min, preco_max)


@router.get("/categorias", response_model=list[str])
def listar_categorias(db: Session = Depends(get_db)) -> list[str]:
    return ProdutoService(db).listar_categorias()


@router.get("/{id_produto}", response_model=ProdutoOut)
def obter_produto(id_produto: int, db: Session = Depends(get_db)) -> ProdutoOut:
    return ProdutoService(db).obter(id_produto)


# ---------------------------------------------------------------------------
#  Restrito a funcionários (CV-01): criação, edição e remoção
# ---------------------------------------------------------------------------
@router.post(
    "",
    response_model=ProdutoOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requer_funcionario)],
)
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)) -> ProdutoOut:
    return ProdutoService(db).criar(dados)


@router.put(
    "/{id_produto}",
    response_model=ProdutoOut,
    dependencies=[Depends(requer_funcionario)],
)
def atualizar_produto(
    id_produto: int, dados: ProdutoUpdate, db: Session = Depends(get_db)
) -> ProdutoOut:
    return ProdutoService(db).atualizar(id_produto, dados)


@router.delete(
    "/{id_produto}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(requer_funcionario)],
)
def remover_produto(id_produto: int, db: Session = Depends(get_db)):
    ProdutoService(db).remover(id_produto)
    return None
