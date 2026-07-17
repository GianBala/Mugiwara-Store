import { defineStore } from 'pinia'
import type { ItemCarrinho, Produto } from '@/types'

interface CartState {
  itens: ItemCarrinho[]
}

const STORAGE_KEY = 'mugiwara_cart'

function carregar(): ItemCarrinho[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  } catch {
    return []
  }
}

export const useCartStore = defineStore('cart', {
  state: (): CartState => ({
    itens: carregar(),
  }),
  getters: {
    quantidadeTotal: (s) => s.itens.reduce((acc, i) => acc + i.quantidade, 0),
    subtotal: (s) => s.itens.reduce((acc, i) => acc + i.produto.preco * i.quantidade, 0),
    vazio: (s) => s.itens.length === 0,
  },
  actions: {
    persistir() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.itens))
    },
    adicionar(produto: Produto, quantidade = 1) {
      const existente = this.itens.find((i) => i.produto.id_produto === produto.id_produto)
      const noCarrinho = existente ? existente.quantidade : 0
      const desejado = noCarrinho + quantidade
      // Não permite exceder o estoque disponível.
      const permitido = Math.min(desejado, produto.quantidade_estoque)
      if (existente) {
        existente.quantidade = permitido
        existente.produto = produto
      } else if (permitido > 0) {
        this.itens.push({ produto, quantidade: permitido })
      }
      this.persistir()
    },
    definirQuantidade(idProduto: number, quantidade: number) {
      const item = this.itens.find((i) => i.produto.id_produto === idProduto)
      if (!item) return
      item.quantidade = Math.max(1, Math.min(quantidade, item.produto.quantidade_estoque))
      this.persistir()
    },
    remover(idProduto: number) {
      this.itens = this.itens.filter((i) => i.produto.id_produto !== idProduto)
      this.persistir()
    },
    limpar() {
      this.itens = []
      this.persistir()
    },
  },
})
