"""Rota de upload de imagens de produto (CA-05), restrita a funcionários."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from app.core.exceptions import RegraNegocioError
from app.deps import requer_funcionario

router = APIRouter(prefix="/uploads", tags=["Uploads"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

EXTENSOES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
TAMANHO_MAX = 5 * 1024 * 1024  # 5 MB


@router.post("/imagem", dependencies=[Depends(requer_funcionario)])
async def upload_imagem(arquivo: UploadFile = File(...)) -> dict[str, str]:
    """Recebe uma imagem, salva localmente e devolve a URL relativa."""
    ext = Path(arquivo.filename or "").suffix.lower()
    if ext not in EXTENSOES_PERMITIDAS:
        raise RegraNegocioError(
            f"Formato não suportado. Use: {', '.join(sorted(EXTENSOES_PERMITIDAS))}"
        )

    conteudo = await arquivo.read()
    if len(conteudo) > TAMANHO_MAX:
        raise RegraNegocioError("Arquivo muito grande (máximo 5 MB)")

    nome_base = re.sub(r"[^a-zA-Z0-9_-]", "", Path(arquivo.filename or "img").stem)[:40]
    nome_arquivo = f"{nome_base}_{uuid.uuid4().hex[:8]}{ext}"
    destino = UPLOAD_DIR / nome_arquivo
    destino.write_bytes(conteudo)

    return {"url": f"/static/uploads/{nome_arquivo}"}
