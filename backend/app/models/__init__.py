"""Models SQLAlchemy da Mugiwara Store.

Importados aqui para que `Base.metadata` conheça todas as tabelas
(usado por `create_all` em testes).
"""
from app.models.endereco import EnderecoCep
from app.models.produto import Produto
from app.models.cliente import Cliente, ClienteTelefone
from app.models.funcionario import Funcionario
from app.models.pedido import Pedido, ItemPedido

__all__ = [
    "EnderecoCep",
    "Produto",
    "Cliente",
    "ClienteTelefone",
    "Funcionario",
    "Pedido",
    "ItemPedido",
]
