"""Schemas Pydantic para FUNCIONARIO."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class FuncionarioCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    senha: str = Field(..., min_length=6, max_length=72)
    cargo: str = Field("Vendedor", max_length=50)


class FuncionarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_funcionario: int
    nome: str
    email: EmailStr
    cargo: str
