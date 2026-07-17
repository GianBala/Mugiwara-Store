"""Funções de segurança: hashing de senhas (bcrypt) e emissão/validação de JWT."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


# ---------------------------------------------------------------------------
#  Senhas — bcrypt (resistente a força bruta)
# ---------------------------------------------------------------------------
def hash_password(senha: str) -> str:
    """Gera o hash bcrypt de uma senha em texto puro."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(senha: str, senha_hash: str) -> bool:
    """Confere se a senha em texto puro corresponde ao hash armazenado."""
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# ---------------------------------------------------------------------------
#  JWT — tokens de acesso
# ---------------------------------------------------------------------------
def criar_access_token(subject: str, role: str, uid: int) -> str:
    """Cria um JWT assinado contendo identidade e perfil do usuário.

    Args:
        subject: e-mail do usuário (claim `sub`).
        role: perfil ('cliente' ou 'funcionario').
        uid: identificador numérico do usuário.
    """
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "uid": uid,
        "exp": expira,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decodificar_token(token: str) -> dict[str, Any] | None:
    """Valida e decodifica um JWT; retorna o payload ou None se inválido/expirado."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
