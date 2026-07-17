"""Dependências compartilhadas: autenticação e autorização por perfil."""
from __future__ import annotations

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import NaoAutorizado, Proibido
from app.core.security import decodificar_token
from app.schemas.auth import UsuarioAutenticado

# auto_error=False para podermos lançar nossa própria exceção 401 padronizada.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)


def get_usuario_atual(token: str | None = Depends(oauth2_scheme)) -> UsuarioAutenticado:
    """Extrai e valida o usuário a partir do JWT (CV-04: 401 sem token válido)."""
    if not token:
        raise NaoAutorizado("Token de autenticação ausente")
    payload = decodificar_token(token)
    if not payload:
        raise NaoAutorizado("Token inválido ou expirado")
    return UsuarioAutenticado(
        uid=int(payload.get("uid")),
        email=payload.get("sub"),
        role=payload.get("role"),
        nome=payload.get("sub"),
    )


def requer_funcionario(
    usuario: UsuarioAutenticado = Depends(get_usuario_atual),
) -> UsuarioAutenticado:
    """CV-04: rotas restritas a funcionários retornam 403 para outros perfis."""
    if usuario.role != "funcionario":
        raise Proibido("Acesso restrito a funcionários")
    return usuario


def requer_cliente(
    usuario: UsuarioAutenticado = Depends(get_usuario_atual),
) -> UsuarioAutenticado:
    if usuario.role != "cliente":
        raise Proibido("Acesso restrito a clientes")
    return usuario
