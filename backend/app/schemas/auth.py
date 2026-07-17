"""Schemas Pydantic de autenticação."""
from __future__ import annotations

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    nome: str
    uid: int


class UsuarioAutenticado(BaseModel):
    """Representa o usuário extraído do token JWT."""

    uid: int
    email: str
    role: str  # 'cliente' | 'funcionario'
    nome: str
