"""Testes de PRODUTO — cobre CV-01, CV-02, CV-04 e CA-01."""
from __future__ import annotations


def _payload_produto(**over) -> dict:
    base = {
        "nome": "Réplica Espada Wado Ichimonji",
        "descricao": "Katana do Zoro",
        "preco": 599.90,
        "quantidade_estoque": 5,
        "categoria": "Réplicas",
    }
    base.update(over)
    return base


# ---- CV-01: CRUD completo de produtos ----
def test_cv01_funcionario_cria_lista_edita_remove(client, auth_funcionario):
    # criar
    r = client.post("/api/produtos", json=_payload_produto(), headers=auth_funcionario)
    assert r.status_code == 201, r.text
    pid = r.json()["id_produto"]

    # listar (público)
    r = client.get("/api/produtos")
    assert r.status_code == 200
    assert any(p["id_produto"] == pid for p in r.json())

    # editar
    r = client.put(f"/api/produtos/{pid}", json={"preco": 499.90}, headers=auth_funcionario)
    assert r.status_code == 200
    assert float(r.json()["preco"]) == 499.90

    # remover
    r = client.delete(f"/api/produtos/{pid}", headers=auth_funcionario)
    assert r.status_code == 204
    assert client.get(f"/api/produtos/{pid}").status_code == 404


def test_cv01_produto_sem_nome_ou_categoria_rejeitado(client, auth_funcionario):
    r = client.post("/api/produtos", json=_payload_produto(nome=""), headers=auth_funcionario)
    assert r.status_code == 422
    r = client.post("/api/produtos", json={"nome": "X", "preco": 10}, headers=auth_funcionario)
    assert r.status_code == 422  # sem categoria


# ---- CV-02: validação de preço ----
def test_cv02_preco_zero_ou_negativo_rejeitado(client, auth_funcionario):
    r = client.post("/api/produtos", json=_payload_produto(preco=0), headers=auth_funcionario)
    assert r.status_code == 422
    r = client.post("/api/produtos", json=_payload_produto(preco=-10), headers=auth_funcionario)
    assert r.status_code == 422


# ---- CV-04: CRUD de produto é restrito a funcionários ----
def test_cv04_criar_produto_sem_token_retorna_401(client):
    r = client.post("/api/produtos", json=_payload_produto())
    assert r.status_code == 401


def test_cv04_cliente_nao_pode_criar_produto_403(client, cliente_elegivel):
    login = client.post(
        "/api/auth/login", data={"username": "luffy@mugiwara.com", "password": "senha123"}
    )
    token = login.json()["access_token"]
    r = client.post(
        "/api/produtos",
        json=_payload_produto(),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 403


# ---- CA-01: navegação pública com busca e filtros ----
def test_ca01_visitante_navega_busca_e_filtra(client, auth_funcionario):
    client.post("/api/produtos", json=_payload_produto(nome="Chapéu de Palha", categoria="Vestuário", preco=100), headers=auth_funcionario)
    client.post("/api/produtos", json=_payload_produto(nome="Pôster Sunny", categoria="Pôsteres", preco=50), headers=auth_funcionario)

    # sem login
    assert len(client.get("/api/produtos").json()) == 2
    # busca por nome
    assert len(client.get("/api/produtos", params={"busca": "Chapéu"}).json()) == 1
    # filtro por categoria
    assert len(client.get("/api/produtos", params={"categoria": "Pôsteres"}).json()) == 1
    # filtro por faixa de preço
    assert len(client.get("/api/produtos", params={"preco_max": 60}).json()) == 1
