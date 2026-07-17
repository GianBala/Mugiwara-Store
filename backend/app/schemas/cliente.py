"""Schemas Pydantic para CLIENTE e endereço."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EnderecoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cep: str
    logradouro: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None


class ClienteCreate(BaseModel):
    """Cadastro público de cliente."""

    nome: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    senha: str = Field(..., min_length=6, max_length=72)
    cep: str | None = Field(None, max_length=9)
    numero_endereco: str | None = Field(None, max_length=20)
    complemento_endereco: str | None = Field(None, max_length=100)
    telefones: list[str] = Field(default_factory=list)
    torce_flamengo: bool = False
    assiste_one_piece: bool = False
    natural_de_sousa: bool = False


class ClienteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cliente: int
    nome: str
    email: EmailStr
    cep: str | None = None
    numero_endereco: str | None = None
    complemento_endereco: str | None = None
    torce_flamengo: bool
    assiste_one_piece: bool
    natural_de_sousa: bool
    elegivel_desconto: bool
    endereco: EnderecoOut | None = None
    telefones: list[str] = Field(default_factory=list)
