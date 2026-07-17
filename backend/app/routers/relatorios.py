"""Rotas de RELATÓRIOS gerenciais (restritas a funcionários)."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.deps import requer_funcionario
from app.schemas.produto import ProdutoOut
from app.schemas.relatorio import RelatorioVendasMensal, ResumoEstoque
from app.services.relatorio_service import RelatorioService

router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"],
    dependencies=[Depends(requer_funcionario)],
)


@router.get("/estoque", response_model=ResumoEstoque)
def resumo_estoque(db: Session = Depends(get_db)) -> ResumoEstoque:
    """Relatório gerencial: total de produtos, unidades e valor do estoque."""
    return RelatorioService(db).resumo_estoque()


@router.get("/estoque-baixo", response_model=list[ProdutoOut])
def estoque_baixo(db: Session = Depends(get_db)) -> list[ProdutoOut]:
    """CV-08: produtos com estoque abaixo do limite (< 5)."""
    return RelatorioService(db).produtos_estoque_baixo()


@router.get("/vendas", response_model=RelatorioVendasMensal)
def vendas_mensal(
    db: Session = Depends(get_db),
    ano: int | None = Query(None, ge=2000, le=2100),
    mes: int | None = Query(None, ge=1, le=12),
) -> RelatorioVendasMensal:
    """CA-06: relatório mensal de vendas com ranking de vendedores."""
    agora = datetime.now(timezone.utc)
    return RelatorioService(db).vendas_mensal(ano or agora.year, mes or agora.month)
