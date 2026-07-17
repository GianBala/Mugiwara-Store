"""Testes de desconto e relatórios — cobre CV-07, CV-08 e CA-06."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.models.cliente import Cliente
from app.core.security import hash_password


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def cliente_sem_desconto(db_session) -> Cliente:
    c = Cliente(
        nome="Buggy",
        email="buggy@mugiwara.com",
        senha_hash=hash_password("senha123"),
    )
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


# ---- CV-07: aplicação de desconto ----
def test_cv07_cliente_elegivel_recebe_desconto(client, cliente_elegivel, produto):
    tok = client.post(
        "/api/auth/login", data={"username": "luffy@mugiwara.com", "password": "senha123"}
    ).json()["access_token"]
    r = client.post(
        "/api/pedidos",
        json={"forma_pagamento": "PIX", "itens": [{"id_produto": produto.id_produto, "quantidade": 2}]},
        headers=_auth(tok),
    )
    assert r.status_code == 201
    # 2 x 100 = 200; desconto de 10% => 180
    assert Decimal(str(r.json()["valor_total"])) == Decimal("180.00")


def test_cv07_cliente_sem_criterio_paga_valor_cheio(client, cliente_sem_desconto, produto):
    tok = client.post(
        "/api/auth/login", data={"username": "buggy@mugiwara.com", "password": "senha123"}
    ).json()["access_token"]
    r = client.post(
        "/api/pedidos",
        json={"forma_pagamento": "PIX", "itens": [{"id_produto": produto.id_produto, "quantidade": 2}]},
        headers=_auth(tok),
    )
    assert r.status_code == 201
    assert Decimal(str(r.json()["valor_total"])) == Decimal("200.00")


# ---- CV-08: relatório de estoque baixo ----
def test_cv08_estoque_baixo_lista_apenas_menor_que_5(client, auth_funcionario, db_session):
    from app.models.produto import Produto

    db_session.add_all([
        Produto(nome="Baixo A", preco=10, quantidade_estoque=2, categoria="X"),
        Produto(nome="Baixo B", preco=10, quantidade_estoque=4, categoria="X"),
        Produto(nome="Ok", preco=10, quantidade_estoque=10, categoria="X"),
    ])
    db_session.commit()

    r = client.get("/api/relatorios/estoque-baixo", headers=auth_funcionario)
    assert r.status_code == 200
    nomes = {p["nome"] for p in r.json()}
    assert nomes == {"Baixo A", "Baixo B"}
    assert all(p["quantidade_estoque"] < 5 for p in r.json())


def test_cv08_estoque_baixo_restrito_a_funcionario(client):
    assert client.get("/api/relatorios/estoque-baixo").status_code == 401


# ---- CA-06: relatório mensal de vendas ----
def test_ca06_relatorio_mensal_com_ranking(client, cliente_elegivel, produto, auth_funcionario):
    tok = client.post(
        "/api/auth/login", data={"username": "luffy@mugiwara.com", "password": "senha123"}
    ).json()["access_token"]
    client.post(
        "/api/pedidos",
        json={"forma_pagamento": "PIX", "itens": [{"id_produto": produto.id_produto, "quantidade": 1}]},
        headers=_auth(tok),
    )
    agora = datetime.now(timezone.utc)
    r = client.get(
        "/api/relatorios/vendas",
        params={"ano": agora.year, "mes": agora.month},
        headers=auth_funcionario,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["total_pedidos"] == 1
    assert Decimal(str(body["total_vendido"])) == Decimal("90.00")  # 100 - 10%
