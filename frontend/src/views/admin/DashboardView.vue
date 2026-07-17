<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { moeda, extrairErro } from '@/utils/format'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import AdminTabs from '@/components/AdminTabs.vue'
import type { Produto, ResumoEstoque } from '@/types'

const auth = useAuthStore()
const toast = useToastStore()

const resumo = ref<ResumoEstoque | null>(null)
const estoqueBaixo = ref<Produto[]>([])
const carregando = ref(true)

async function carregar() {
  try {
    const [r1, r2] = await Promise.all([
      api.get<ResumoEstoque>('/relatorios/estoque'),
      api.get<Produto[]>('/relatorios/estoque-baixo'),
    ])
    resumo.value = r1.data
    estoqueBaixo.value = r2.data
  } catch (e) {
    toast.erro(extrairErro(e, 'Não foi possível carregar o painel.'))
  } finally {
    carregando.value = false
  }
}

onMounted(carregar)
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-10">
    <div class="mb-6">
      <h1 class="font-display text-4xl text-ocean-900">Painel do Funcionário</h1>
      <p class="mt-1 text-ocean-500">Bem-vindo, <strong>{{ auth.nome }}</strong>. Comande o convés da Mugiwara Store.</p>
    </div>

    <AdminTabs />

    <div v-if="carregando" class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <div v-for="n in 4" :key="n" class="h-32 animate-pulse rounded-2xl bg-ocean-100/70" />
    </div>

    <template v-else>
      <!-- KPIs -->
      <div class="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div class="card p-5">
          <div class="flex items-center gap-3">
            <span class="grid h-11 w-11 place-items-center rounded-xl bg-ocean-100 text-xl">📦</span>
            <span class="text-sm font-semibold text-ocean-400">Produtos</span>
          </div>
          <p class="mt-3 font-display text-4xl text-ocean-900">{{ resumo?.total_produtos }}</p>
        </div>
        <div class="card p-5">
          <div class="flex items-center gap-3">
            <span class="grid h-11 w-11 place-items-center rounded-xl bg-treasure-100 text-xl">🎒</span>
            <span class="text-sm font-semibold text-ocean-400">Unidades em estoque</span>
          </div>
          <p class="mt-3 font-display text-4xl text-ocean-900">{{ resumo?.total_unidades }}</p>
        </div>
        <div class="card p-5">
          <div class="flex items-center gap-3">
            <span class="grid h-11 w-11 place-items-center rounded-xl bg-emerald-100 text-xl">💰</span>
            <span class="text-sm font-semibold text-ocean-400">Valor do estoque</span>
          </div>
          <p class="mt-3 font-display text-3xl text-ocean-900">{{ moeda(resumo?.valor_total_estoque || 0) }}</p>
        </div>
        <div class="card p-5" :class="{ 'ring-2 ring-coral-300': (resumo?.produtos_estoque_baixo || 0) > 0 }">
          <div class="flex items-center gap-3">
            <span class="grid h-11 w-11 place-items-center rounded-xl bg-coral-100 text-xl">⚠️</span>
            <span class="text-sm font-semibold text-ocean-400">Estoque baixo</span>
          </div>
          <p class="mt-3 font-display text-4xl text-coral-600">{{ resumo?.produtos_estoque_baixo }}</p>
        </div>
      </div>

      <!-- Alerta de estoque baixo -->
      <div class="mt-8 card overflow-hidden">
        <div class="flex items-center justify-between border-b border-ocean-100 bg-coral-50/60 px-6 py-4">
          <h2 class="font-display text-2xl text-ocean-800">⚠️ Alerta de Estoque Baixo</h2>
          <span class="badge bg-coral-500 text-white">{{ estoqueBaixo.length }} produto(s) &lt; 5 un.</span>
        </div>
        <div v-if="!estoqueBaixo.length" class="p-8 text-center text-ocean-400">
          Tudo em ordem, capitão! Nenhum produto com estoque crítico. 🎉
        </div>
        <table v-else class="w-full text-sm">
          <thead class="bg-ocean-50 text-left text-ocean-400">
            <tr>
              <th class="px-6 py-3 font-semibold">Produto</th>
              <th class="px-6 py-3 font-semibold">Categoria</th>
              <th class="px-6 py-3 text-center font-semibold">Estoque</th>
              <th class="px-6 py-3 text-right font-semibold">Preço</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-ocean-100">
            <tr v-for="p in estoqueBaixo" :key="p.id_produto" class="hover:bg-ocean-50/50">
              <td class="px-6 py-3 font-medium text-ocean-800">{{ p.nome }}</td>
              <td class="px-6 py-3 text-ocean-500">{{ p.categoria }}</td>
              <td class="px-6 py-3 text-center">
                <span class="badge" :class="p.quantidade_estoque === 0 ? 'bg-ocean-200 text-ocean-700' : 'bg-coral-100 text-coral-700'">
                  {{ p.quantidade_estoque }} un.
                </span>
              </td>
              <td class="px-6 py-3 text-right font-semibold text-ocean-700">{{ moeda(p.preco) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
