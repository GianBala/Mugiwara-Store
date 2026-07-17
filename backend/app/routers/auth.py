"""Rotas de autenticação e cadastro."""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.deps import get_usuario_atual, requer_funcionario
from app.schemas.auth import Token, UsuarioAutenticado
from app.schemas.cliente import ClienteCreate, ClienteOut
from app.schemas.funcionario import FuncionarioCreate, FuncionarioOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """Autentica cliente ou funcionário e devolve um token JWT."""
    return AuthService(db).autenticar(form.username, form.password)


@router.post("/register", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def registrar_cliente(dados: ClienteCreate, db: Session = Depends(get_db)) -> ClienteOut:
    """CA-02: cadastro público de cliente (com endereço via CEP)."""
    cliente = AuthService(db).registrar_cliente(dados)
    return _cliente_para_out(cliente)


@router.post(
    "/funcionarios",
    response_model=FuncionarioOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(requer_funcionario)],
)
def registrar_funcionario(dados: FuncionarioCreate, db: Session = Depends(get_db)) -> FuncionarioOut:
    """Cadastro de novo funcionário (restrito a funcionários)."""
    return AuthService(db).registrar_funcionario(dados)


@router.get("/me", response_model=UsuarioAutenticado)
def me(usuario: UsuarioAutenticado = Depends(get_usuario_atual)) -> UsuarioAutenticado:
    """Devolve os dados do usuário autenticado (a partir do token)."""
    return usuario


# Reaproveitado pelo router de clientes.
def _cliente_para_out(cliente) -> ClienteOut:
    from app.schemas.cliente import EnderecoOut

    return ClienteOut(
        id_cliente=cliente.id_cliente,
        nome=cliente.nome,
        email=cliente.email,
        cep=cliente.cep,
        numero_endereco=cliente.numero_endereco,
        complemento_endereco=cliente.complemento_endereco,
        torce_flamengo=cliente.torce_flamengo,
        assiste_one_piece=cliente.assiste_one_piece,
        natural_de_sousa=cliente.natural_de_sousa,
        elegivel_desconto=cliente.elegivel_desconto,
        endereco=EnderecoOut.model_validate(cliente.endereco) if getattr(cliente, "endereco", None) else None,
        telefones=[t.telefone for t in cliente.telefones],
    )
