"""Serviço de consulta de CEP (ViaCEP), com tolerância a indisponibilidade."""
from __future__ import annotations

import re

import httpx

from app.models.endereco import EnderecoCep

_CEP_RE = re.compile(r"^\d{5}-?\d{3}$")


def normalizar_cep(cep: str) -> str:
    """Normaliza o CEP para o formato 00000-000."""
    digitos = re.sub(r"\D", "", cep)
    if len(digitos) != 8:
        return cep
    return f"{digitos[:5]}-{digitos[5:]}"


def consultar_cep(cep: str) -> EnderecoCep | None:
    """Consulta o ViaCEP e devolve um EnderecoCep preenchido.

    Se o serviço estiver indisponível (ex.: ambiente sem internet) ou o CEP
    for inválido, devolve um endereço apenas com o CEP, sem quebrar o fluxo
    de cadastro.
    """
    cep_norm = normalizar_cep(cep)
    if not _CEP_RE.match(cep_norm):
        return None

    endereco = EnderecoCep(cep=cep_norm)
    try:
        digitos = cep_norm.replace("-", "")
        resp = httpx.get(f"https://viacep.com.br/ws/{digitos}/json/", timeout=3.0)
        if resp.status_code == 200:
            dados = resp.json()
            if not dados.get("erro"):
                endereco.logradouro = dados.get("logradouro")
                endereco.bairro = dados.get("bairro")
                endereco.cidade = dados.get("localidade")
                endereco.estado = dados.get("uf")
    except (httpx.HTTPError, ValueError):
        # Offline ou resposta inválida: mantém apenas o CEP.
        pass
    return endereco
