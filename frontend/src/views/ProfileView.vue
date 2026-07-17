<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import { extrairErro } from '@/utils/format'
import { useToastStore } from '@/stores/toast'
import type { Cliente } from '@/types'

const toast = useToastStore()
const cliente = ref<Cliente | null>(null)
const carregando = ref(true)

async function carregar() {
  try {
    const { data } = await api.get<Cliente>('/clientes/me')
    cliente.value = data
  } catch (e) {
    toast.erro(extrairErro(e, 'Não foi possível carregar o perfil.'))
  } finally {
    carregando.value = false
  }
}

onMounted(carregar)
</script>

<template>
  <div class="mx-auto max-w-3xl px-6 py-10">
    <div v-if="carregando" class="h-64 animate-pulse rounded-3xl bg-ocean-100/70" />

    <div v-else-if="cliente">
      <!-- Cabeçalho -->
      <div class="relative overflow-hidden rounded-3xl bg-ocean-hero p-8 text-white">
        <div class="flex items-center gap-5">
          <div class="grid h-20 w-20 shrink-0 place-items-center rounded-2xl bg-treasure-400 font-display text-4xl text-ocean-950">
            {{ cliente.nome.charAt(0).toUpperCase() }}
          </div>
          <div>
            <h1 class="font-display text-3xl text-shadow-hero">{{ cliente.nome }}</h1>
            <p class="text-ocean-200">{{ cliente.email }}</p>
            <span v-if="cliente.elegivel_desconto" class="badge mt-2 bg-treasure-400 text-ocean-950">★ Nakama com 10% de desconto</span>
          </div>
        </div>
      </div>

      <!-- Cards -->
      <div class="mt-6 grid gap-6 sm:grid-cols-2">
        <div class="card p-6">
          <h2 class="mb-4 font-display text-xl text-ocean-800">Endereço</h2>
          <template v-if="cliente.endereco">
            <p class="text-ocean-700">{{ cliente.endereco.logradouro || 'Logradouro não informado' }}, {{ cliente.numero_endereco || 's/n' }}</p>
            <p class="text-ocean-500">{{ cliente.endereco.bairro }}</p>
            <p class="text-ocean-500">{{ cliente.endereco.cidade }} - {{ cliente.endereco.estado }}</p>
            <p class="text-ocean-400">CEP: {{ cliente.endereco.cep }}</p>
            <p v-if="cliente.complemento_endereco" class="mt-1 text-ocean-500">{{ cliente.complemento_endereco }}</p>
          </template>
          <p v-else class="text-ocean-400">Nenhum endereço cadastrado.</p>
        </div>

        <div class="card p-6">
          <h2 class="mb-4 font-display text-xl text-ocean-800">Contato & Benefícios</h2>
          <div class="space-y-2 text-sm">
            <p class="text-ocean-600"><span class="font-semibold">Telefones:</span>
              {{ cliente.telefones.length ? cliente.telefones.join(', ') : 'não informado' }}
            </p>
            <div class="mt-3 flex flex-wrap gap-2">
              <span v-if="cliente.assiste_one_piece" class="badge bg-ocean-100 text-ocean-700">⚓ One Piece</span>
              <span v-if="cliente.torce_flamengo" class="badge bg-coral-100 text-coral-700">🔴 Flamengo</span>
              <span v-if="cliente.natural_de_sousa" class="badge bg-treasure-100 text-treasure-800">🏴‍☠️ Sousa-PB</span>
              <span v-if="!cliente.assiste_one_piece && !cliente.torce_flamengo && !cliente.natural_de_sousa" class="text-ocean-400">
                Nenhum critério de desconto marcado.
              </span>
            </div>
          </div>
        </div>
      </div>

      <RouterLink :to="{ name: 'pedidos' }" class="btn-outline mt-6">Ver meus pedidos →</RouterLink>
    </div>
  </div>
</template>
