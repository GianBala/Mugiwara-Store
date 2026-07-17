"""Relatórios gerenciais: estoque e vendas por vendedor.

As agregações são feitas em Python a partir de consultas ORM para garantir
portabilidade entre PostgreSQL (produção) e SQLite (testes). Em produção, a
VIEW `vw_vendas_por_vendedor` (db/init.sql) oferece a mesma consolidação em SQL.
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.schemas.relatorio import (
    RelatorioVendasMensal,
    ResumoEstoque,
    VendaPorVendedor,
)


class RelatorioService:
    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    #  Estoque
    # ------------------------------------------------------------------
    def resumo_estoque(self) -> ResumoEstoque:
        total_produtos = self.db.scalar(select(func.count(Produto.id_produto))) or 0
        total_unidades = self.db.scalar(select(func.coalesce(func.sum(Produto.quantidade_estoque), 0))) or 0
        valor_total = self.db.scalar(
            select(func.coalesce(func.sum(Produto.preco * Produto.quantidade_estoque), 0))
        ) or Decimal("0")
        estoque_baixo = self.db.scalar(
            select(func.count(Produto.id_produto)).where(
                Produto.quantidade_estoque < settings.LIMITE_ESTOQUE_BAIXO
            )
        ) or 0
        return ResumoEstoque(
            total_produtos=int(total_produtos),
            total_unidades=int(total_unidades),
            valor_total_estoque=Decimal(str(valor_total)),
            produtos_estoque_baixo=int(estoque_baixo),
        )

    def produtos_estoque_baixo(self) -> list[Produto]:
        """CV-08: apenas produtos com quantidade_estoque < limite."""
        stmt = (
            select(Produto)
            .where(Produto.quantidade_estoque < settings.LIMITE_ESTOQUE_BAIXO)
            .order_by(Produto.quantidade_estoque)
        )
        return list(self.db.scalars(stmt).all())

    # ------------------------------------------------------------------
    #  Vendas por vendedor (relatório mensal)
    # ------------------------------------------------------------------
    def vendas_mensal(self, ano: int, mes: int) -> RelatorioVendasMensal:
        stmt = (
            select(Pedido)
            .options(selectinload(Pedido.itens), selectinload(Pedido.funcionario))
            .where(
                func.extract("year", Pedido.data_pedido) == ano,
                func.extract("month", Pedido.data_pedido) == mes,
            )
        )
        pedidos = list(self.db.scalars(stmt).all())

        total_vendido = Decimal("0.00")
        por_vendedor: dict[int, dict] = defaultdict(
            lambda: {"nome": None, "cargo": None, "pedidos": 0, "itens": 0, "total": Decimal("0.00")}
        )

        for pedido in pedidos:
            total_vendido += pedido.valor_total
            fid = pedido.id_funcionario or 0
            reg = por_vendedor[fid]
            reg["pedidos"] += 1
            reg["total"] += pedido.valor_total
            reg["itens"] += sum(item.quantidade for item in pedido.itens)
            if pedido.funcionario:
                reg["nome"] = pedido.funcionario.nome
                reg["cargo"] = pedido.funcionario.cargo
            else:
                reg["nome"] = "Loja (autoatendimento)"

        ranking = [
            VendaPorVendedor(
                id_funcionario=fid,
                nome_vendedor=reg["nome"] or "Desconhecido",
                cargo=reg["cargo"],
                total_pedidos=reg["pedidos"],
                total_itens=reg["itens"],
                total_vendido=reg["total"],
            )
            for fid, reg in por_vendedor.items()
        ]
        ranking.sort(key=lambda v: v.total_vendido, reverse=True)

        return RelatorioVendasMensal(
            mes_referencia=f"{ano:04d}-{mes:02d}",
            total_pedidos=len(pedidos),
            total_vendido=total_vendido,
            ranking_vendedores=ranking,
        )
