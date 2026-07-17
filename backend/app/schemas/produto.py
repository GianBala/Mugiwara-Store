"""Schemas Pydantic para PRODUTO."""
from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    descricao: str | None = None
    # CV-02: preço deve ser estritamente maior que zero.
    preco: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    quantidade_estoque: int = Field(0, ge=0)
    categoria: str = Field(..., min_length=1, max_length=50)
    fabricado_em_mari: bool = False
    imagem: str | None = Field(None, max_length=255)


class ProdutoCreate(ProdutoBase):
    """Payload de criação de produto."""


class ProdutoUpdate(BaseModel):
    """Payload de atualização parcial de produto."""

    nome: str | None = Field(None, min_length=1, max_length=100)
    descricao: str | None = None
    preco: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    quantidade_estoque: int | None = Field(None, ge=0)
    categoria: str | None = Field(None, min_length=1, max_length=50)
    fabricado_em_mari: bool | None = None
    imagem: str | None = Field(None, max_length=255)


class ProdutoOut(ProdutoBase):
    model_config = ConfigDict(from_attributes=True)

    id_produto: int
