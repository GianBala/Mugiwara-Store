"""Models das entidades CLIENTE e CLIENTE_TELEFONE."""
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    numero_endereco: Mapped[str | None] = mapped_column(String(20))
    complemento_endereco: Mapped[str | None] = mapped_column(String(100))
    cep: Mapped[str | None] = mapped_column(String(9), ForeignKey("endereco_cep.cep"))
    torce_flamengo: Mapped[bool] = mapped_column(default=False, nullable=False)
    assiste_one_piece: Mapped[bool] = mapped_column(default=False, nullable=False)
    natural_de_sousa: Mapped[bool] = mapped_column(default=False, nullable=False)

    telefones: Mapped[list["ClienteTelefone"]] = relationship(
        back_populates="cliente", cascade="all, delete-orphan"
    )
    endereco = relationship("EnderecoCep", lazy="joined")

    @property
    def elegivel_desconto(self) -> bool:
        """Cliente elegível a desconto se atender a pelo menos um critério."""
        return self.torce_flamengo or self.assiste_one_piece or self.natural_de_sousa


class ClienteTelefone(Base):
    __tablename__ = "cliente_telefone"

    id_cliente: Mapped[int] = mapped_column(
        Integer, ForeignKey("cliente.id_cliente", ondelete="CASCADE"), primary_key=True
    )
    telefone: Mapped[str] = mapped_column(String(20), primary_key=True)

    cliente: Mapped["Cliente"] = relationship(back_populates="telefones")
