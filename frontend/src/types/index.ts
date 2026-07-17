export interface Produto {
  id_produto: number
  nome: string
  descricao: string | null
  preco: number
  quantidade_estoque: number
  categoria: string
  fabricado_em_mari: boolean
  imagem: string | null
}

export interface ProdutoInput {
  nome: string
  descricao?: string | null
  preco: number
  quantidade_estoque: number
  categoria: string
  fabricado_em_mari: boolean
  imagem?: string | null
}

export interface Endereco {
  cep: string
  logradouro: string | null
  bairro: string | null
  cidade: string | null
  estado: string | null
}

export interface Cliente {
  id_cliente: number
  nome: string
  email: string
  cep: string | null
  numero_endereco: string | null
  complemento_endereco: string | null
  torce_flamengo: boolean
  assiste_one_piece: boolean
  natural_de_sousa: boolean
  elegivel_desconto: boolean
  endereco: Endereco | null
  telefones: string[]
}

export interface ItemPedido {
  id_produto: number
  nome_produto: string | null
  quantidade: number
  preco_unitario_na_venda: number
}

export interface Pedido {
  id_pedido: number
  data_pedido: string
  forma_pagamento: string
  status_pagamento: string
  valor_total: number
  id_cliente: number
  id_funcionario: number | null
  itens: ItemPedido[]
}

export interface TokenResposta {
  access_token: string
  token_type: string
  role: 'cliente' | 'funcionario'
  nome: string
  uid: number
}

export interface ResumoEstoque {
  total_produtos: number
  total_unidades: number
  valor_total_estoque: number
  produtos_estoque_baixo: number
}

export interface VendaPorVendedor {
  id_funcionario: number
  nome_vendedor: string
  cargo: string | null
  total_pedidos: number
  total_itens: number
  total_vendido: number
}

export interface RelatorioVendas {
  mes_referencia: string
  total_pedidos: number
  total_vendido: number
  ranking_vendedores: VendaPorVendedor[]
}

export interface ItemCarrinho {
  produto: Produto
  quantidade: number
}
