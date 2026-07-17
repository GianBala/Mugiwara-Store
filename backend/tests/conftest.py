"""Configuração dos testes: banco SQLite em memória + TestClient.

Cada teste roda contra um banco limpo, isolado, sem necessidade de servidor
ou PostgreSQL em execução (conforme plano de testes da Atividade 03).
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.models.cliente import Cliente
from app.models.funcionario import Funcionario
from app.models.produto import Produto


@pytest.fixture()
def engine():
    eng = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Habilita verificação de chaves estrangeiras no SQLite.
    @event.listens_for(eng, "connect")
    def _fk_pragma(dbapi_conn, _):
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()

    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)


@pytest.fixture()
def db_session(engine):
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(engine):
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
#  Fixtures de dados / autenticação
# ---------------------------------------------------------------------------
@pytest.fixture()
def funcionario(db_session) -> Funcionario:
    f = Funcionario(
        nome="Nami",
        email="nami@mugiwara.com",
        senha_hash=hash_password("senha123"),
        cargo="Gerente de Vendas",
    )
    db_session.add(f)
    db_session.commit()
    db_session.refresh(f)
    return f


@pytest.fixture()
def cliente_elegivel(db_session) -> Cliente:
    """Cliente que assiste One Piece -> elegível a desconto."""
    c = Cliente(
        nome="Monkey D. Luffy",
        email="luffy@mugiwara.com",
        senha_hash=hash_password("senha123"),
        assiste_one_piece=True,
    )
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


@pytest.fixture()
def produto(db_session) -> Produto:
    p = Produto(
        nome="Action Figure Luffy Gear 5",
        descricao="Figura de colecionador",
        preco=100.00,
        quantidade_estoque=10,
        categoria="Action Figures",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


def _login(client, email: str, senha: str = "senha123") -> str:
    resp = client.post("/api/auth/login", data={"username": email, "password": senha})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@pytest.fixture()
def token_funcionario(client, funcionario) -> str:
    return _login(client, funcionario.email)


@pytest.fixture()
def auth_funcionario(token_funcionario) -> dict[str, str]:
    return {"Authorization": f"Bearer {token_funcionario}"}
