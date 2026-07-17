<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, resolverImagem } from '@/api/client'
import { moeda, extrairErro } from '@/utils/format'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import type { Produto } from '@/types'

const route = useRoute()
const router = useRouter()
const cart = useCartStore()
const auth = useAuthStore()
const toast = useToastStore()

const produto = ref<Produto | null>(null)
const carregando = ref(true)
const quantidade = ref(1)

const semEstoque = computed(() => (produto.value?.quantidade_estoque ?? 0) <= 0)

async function carregar() {
  carregando.value = true
  try {
    const { data } = await api.get<Produto>(`/produtos/${route.params.id}`)
    produto.value = data
  } catch (e) {
    toast.erro(extrairErro(e, 'Produto não encontrado.'))
    router.push({ name: 'home' })
  } finally {
    carregando.value = false
  }
}

function adicionar() {
  if (!produto.value || semEstoque.value) return
  cart.adicionar(produto.value, quantidade.value)
  toast.sucesso(`${quantidade.value}x "${produto.value.nome}" no carrinho!`)
}

function comprarAgora() {
  adicionar()
  router.push({ name: 'carrinho' })
}

onMounted(carregar)
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-10">
    <button class="mb-6 flex items-center gap-1.5 text-sm font-semibold text-ocean-500 hover:text-coral-600" @click="router.back()">
      <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
      </svg>
      Voltar
    </button>

    <div v-if="carregando" class="grid gap-8 md:grid-cols-2">
      <div class="aspect-square animate-pulse rounded-3xl bg-ocean-100" />
      <div class="space-y-4">
        <div class="h-8 w-3/4 animate-pulse rounded bg-ocean-100" />
        <div class="h-24 animate-pulse rounded bg-ocean-100" />
      </div>
    </div>

    <div v-else-if="produto" class="grid gap-10 md:grid-cols-2">
      <!-- Imagem -->
      <div class="relative overflow-hidden rounded-3xl border border-ocean-100 bg-white shadow-card">
        <img :src="resolverImagem(produto.imagem)" :alt="produto.nome" class="aspect-square w-full object-cover" />
        <span v-if="produto.fabricado_em_mari" class="absolute left-4 top-4 badge bg-treasure-400 text-ocean-950">★ Edição Mari</span>
      </div>

      <!-- Detalhes -->
      <div class="flex flex-col">
        <span class="badge w-fit bg-ocean-100 text-ocean-700">{{ produto.categoria }}</span>
        <h1 class="mt-3 font-display text-4xl leading-tight text-ocean-900">{{ produto.nome }}</h1>
        <p class="mt-4 text-lg leading-relaxed text-ocean-600">{{ produto.descricao }}</p>

        <div class="mt-6 flex items-baseline gap-3">
          <span class="font-display text-5xl text-coral-600">{{ moeda(produto.preco) }}</span>
        </div>

        <!-- Estoque -->
        <div class="mt-4 flex items-center gap-2 text-sm">
          <template v-if="semEstoque">
            <span class="h-2.5 w-2.5 rounded-full bg-ocean-400" />
            <span class="font-semibold text-ocean-500">Produto esgotado</span>
          </template>
          <template v-else-if="produto.quantidade_estoque < 5">
            <span class="h-2.5 w-2.5 animate-pulse rounded-full bg-coral-500" />
            <span class="font-semibold text-coral-600">Apenas {{ produto.quantidade_estoque }} em estoque!</span>
          </template>
          <template v-else>
            <span class="h-2.5 w-2.5 rounded-full bg-emerald-500" />
            <span class="font-semibold text-emerald-600">Em estoque ({{ produto.quantidade_estoque }} unidades)</span>
          </template>
        </div>

        <!-- Ações do cliente -->
        <div v-if="!auth.ehFuncionario" class="mt-8 flex flex-wrap items-center gap-4">
          <div class="flex items-center rounded-xl border-2 border-ocean-100 bg-white">
            <button class="grid h-11 w-11 place-items-center text-xl font-bold text-ocean-600 hover:text-coral-600 disabled:opacity-30"
              :disabled="quantidade <= 1 || semEstoque" @click="quantidade--">−</button>
            <span class="w-10 text-center font-bold">{{ quantidade }}</span>
            <button class="grid h-11 w-11 place-items-center text-xl font-bold text-ocean-600 hover:text-coral-600 disabled:opacity-30"
              :disabled="quantidade >= produto.quantidade_estoque || semEstoque" @click="quantidade++">+</button>
          </div>
          <button class="btn-treasure text-base" :disabled="semEstoque" @click="adicionar">Adicionar ao carrinho</button>
          <button class="btn-primary text-base" :disabled="semEstoque" @click="comprarAgora">Comprar agora</button>
        </div>

        <div v-else class="mt-8 rounded-xl bg-ocean-50 p-4 text-sm text-ocean-600">
          Você está autenticado como funcionário. Gerencie este produto pelo
          <RouterLink :to="{ name: 'painel-produtos' }" class="font-semibold text-coral-600 hover:underline">painel</RouterLink>.
        </div>
      </div>
    </div>
  </div>
</template>
