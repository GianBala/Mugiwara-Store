"""Rotas de PEDIDO: finalização de compra e histórico."""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import Proibido
from app.deps import get_usuario_atual, requer_cliente
from app.models.pedido import Pedido
from app.schemas.auth import UsuarioAutenticado
from app.schemas.pedido import ItemPedidoOut, PedidoCreate, PedidoOut
from app.services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def _pedido_para_out(pedido: Pedido) -> PedidoOut:
    return PedidoOut(
        id_pedido=pedido.id_pedido,
        data_pedido=pedido.data_pedido,
        forma_pagamento=pedido.forma_pagamento,
        status_pagamento=pedido.status_pagamento,
        valor_total=pedido.valor_total,
        id_cliente=pedido.id_cliente,
        id_funcionario=pedido.id_funcionario,
        itens=[
            ItemPedidoOut(
                id_produto=item.id_produto,
                nome_produto=item.produto.nome if item.produto else None,
                quantidade=item.quantidade,
                preco_unitario_na_venda=item.preco_unitario_na_venda,
            )
            for item in pedido.itens
        ],
    )


@router.post(
    "",
    response_model=PedidoOut,
    status_code=status.HTTP_201_CREATED,
)
def criar_pedido(
    dados: PedidoCreate,
    db: Session = Depends(get_db),
    usuario: UsuarioAutenticado = Depends(requer_cliente),
) -> PedidoOut:
    """CA-04: cliente autenticado finaliza a compra."""
    pedido = PedidoService(db).criar_pedido(usuario.uid, dados)
    return _pedido_para_out(pedido)


@router.get("/meus", response_model=list[PedidoOut])
def meus_pedidos(
    db: Session = Depends(get_db),
    usuario: UsuarioAutenticado = Depends(requer_cliente),
) -> list[PedidoOut]:
    """CA-03: histórico de pedidos do cliente autenticado."""
    pedidos = PedidoService(db).listar_por_cliente(usuario.uid)
    return [_pedido_para_out(p) for p in pedidos]


@router.get("/{id_pedido}", response_model=PedidoOut)
def obter_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    usuario: UsuarioAutenticado = Depends(get_usuario_atual),
) -> PedidoOut:
    pedido = PedidoService(db).obter(id_pedido)
    # Cliente só acessa os próprios pedidos; funcionário acessa qualquer um.
    if usuario.role == "cliente" and pedido.id_cliente != usuario.uid:
        raise Proibido("Você não tem acesso a este pedido")
    return _pedido_para_out(pedido)
