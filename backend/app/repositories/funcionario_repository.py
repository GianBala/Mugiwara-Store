"""Repositório de acesso a dados de FUNCIONARIO."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.funcionario import Funcionario


class FuncionarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def obter(self, id_funcionario: int) -> Funcionario | None:
        return self.db.get(Funcionario, id_funcionario)

    def obter_por_email(self, email: str) -> Funcionario | None:
        stmt = select(Funcionario).where(Funcionario.email == email)
        return self.db.scalars(stmt).first()

    def criar(self, funcionario: Funcionario) -> Funcionario:
        self.db.add(funcionario)
        self.db.flush()
        return funcionario
