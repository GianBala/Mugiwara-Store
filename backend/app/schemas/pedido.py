"""Schemas Pydantic para PEDIDO e ITEM_PEDIDO."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ItemPedidoIn(BaseModel):
    id_produto: int
    quantidade: int = Field(..., gt=0)


class PedidoCreate(BaseModel):
    """Payload de finalização de compra pelo cliente autenticado."""

    forma_pagamento: str = Field(..., min_length=1, max_length=50)
    itens: list[ItemPedidoIn] = Field(..., min_length=1)
    id_funcionario: int | None = None


class ItemPedidoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_produto: int
    nome_produto: str | None = None
    quantidade: int
    preco_unitario_na_venda: Decimal


class PedidoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_pedido: int
    data_pedido: datetime
    forma_pagamento: str
    status_pagamento: str
    valor_total: Decimal
    id_cliente: int
    id_funcionario: int | None = None
    itens: list[ItemPedidoOut] = Field(default_factory=list)
