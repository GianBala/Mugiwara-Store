"""Rotas de CLIENTE: perfil do cliente autenticado."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import RecursoNaoEncontrado
from app.deps import requer_cliente
from app.repositories.cliente_repository import ClienteRepository
from app.routers.auth import _cliente_para_out
from app.schemas.auth import UsuarioAutenticado
from app.schemas.cliente import ClienteOut

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/me", response_model=ClienteOut)
def meu_perfil(
    db: Session = Depends(get_db),
    usuario: UsuarioAutenticado = Depends(requer_cliente),
) -> ClienteOut:
    """CA-03: cliente visualiza o próprio perfil."""
    cliente = ClienteRepository(db).obter(usuario.uid)
    if not cliente:
        raise RecursoNaoEncontrado("Cliente não encontrado")
    return _cliente_para_out(cliente)
