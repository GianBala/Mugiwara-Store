<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api, resolverImagem } from '@/api/client'
import { moeda, extrairErro } from '@/utils/format'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const cart = useCartStore()
const auth = useAuthStore()
const toast = useToastStore()
const router = useRouter()

const formaPagamento = ref('PIX')
const finalizando = ref(false)

const formas = [
  { valor: 'PIX', label: 'PIX', icone: '⚡' },
  { valor: 'CARTAO', label: 'Cartão', icone: '💳' },
  { valor: 'BOLETO', label: 'Boleto', icone: '🧾' },
]

// Estimativa de desconto (10% para nakamas elegíveis; confirmado no backend).
const clienteElegivel = ref<boolean | null>(null)
const descontoEstimado = computed(() => (clienteElegivel.value ? cart.subtotal * 0.1 : 0))
const totalEstimado = computed(() => cart.subtotal - descontoEstimado.value)

async function verificarElegibilidade() {
  if (!auth.ehCliente) return
  try {
    const { data } = await api.get('/clientes/me')
    clienteElegivel.value = data.elegivel_desconto
  } catch {
    clienteElegivel.value = false
  }
}
verificarElegibilidade()

async function finalizar() {
  if (!auth.ehCliente) {
    toast.erro('Faça login como cliente para finalizar a compra.')
    router.push({ name: 'login', query: { redirect: '/carrinho' } })
    return
  }
  finalizando.value = true
  try {
    const payload = {
      forma_pagamento: formaPagamento.value,
      itens: cart.itens.map((i) => ({ id_produto: i.produto.id_produto, quantidade: i.quantidade })),
    }
    const { data } = await api.post('/pedidos', payload)
    cart.limpar()
    toast.sucesso(`Pedido #${data.id_pedido} realizado com sucesso! 🏴‍☠️`)
    router.push({ name: 'pedidos' })
  } catch (e) {
    toast.erro(extrairErro(e, 'Não foi possível finalizar a compra.'))
  } finally {
    finalizando.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-10">
    <h1 class="font-display text-4xl text-ocean-900">Seu Carrinho</h1>

    <!-- Vazio -->
    <div v-if="cart.vazio" class="mt-12 flex flex-col items-center gap-4 text-center">
      <div class="grid h-24 w-24 place-items-center rounded-full bg-ocean-50 text-5xl">🛒</div>
      <p class="font-display text-2xl text-ocean-700">Seu porão está vazio</p>
      <p class="text-ocean-500">Adicione tesouros ao carrinho para zarpar.</p>
      <RouterLink :to="{ name: 'home' }" class="btn-treasure mt-2">Explorar catálogo</RouterLink>
    </div>

    <div v-else class="mt-8 grid gap-8 lg:grid-cols-[1fr_360px]">
      <!-- Itens -->
      <div class="space-y-4">
        <div v-for="item in cart.itens" :key="item.produto.id_produto"
          class="flex gap-4 rounded-2xl border border-ocean-100 bg-white p-4 shadow-card">
          <img :src="resolverImagem(item.produto.imagem)" :alt="item.produto.nome"
            class="h-24 w-24 shrink-0 rounded-xl object-cover" />
          <div class="flex flex-1 flex-col">
            <div class="flex items-start justify-between gap-2">
              <div>
                <h3 class="font-bold text-ocean-900">{{ item.produto.nome }}</h3>
                <p class="text-sm text-ocean-400">{{ item.produto.categoria }}</p>
              </div>
              <button class="text-ocean-300 hover:text-coral-600" @click="cart.remover(item.produto.id_produto)" aria-label="Remover">
                <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.35 9m-4.78 0L9.26 9m9.97-3.23c.34.06.68.12 1.02.19m-1.02-.19L18.16 19.67a2.25 2.25 0 0 1-2.24 2.08H8.08a2.25 2.25 0 0 1-2.24-2.08L4.77 5.79m14.46 0a48.11 48.11 0 0 0-3.48-.4m-11 .4c.34-.07.68-.13 1.02-.19m0 0a48.11 48.11 0 0 1 3.48-.4m7.5 0v-.92c0-1.18-.91-2.16-2.09-2.2a51.96 51.96 0 0 0-3.32 0c-1.18.04-2.09 1.02-2.09 2.2v.92m7.5 0a48.67 48.67 0 0 0-7.5 0" />
                </svg>
              </button>
            </div>
            <div class="mt-auto flex items-end justify-between pt-2">
              <div class="flex items-center rounded-lg border-2 border-ocean-100">
                <button class="h-9 w-9 text-lg font-bold text-ocean-600 hover:text-coral-600"
                  @click="cart.definirQuantidade(item.produto.id_produto, item.quantidade - 1)">−</button>
                <span class="w-9 text-center font-bold">{{ item.quantidade }}</span>
                <button class="h-9 w-9 text-lg font-bold text-ocean-600 hover:text-coral-600 disabled:opacity-30"
                  :disabled="item.quantidade >= item.produto.quantidade_estoque"
                  @click="cart.definirQuantidade(item.produto.id_produto, item.quantidade + 1)">+</button>
              </div>
              <p class="font-display text-xl text-coral-600">{{ moeda(item.produto.preco * item.quantidade) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumo -->
      <aside class="h-fit rounded-2xl border border-ocean-100 bg-white p-6 shadow-card lg:sticky lg:top-24">
        <h2 class="font-display text-2xl text-ocean-900">Resumo</h2>

        <div class="mt-4 space-y-2 text-sm">
          <div class="flex justify-between text-ocean-600">
            <span>Subtotal ({{ cart.quantidadeTotal }} itens)</span>
            <span class="font-semibold">{{ moeda(cart.subtotal) }}</span>
          </div>
          <div v-if="descontoEstimado > 0" class="flex justify-between text-emerald-600">
            <span>Desconto nakama (10%)</span>
            <span class="font-semibold">− {{ moeda(descontoEstimado) }}</span>
          </div>
          <div v-if="clienteElegivel === false && auth.ehCliente" class="rounded-lg bg-treasure-50 p-2.5 text-xs text-treasure-800">
            💡 Atenda a um critério de desconto no seu perfil e economize 10%!
          </div>
        </div>

        <div class="my-4 rope-divider opacity-40" />
        <div class="flex items-baseline justify-between">
          <span class="font-semibold text-ocean-700">Total</span>
          <span class="font-display text-3xl text-coral-600">{{ moeda(totalEstimado) }}</span>
        </div>

        <!-- Forma de pagamento -->
        <p class="label mt-6">Forma de pagamento</p>
        <div class="grid grid-cols-3 gap-2">
          <button v-for="f in formas" :key="f.valor" class="chip flex-col !py-3 text-center"
            :class="formaPagamento === f.valor ? 'chip-active' : 'chip-idle'" @click="formaPagamento = f.valor">
            <span class="text-lg">{{ f.icone }}</span>
            <span class="text-xs">{{ f.label }}</span>
          </button>
        </div>

        <button class="btn-primary mt-6 w-full text-base" :disabled="finalizando" @click="finalizar">
          <span v-if="finalizando">Processando...</span>
          <span v-else>Finalizar compra</span>
        </button>
        <p v-if="!auth.ehCliente" class="mt-3 text-center text-xs text-ocean-400">
          É necessário estar logado como cliente.
        </p>
      </aside>
    </div>
  </div>
</template>
