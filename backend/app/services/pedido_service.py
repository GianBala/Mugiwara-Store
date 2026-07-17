"""Regras de negócio de PEDIDO: finalização de compra atômica.

Espelha, na camada de aplicação, a lógica da stored procedure
`criar_pedido_completo` (definida em db/init.sql): valida o estoque, aplica o
desconto conforme o perfil do cliente, cria o pedido e seus itens e baixa o
estoque — tudo dentro de uma única transação.
"""
from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import RecursoNaoEncontrado, RegraNegocioError
from app.models.pedido import ItemPedido, Pedido
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.produto_repository import ProdutoRepository
from app.schemas.pedido import PedidoCreate

CENTAVO = Decimal("0.01")


class PedidoService:
    def __init__(self, db: Session):
        self.db = db
        self.pedidos = PedidoRepository(db)
        self.produtos = ProdutoRepository(db)
        self.clientes = ClienteRepository(db)

    def criar_pedido(self, id_cliente: int, dados: PedidoCreate) -> Pedido:
        cliente = self.clientes.obter(id_cliente)
        if not cliente:
            raise RecursoNaoEncontrado(f"Cliente {id_cliente} não encontrado")

        # Consolida quantidades por produto (evita itens duplicados no payload).
        quantidades: dict[int, int] = {}
        for item in dados.itens:
            quantidades[item.id_produto] = quantidades.get(item.id_produto, 0) + item.quantidade

        subtotal = Decimal("0.00")
        itens_pedido: list[ItemPedido] = []

        for id_produto, quantidade in quantidades.items():
            produto = self.produtos.obter_para_atualizar(id_produto)
            if not produto:
                raise RecursoNaoEncontrado(f"Produto {id_produto} não encontrado")
            # CV-03: rejeita compra com quantidade acima do estoque disponível.
            if produto.quantidade_estoque < quantidade:
                raise RegraNegocioError(
                    f"Estoque insuficiente para '{produto.nome}' "
                    f"(disponível: {produto.quantidade_estoque}, solicitado: {quantidade})"
                )
            subtotal += produto.preco * quantidade
            itens_pedido.append(
                ItemPedido(
                    id_produto=produto.id_produto,
                    quantidade=quantidade,
                    preco_unitario_na_venda=produto.preco,
                )
            )
            produto.quantidade_estoque -= quantidade

        # CV-07: desconto para clientes elegíveis.
        valor_total = subtotal
        if cliente.elegivel_desconto:
            fator = Decimal("1") - Decimal(str(settings.DESCONTO_PERCENTUAL))
            valor_total = (subtotal * fator).quantize(CENTAVO)

        pedido = Pedido(
            forma_pagamento=dados.forma_pagamento,
            status_pagamento="APROVADO",
            valor_total=valor_total,
            id_cliente=id_cliente,
            id_funcionario=dados.id_funcionario,
        )
        pedido.itens = itens_pedido
        self.pedidos.criar(pedido)
        self.db.commit()
        return self.pedidos.obter(pedido.id_pedido)

    def listar_por_cliente(self, id_cliente: int) -> list[Pedido]:
        return self.pedidos.listar_por_cliente(id_cliente)

    def obter(self, id_pedido: int) -> Pedido:
        pedido = self.pedidos.obter(id_pedido)
        if not pedido:
            raise RecursoNaoEncontrado(f"Pedido {id_pedido} não encontrado")
        return pedido
