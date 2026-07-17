<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { api } from '@/api/client'
import { extrairErro } from '@/utils/format'
import { useToastStore } from '@/stores/toast'
import ProductCard from '@/components/ProductCard.vue'
import StrawHatIcon from '@/components/StrawHatIcon.vue'
import type { Produto } from '@/types'

const toast = useToastStore()

const produtos = ref<Produto[]>([])
const categorias = ref<string[]>([])
const carregando = ref(true)

const busca = ref('')
const categoriaSel = ref<string | null>(null)
const precoMax = ref<number | null>(null)

let debounce: number | undefined

async function carregar() {
  carregando.value = true
  try {
    const params: Record<string, any> = {}
    if (busca.value) params.busca = busca.value
    if (categoriaSel.value) params.categoria = categoriaSel.value
    if (precoMax.value) params.preco_max = precoMax.value
    const { data } = await api.get<Produto[]>('/produtos', { params })
    produtos.value = data
  } catch (e) {
    toast.erro(extrairErro(e, 'Não foi possível carregar o catálogo.'))
  } finally {
    carregando.value = false
  }
}

async function carregarCategorias() {
  try {
    const { data } = await api.get<string[]>('/produtos/categorias')
    categorias.value = data
  } catch {
    /* silencioso */
  }
}

watch([busca, categoriaSel, precoMax], () => {
  window.clearTimeout(debounce)
  debounce = window.setTimeout(carregar, 300)
})

function selecionarCategoria(cat: string | null) {
  categoriaSel.value = categoriaSel.value === cat ? null : cat
}

const totalResultados = computed(() => produtos.value.length)

onMounted(() => {
  carregar()
  carregarCategorias()
})
</script>

<template>
  <div>
  <!-- HERO -->
  <section class="relative overflow-hidden bg-ocean-hero">
    <div class="absolute inset-0 opacity-20"
      style="background-image: radial-gradient(circle, rgba(255,255,255,0.4) 1px, transparent 1px); background-size: 22px 22px;" />
    <div class="relative mx-auto grid max-w-7xl items-center gap-8 px-6 py-16 md:grid-cols-2 md:py-24">
      <div class="animate-fade-up">
        <span class="badge bg-treasure-400/20 text-treasure-200 ring-1 ring-treasure-400/40">🏴‍☠️ Grand Line Collection</span>
        <h1 class="mt-4 font-display text-5xl leading-tight text-white text-shadow-hero sm:text-6xl">
          Tesouros dignos do <span class="text-treasure-300">Rei dos Piratas</span>
        </h1>
        <p class="mt-4 max-w-lg text-lg text-ocean-100">
          Action figures, réplicas, pôsteres e colecionáveis oficiais do universo
          <span class="font-semibold text-treasure-200">One Piece</span>. Zarpe rumo à sua próxima aventura.
        </p>
        <div class="mt-8 flex flex-wrap gap-3">
          <a href="#catalogo" class="btn-primary text-base">Explorar catálogo</a>
          <RouterLink :to="{ name: 'cadastro' }" class="btn-treasure text-base">Junte-se à tripulação</RouterLink>
        </div>
        <div class="mt-8 flex items-center gap-6 text-sm text-ocean-200">
          <div><span class="font-display text-2xl text-treasure-300">10%</span> de desconto p/ nakamas</div>
          <div class="h-8 w-px bg-ocean-700" />
          <div><span class="font-display text-2xl text-treasure-300">100%</span> temático One Piece</div>
        </div>
      </div>
      <div class="relative hidden justify-center md:flex">
        <div class="absolute h-72 w-72 rounded-full bg-treasure-400/20 blur-3xl" />
        <StrawHatIcon class="relative w-72 animate-float-slow drop-shadow-2xl" />
      </div>
    </div>
    <div class="rope-divider" />
  </section>

  <!-- CATÁLOGO -->
  <section id="catalogo" class="mx-auto max-w-7xl px-6 py-12">
    <div class="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
      <div>
        <h2 class="font-display text-4xl text-ocean-900">Catálogo</h2>
        <p class="mt-1 text-ocean-500">{{ totalResultados }} tesouro(s) encontrado(s)</p>
      </div>
      <!-- Busca -->
      <div class="relative w-full md:w-80">
        <svg class="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-ocean-300"
          fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.2-5.2m2.2-5.3a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0Z" />
        </svg>
        <input v-model="busca" type="search" placeholder="Buscar por nome..." class="input pl-11" />
      </div>
    </div>

    <!-- Filtros -->
    <div class="mt-6 flex flex-wrap items-center gap-2">
      <button class="chip" :class="!categoriaSel ? 'chip-active' : 'chip-idle'" @click="selecionarCategoria(null)">
        Todos
      </button>
      <button
        v-for="cat in categorias"
        :key="cat"
        class="chip"
        :class="categoriaSel === cat ? 'chip-active' : 'chip-idle'"
        @click="selecionarCategoria(cat)"
      >
        {{ cat }}
      </button>
      <div class="ml-auto flex items-center gap-2">
        <label class="text-sm font-semibold text-ocean-600">Até {{ precoMax ? `R$ ${precoMax}` : 'qualquer valor' }}</label>
        <input v-model.number="precoMax" type="range" min="0" max="800" step="50" class="accent-coral-500" />
        <button v-if="precoMax" class="text-xs font-semibold text-coral-600 hover:underline" @click="precoMax = null">limpar</button>
      </div>
    </div>

    <!-- Grid -->
    <div v-if="carregando" class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <div v-for="n in 8" :key="n" class="h-80 animate-pulse rounded-2xl bg-ocean-100/70" />
    </div>

    <div v-else-if="produtos.length" class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <ProductCard v-for="p in produtos" :key="p.id_produto" :produto="p" />
    </div>

    <div v-else class="mt-16 flex flex-col items-center gap-3 text-center">
      <StrawHatIcon class="h-16 w-16 opacity-40" />
      <p class="font-display text-2xl text-ocean-700">Nenhum tesouro por aqui...</p>
      <p class="text-ocean-500">Tente ajustar a busca ou os filtros.</p>
    </div>
  </section>
  </div>
</template>
