<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { moeda, extrairErro } from '@/utils/format'
import { useToastStore } from '@/stores/toast'
import AdminTabs from '@/components/AdminTabs.vue'
import type { RelatorioVendas } from '@/types'

const toast = useToastStore()

const hoje = new Date()
const ano = ref(hoje.getFullYear())
const mes = ref(hoje.getMonth() + 1)
const relatorio = ref<RelatorioVendas | null>(null)
const carregando = ref(true)

const meses = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
]

const maiorVenda = computed(() => {
  if (!relatorio.value?.ranking_vendedores.length) return 1
  return Math.max(...relatorio.value.ranking_vendedores.map((v) => v.total_vendido), 1)
})

async function carregar() {
  carregando.value = true
  try {
    const { data } = await api.get<RelatorioVendas>('/relatorios/vendas', { params: { ano: ano.value, mes: mes.value } })
    relatorio.value = data
  } catch (e) {
    toast.erro(extrairErro(e, 'Não foi possível carregar o relatório.'))
  } finally {
    carregando.value = false
  }
}

const medalhas = ['🥇', '🥈', '🥉']

onMounted(carregar)
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-10">
    <div class="mb-6">
      <h1 class="font-display text-4xl text-ocean-900">Relatórios Gerenciais</h1>
      <p class="mt-1 text-ocean-500">Vendas mensais e desempenho da tripulação de vendedores.</p>
    </div>

    <AdminTabs />

    <!-- Seletor de período -->
    <div class="mt-8 flex flex-wrap items-end gap-4 rounded-2xl border border-ocean-100 bg-white p-5 shadow-card">
      <div>
        <label class="label">Mês</label>
        <select v-model.number="mes" class="input min-w-[150px]">
          <option v-for="(m, i) in meses" :key="i" :value="i + 1">{{ m }}</option>
        </select>
      </div>
      <div>
        <label class="label">Ano</label>
        <input v-model.number="ano" type="number" min="2000" max="2100" class="input w-28" />
      </div>
      <button class="btn-treasure" @click="carregar">Gerar relatório</button>
    </div>

    <div v-if="carregando" class="mt-8 h-64 animate-pulse rounded-2xl bg-ocean-100/70" />

    <template v-else-if="relatorio">
      <!-- Totais do mês -->
      <div class="mt-8 grid gap-5 sm:grid-cols-2">
        <div class="card flex items-center gap-4 p-6">
          <span class="grid h-14 w-14 place-items-center rounded-2xl bg-ocean-hero text-2xl text-treasure-300">🧾</span>
          <div>
            <p class="text-sm font-semibold text-ocean-400">Pedidos no mês</p>
            <p class="font-display text-4xl text-ocean-900">{{ relatorio.total_pedidos }}</p>
          </div>
        </div>
        <div class="card flex items-center gap-4 p-6">
          <span class="grid h-14 w-14 place-items-center rounded-2xl bg-emerald-100 text-2xl">💰</span>
          <div>
            <p class="text-sm font-semibold text-ocean-400">Faturamento total</p>
            <p class="font-display text-4xl text-emerald-600">{{ moeda(relatorio.total_vendido) }}</p>
          </div>
        </div>
      </div>

      <!-- Ranking de vendedores -->
      <div class="mt-8 card overflow-hidden">
        <div class="border-b border-ocean-100 px-6 py-4">
          <h2 class="font-display text-2xl text-ocean-800">🏆 Ranking de Vendedores — {{ meses[mes - 1] }}/{{ ano }}</h2>
        </div>

        <div v-if="!relatorio.ranking_vendedores.length" class="p-10 text-center text-ocean-400">
          Nenhuma venda registrada neste período.
        </div>

        <ul v-else class="divide-y divide-ocean-100">
          <li v-for="(v, i) in relatorio.ranking_vendedores" :key="v.id_funcionario" class="px-6 py-4">
            <div class="flex items-center gap-4">
              <span class="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-ocean-50 text-lg font-black text-ocean-600">
                {{ medalhas[i] || i + 1 }}
              </span>
              <div class="flex-1">
                <p class="font-bold text-ocean-900">{{ v.nome_vendedor }}</p>
                <p class="text-sm text-ocean-400">{{ v.cargo || 'Vendedor' }} · {{ v.total_pedidos }} pedido(s) · {{ v.total_itens }} item(ns)</p>
                <!-- Barra de progresso -->
                <div class="mt-2 h-2 w-full overflow-hidden rounded-full bg-ocean-100">
                  <div class="h-full rounded-full bg-gradient-to-r from-treasure-400 to-coral-500 transition-all duration-700"
                    :style="{ width: `${(v.total_vendido / maiorVenda) * 100}%` }" />
                </div>
              </div>
              <p class="font-display text-2xl text-coral-600">{{ moeda(v.total_vendido) }}</p>
            </div>
          </li>
        </ul>
      </div>
    </template>
  </div>
</template>
