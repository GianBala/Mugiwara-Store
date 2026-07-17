"""Testes de PEDIDO — cobre CV-03, CV-05 e CA-04."""
from __future__ import annotations

import pytest

from app.models.produto import Produto


@pytest.fixture()
def token_cliente(client, cliente_elegivel) -> str:
    return client.post(
        "/api/auth/login", data={"username": "luffy@mugiwara.com", "password": "senha123"}
    ).json()["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ---- CA-04: compra completa ----
def test_ca04_cliente_finaliza_compra(client, token_cliente, produto):
    r = client.post(
        "/api/pedidos",
        json={"forma_pagamento": "PIX", "itens": [{"id_produto": produto.id_produto, "quantidade": 2}]},
        headers=_auth(token_cliente),
    )
    assert r.status_code == 201, r.text
    pedido = r.json()
    assert pedido["forma_pagamento"] == "PIX"
    assert len(pedido["itens"]) == 1

    # pedido aparece no histórico
    hist = client.get("/api/pedidos/meus", headers=_auth(token_cliente))
    assert hist.status_code == 200
    assert len(hist.json()) == 1


def test_ca04_compra_baixa_estoque(client, token_cliente, produto, db_session):
    client.post(
        "/api/pedidos",
        json={"forma_pagamento": "PIX", "itens": [{"id_produto": produto.id_produto, "quantidade": 3}]},
        headers=_auth(token_cliente),
    )
    atualizado = db_session.get(Produto, produto.id_produto)
    db_session.refresh(atualizado)
    assert atualizado.quantidade_estoque == 7  # 10 - 3


# ---- CV-03: controle de estoque ----
def test_cv03_estoque_insuficiente_rejeitado(client, token_cliente, produto):
    r = client.post(
        "/api/pedidos",
        json={"forma_pagamento": "PIX", "itens": [{"id_produto": produto.id_produto, "quantidade": 999}]},
        headers=_auth(token_cliente),
    )
    assert r.status_code == 422
    assert "estoque insuficiente" in r.json()["detail"].lower()


# ---- CV-05: integridade referencial ----
def test_cv05_pedido_com_produto_inexistente_rejeitado(client, token_cliente):
    r = client.post(
        "/api/pedidos",
        json={"forma_pagamento": "PIX", "itens": [{"id_produto": 99999, "quantidade": 1}]},
        headers=_auth(token_cliente),
    )
    assert r.status_code == 404


def test_cv04_compra_exige_autenticacao(client, produto):
    r = client.post(
        "/api/pedidos",
        json={"forma_pagamento": "PIX", "itens": [{"id_produto": produto.id_produto, "quantidade": 1}]},
    )
    assert r.status_code == 401
