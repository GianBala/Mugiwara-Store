<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { resolverImagem } from '@/api/client'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import { moeda } from '@/utils/format'
import type { Produto } from '@/types'

const props = defineProps<{ produto: Produto }>()
const cart = useCartStore()
const auth = useAuthStore()
const toast = useToastStore()
const router = useRouter()

const semEstoque = computed(() => props.produto.quantidade_estoque <= 0)
const estoqueBaixo = computed(
  () => props.produto.quantidade_estoque > 0 && props.produto.quantidade_estoque < 5,
)

function adicionar() {
  if (semEstoque.value) return
  cart.adicionar(props.produto, 1)
  toast.sucesso(`"${props.produto.nome}" foi para o carrinho!`)
}
</script>

<template>
  <article
    class="group flex flex-col overflow-hidden rounded-2xl border border-ocean-100 bg-white shadow-card transition-all duration-300 hover:-translate-y-1.5 hover:shadow-card-hover"
  >
    <!-- Imagem -->
    <div class="relative aspect-[4/3] cursor-pointer overflow-hidden bg-ocean-50" @click="router.push({ name: 'produto', params: { id: produto.id_produto } })">
      <img
        :src="resolverImagem(produto.imagem)"
        :alt="produto.nome"
        loading="lazy"
        class="h-full w-full object-cover transition duration-500 group-hover:scale-110"
      />
      <div class="absolute left-3 top-3 flex flex-col gap-1.5">
        <span class="badge bg-ocean-900/90 text-treasure-200 backdrop-blur">{{ produto.categoria }}</span>
        <span v-if="produto.fabricado_em_mari" class="badge bg-treasure-400/95 text-ocean-950">★ Edição Mari</span>
      </div>
      <span v-if="semEstoque" class="absolute right-3 top-3 badge bg-ocean-900/90 text-white">Esgotado</span>
      <span v-else-if="estoqueBaixo" class="absolute right-3 top-3 badge bg-coral-500 text-white">Últimas unidades</span>
    </div>

    <!-- Conteúdo -->
    <div class="flex flex-1 flex-col p-4">
      <h3
        class="cursor-pointer font-bold leading-snug text-ocean-900 line-clamp-2 hover:text-coral-600"
        @click="router.push({ name: 'produto', params: { id: produto.id_produto } })"
      >
        {{ produto.nome }}
      </h3>
      <p class="mt-1 line-clamp-2 text-sm text-ocean-500">{{ produto.descricao }}</p>

      <div class="mt-auto flex items-end justify-between pt-4">
        <div>
          <p class="text-xs font-medium text-ocean-400">à vista</p>
          <p class="font-display text-2xl leading-none text-coral-600">{{ moeda(produto.preco) }}</p>
        </div>
        <button
          v-if="!auth.ehFuncionario"
          class="btn-treasure !px-3.5 !py-2.5"
          :disabled="semEstoque"
          @click="adicionar"
          :aria-label="`Adicionar ${produto.nome} ao carrinho`"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
        </button>
      </div>
    </div>
  </article>
</template>
