"""Repositório de acesso a dados de CLIENTE e endereço."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.models.endereco import EnderecoCep


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def obter(self, id_cliente: int) -> Cliente | None:
        return self.db.get(Cliente, id_cliente)

    def obter_por_email(self, email: str) -> Cliente | None:
        stmt = select(Cliente).where(Cliente.email == email)
        return self.db.scalars(stmt).first()

    def criar(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.flush()
        return cliente

    # ---- Endereço (CEP) ----
    def obter_endereco(self, cep: str) -> EnderecoCep | None:
        return self.db.get(EnderecoCep, cep)

    def salvar_endereco(self, endereco: EnderecoCep) -> EnderecoCep:
        existente = self.db.get(EnderecoCep, endereco.cep)
        if existente:
            return existente
        self.db.add(endereco)
        self.db.flush()
        return endereco
