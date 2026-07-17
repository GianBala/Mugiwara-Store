"""Testes de autenticação e cadastro — cobre CV-04, CV-06 e CA-02/CA-03."""
from __future__ import annotations


def _cadastro(**over) -> dict:
    base = {
        "nome": "Nico Robin",
        "email": "robin@mugiwara.com",
        "senha": "senha123",
        "torce_flamengo": True,
    }
    base.update(over)
    return base


# ---- CA-02: cadastro de cliente ----
def test_ca02_cadastro_cliente_sucesso(client):
    r = client.post("/api/auth/register", json=_cadastro())
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["email"] == "robin@mugiwara.com"
    assert body["elegivel_desconto"] is True  # torce_flamengo


def test_ca02_login_apos_cadastro(client):
    client.post("/api/auth/register", json=_cadastro())
    r = client.post(
        "/api/auth/login", data={"username": "robin@mugiwara.com", "password": "senha123"}
    )
    assert r.status_code == 200
    assert r.json()["role"] == "cliente"


# ---- CV-06: unicidade de e-mail (entre clientes e funcionários) ----
def test_cv06_email_duplicado_cliente_rejeitado(client):
    assert client.post("/api/auth/register", json=_cadastro()).status_code == 201
    r = client.post("/api/auth/register", json=_cadastro(nome="Outro"))
    assert r.status_code == 409


def test_cv06_email_igual_ao_funcionario_rejeitado(client, funcionario):
    # funcionário nami@mugiwara.com já existe (fixture)
    r = client.post("/api/auth/register", json=_cadastro(email="nami@mugiwara.com"))
    assert r.status_code == 409


# ---- CV-04: autenticação ----
def test_cv04_credenciais_invalidas_retorna_401(client, funcionario):
    r = client.post(
        "/api/auth/login", data={"username": "nami@mugiwara.com", "password": "errada"}
    )
    assert r.status_code == 401


def test_cv04_rota_protegida_sem_token_retorna_401(client):
    assert client.get("/api/clientes/me").status_code == 401


def test_cv04_funcionario_acessa_relatorio_cliente_nao(client, funcionario, cliente_elegivel):
    # funcionário -> 200
    tok_f = client.post(
        "/api/auth/login", data={"username": "nami@mugiwara.com", "password": "senha123"}
    ).json()["access_token"]
    assert client.get(
        "/api/relatorios/estoque", headers={"Authorization": f"Bearer {tok_f}"}
    ).status_code == 200

    # cliente -> 403
    tok_c = client.post(
        "/api/auth/login", data={"username": "luffy@mugiwara.com", "password": "senha123"}
    ).json()["access_token"]
    assert client.get(
        "/api/relatorios/estoque", headers={"Authorization": f"Bearer {tok_c}"}
    ).status_code == 403


# ---- CA-03: perfil do cliente ----
def test_ca03_cliente_ve_proprio_perfil(client):
    client.post("/api/auth/register", json=_cadastro())
    tok = client.post(
        "/api/auth/login", data={"username": "robin@mugiwara.com", "password": "senha123"}
    ).json()["access_token"]
    r = client.get("/api/clientes/me", headers={"Authorization": f"Bearer {tok}"})
    assert r.status_code == 200
    assert r.json()["nome"] == "Nico Robin"
