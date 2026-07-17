"""Regras de autenticação e cadastro de usuários (cliente e funcionário)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import ConflitoError, NaoAutorizado
from app.core.security import criar_access_token, hash_password, verify_password
from app.models.cliente import Cliente, ClienteTelefone
from app.models.funcionario import Funcionario
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.funcionario_repository import FuncionarioRepository
from app.schemas.auth import Token
from app.schemas.cliente import ClienteCreate
from app.schemas.funcionario import FuncionarioCreate
from app.services import cep_service


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.clientes = ClienteRepository(db)
        self.funcionarios = FuncionarioRepository(db)

    # ---------------------------------------------------------------
    #  Cadastro
    # ---------------------------------------------------------------
    def _garantir_email_unico(self, email: str) -> None:
        """CV-06: e-mail único entre clientes E funcionários."""
        if self.clientes.obter_por_email(email) or self.funcionarios.obter_por_email(email):
            raise ConflitoError("Já existe um usuário cadastrado com este e-mail")

    def registrar_cliente(self, dados: ClienteCreate) -> Cliente:
        self._garantir_email_unico(dados.email)

        cep_norm: str | None = None
        if dados.cep:
            endereco = cep_service.consultar_cep(dados.cep)
            if endereco:
                self.clientes.salvar_endereco(endereco)
                cep_norm = endereco.cep

        cliente = Cliente(
            nome=dados.nome,
            email=dados.email,
            senha_hash=hash_password(dados.senha),
            numero_endereco=dados.numero_endereco,
            complemento_endereco=dados.complemento_endereco,
            cep=cep_norm,
            torce_flamengo=dados.torce_flamengo,
            assiste_one_piece=dados.assiste_one_piece,
            natural_de_sousa=dados.natural_de_sousa,
        )
        for tel in dados.telefones:
            if tel.strip():
                cliente.telefones.append(ClienteTelefone(telefone=tel.strip()))

        self.clientes.criar(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def registrar_funcionario(self, dados: FuncionarioCreate) -> Funcionario:
        self._garantir_email_unico(dados.email)
        funcionario = Funcionario(
            nome=dados.nome,
            email=dados.email,
            senha_hash=hash_password(dados.senha),
            cargo=dados.cargo,
        )
        self.funcionarios.criar(funcionario)
        self.db.commit()
        self.db.refresh(funcionario)
        return funcionario

    # ---------------------------------------------------------------
    #  Login
    # ---------------------------------------------------------------
    def autenticar(self, email: str, senha: str) -> Token:
        """Autentica em ambas as tabelas; funcionário tem precedência."""
        funcionario = self.funcionarios.obter_por_email(email)
        if funcionario and verify_password(senha, funcionario.senha_hash):
            token = criar_access_token(email, "funcionario", funcionario.id_funcionario)
            return Token(
                access_token=token, role="funcionario",
                nome=funcionario.nome, uid=funcionario.id_funcionario,
            )

        cliente = self.clientes.obter_por_email(email)
        if cliente and verify_password(senha, cliente.senha_hash):
            token = criar_access_token(email, "cliente", cliente.id_cliente)
            return Token(
                access_token=token, role="cliente",
                nome=cliente.nome, uid=cliente.id_cliente,
            )

        raise NaoAutorizado("E-mail ou senha inválidos")
