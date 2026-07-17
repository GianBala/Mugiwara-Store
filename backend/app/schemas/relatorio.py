"""Schemas Pydantic para relatórios gerenciais."""
from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class VendaPorVendedor(BaseModel):
    id_funcionario: int
    nome_vendedor: str
    cargo: str | None = None
    total_pedidos: int
    total_itens: int
    total_vendido: Decimal


class RelatorioVendasMensal(BaseModel):
    mes_referencia: str
    total_pedidos: int
    total_vendido: Decimal
    ranking_vendedores: list[VendaPorVendedor]


class ResumoEstoque(BaseModel):
    total_produtos: int
    total_unidades: int
    valor_total_estoque: Decimal
    produtos_estoque_baixo: int
