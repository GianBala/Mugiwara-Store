<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { moeda, dataHora, extrairErro } from '@/utils/format'
import { useToastStore } from '@/stores/toast'
import type { Pedido } from '@/types'

const toast = useToastStore()
const pedidos = ref<Pedido[]>([])
const carregando = ref(true)
const expandido = ref<number | null>(null)

const statusCor: Record<string, string> = {
  APROVADO: 'bg-emerald-100 text-emerald-700',
  PENDENTE: 'bg-treasure-100 text-treasure-800',
  CANCELADO: 'bg-coral-100 text-coral-700',
}

async function carregar() {
  try {
    const { data } = await api.get<Pedido[]>('/pedidos/meus')
    pedidos.value = data
  } catch (e) {
    toast.erro(extrairErro(e, 'Não foi possível carregar os pedidos.'))
  } finally {
    carregando.value = false
  }
}

onMounted(carregar)
</script>

<template>
  <div class="mx-auto max-w-4xl px-6 py-10">
    <h1 class="font-display text-4xl text-ocean-900">Meus Pedidos</h1>
    <p class="mt-1 text-ocean-500">Acompanhe o histórico das suas aventuras de compra.</p>

    <div v-if="carregando" class="mt-8 space-y-4">
      <div v-for="n in 3" :key="n" class="h-24 animate-pulse rounded-2xl bg-ocean-100/70" />
    </div>

    <div v-else-if="!pedidos.length" class="mt-12 flex flex-col items-center gap-3 text-center">
      <div class="grid h-24 w-24 place-items-center rounded-full bg-ocean-50 text-5xl">📜</div>
      <p class="font-display text-2xl text-ocean-700">Nenhum pedido ainda</p>
      <RouterLink :to="{ name: 'home' }" class="btn-treasure mt-2">Começar a comprar</RouterLink>
    </div>

    <div v-else class="mt-8 space-y-4">
      <div v-for="p in pedidos" :key="p.id_pedido" class="overflow-hidden rounded-2xl border border-ocean-100 bg-white shadow-card">
        <button class="flex w-full items-center gap-4 p-5 text-left" @click="expandido = expandido === p.id_pedido ? null : p.id_pedido">
          <div class="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-ocean-hero font-display text-lg text-treasure-300">
            #{{ p.id_pedido }}
          </div>
          <div class="flex-1">
            <p class="font-bold text-ocean-900">Pedido #{{ p.id_pedido }}</p>
            <p class="text-sm text-ocean-400">{{ dataHora(p.data_pedido) }} · {{ p.forma_pagamento }}</p>
          </div>
          <span class="badge" :class="statusCor[p.status_pagamento] || 'bg-ocean-100 text-ocean-600'">{{ p.status_pagamento }}</span>
          <div class="text-right">
            <p class="font-display text-xl text-coral-600">{{ moeda(p.valor_total) }}</p>
            <p class="text-xs text-ocean-400">{{ p.itens.length }} item(ns)</p>
          </div>
          <svg class="h-5 w-5 text-ocean-300 transition" :class="{ 'rotate-180': expandido === p.id_pedido }" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </button>

        <transition name="expand">
          <div v-if="expandido === p.id_pedido" class="border-t border-ocean-100 bg-ocean-50/50 px-5 py-4">
            <table class="w-full text-sm">
              <thead>
                <tr class="text-left text-ocean-400">
                  <th class="pb-2 font-semibold">Produto</th>
                  <th class="pb-2 text-center font-semibold">Qtd</th>
                  <th class="pb-2 text-right font-semibold">Preço unit.</th>
                  <th class="pb-2 text-right font-semibold">Subtotal</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-ocean-100">
                <tr v-for="item in p.itens" :key="item.id_produto">
                  <td class="py-2 font-medium text-ocean-800">{{ item.nome_produto || `Produto #${item.id_produto}` }}</td>
                  <td class="py-2 text-center">{{ item.quantidade }}</td>
                  <td class="py-2 text-right">{{ moeda(item.preco_unitario_na_venda) }}</td>
                  <td class="py-2 text-right font-semibold">{{ moeda(item.preco_unitario_na_venda * item.quantidade) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
}
.expand-enter-to,
.expand-leave-from {
  max-height: 400px;
}
</style>
