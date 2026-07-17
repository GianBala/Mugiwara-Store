"""Ponto de entrada da API da Mugiwara Store (FastAPI)."""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import DomainError
from app.routers import auth, clientes, pedidos, produtos, relatorios, uploads

# Garante que os models sejam registrados na metadata.
import app.models  # noqa: F401

STATIC_DIR = Path(__file__).resolve().parent / "static"
(STATIC_DIR / "uploads").mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas caso ainda não existam (útil em execução local sem Docker).
    # Em produção (Docker), o esquema completo — incluindo VIEW e PROCEDURE —
    # é criado pelo db/init.sql. create_all usa checkfirst e é idempotente.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API do e-commerce temático One Piece — Mugiwara Store.",
    lifespan=lifespan,
)

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Arquivos estáticos (imagens de produtos) ----
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ---- Tratamento centralizado de erros de domínio ----
@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.mensagem})


# ---- Rotas ----
prefix = settings.API_V1_PREFIX
app.include_router(auth.router, prefix=prefix)
app.include_router(produtos.router, prefix=prefix)
app.include_router(pedidos.router, prefix=prefix)
app.include_router(clientes.router, prefix=prefix)
app.include_router(relatorios.router, prefix=prefix)
app.include_router(uploads.router, prefix=prefix)


@app.get("/", tags=["Health"])
def raiz() -> dict[str, str]:
    return {"aplicacao": settings.PROJECT_NAME, "status": "online", "docs": "/docs"}


@app.get(f"{prefix}/health", tags=["Health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
