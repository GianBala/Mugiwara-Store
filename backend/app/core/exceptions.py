"""Exceções de domínio da aplicação.

São convertidas em respostas HTTP apropriadas por handlers registrados
em `app.main`, mantendo a camada de serviço livre de detalhes de HTTP.
"""
from __future__ import annotations


class DomainError(Exception):
    """Erro de regra de negócio (base)."""

    status_code = 400

    def __init__(self, mensagem: str):
        self.mensagem = mensagem
        super().__init__(mensagem)


class RecursoNaoEncontrado(DomainError):
    status_code = 404


class ConflitoError(DomainError):
    """Violação de unicidade / conflito de estado (ex.: e-mail já cadastrado)."""

    status_code = 409


class RegraNegocioError(DomainError):
    """Violação de regra de negócio (ex.: estoque insuficiente)."""

    status_code = 422


class NaoAutorizado(DomainError):
    status_code = 401


class Proibido(DomainError):
    status_code = 403
