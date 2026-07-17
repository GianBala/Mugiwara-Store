<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useToastStore } from '@/stores/toast'
import StrawHatIcon from './StrawHatIcon.vue'

const auth = useAuthStore()
const cart = useCartStore()
const toast = useToastStore()
const router = useRouter()

const menuAberto = ref(false)

function sair() {
  auth.logout()
  toast.sucesso('Você saiu da tripulação. Até a próxima!')
  router.push({ name: 'home' })
  menuAberto.value = false
}
</script>

<template>
  <header class="sticky top-0 z-50 border-b border-ocean-800/40 bg-ocean-950/95 backdrop-blur">
    <nav class="mx-auto flex h-16 max-w-7xl items-center gap-4 px-4 sm:px-6">
      <!-- Logo -->
      <RouterLink :to="{ name: 'home' }" class="flex items-center gap-2.5">
        <StrawHatIcon class="h-9 w-9 drop-shadow" />
        <span class="font-display text-2xl leading-none text-treasure-300">
          Mugiwara<span class="text-coral-400">Store</span>
        </span>
      </RouterLink>

      <div class="flex-1" />

      <!-- Ações desktop -->
      <div class="hidden items-center gap-1.5 md:flex">
        <RouterLink :to="{ name: 'home' }" class="nav-link">Catálogo</RouterLink>

        <template v-if="auth.ehFuncionario">
          <RouterLink :to="{ name: 'painel' }" class="nav-link">Painel</RouterLink>
        </template>

        <template v-if="auth.ehCliente">
          <RouterLink :to="{ name: 'pedidos' }" class="nav-link">Meus Pedidos</RouterLink>
        </template>

        <!-- Carrinho -->
        <RouterLink
          v-if="!auth.ehFuncionario"
          :to="{ name: 'carrinho' }"
          class="nav-link relative"
          aria-label="Carrinho"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121 0 2.1-.744 2.4-1.821l1.05-3.75c.15-.535-.11-1.079-.6-1.267m-15.6 0L5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
          </svg>
          <span
            v-if="cart.quantidadeTotal > 0"
            class="absolute -right-1 -top-1 grid h-5 min-w-[1.25rem] place-items-center rounded-full bg-coral-500 px-1 text-[11px] font-bold text-white"
          >
            {{ cart.quantidadeTotal }}
          </span>
        </RouterLink>

        <!-- Autenticação -->
        <template v-if="auth.autenticado">
          <RouterLink v-if="auth.ehCliente" :to="{ name: 'perfil' }" class="nav-link">
            <span class="grid h-7 w-7 place-items-center rounded-full bg-treasure-400 text-sm font-black text-ocean-950">
              {{ auth.nome?.charAt(0).toUpperCase() }}
            </span>
          </RouterLink>
          <span class="ml-1 hidden text-sm font-semibold text-ocean-200 lg:inline">Olá, {{ auth.nome }}</span>
          <button class="btn-outline ml-1 !px-3 !py-2" @click="sair">Sair</button>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'login' }" class="btn-ghost !text-ocean-100 hover:!bg-ocean-800">Entrar</RouterLink>
          <RouterLink :to="{ name: 'cadastro' }" class="btn-treasure !px-4 !py-2">Criar conta</RouterLink>
        </template>
      </div>

      <!-- Botão mobile -->
      <button
        class="grid h-10 w-10 place-items-center rounded-lg text-ocean-100 hover:bg-ocean-800 md:hidden"
        @click="menuAberto = !menuAberto"
        aria-label="Menu"
      >
        <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
        </svg>
      </button>
    </nav>

    <!-- Menu mobile -->
    <transition name="slide">
      <div v-if="menuAberto" class="border-t border-ocean-800 bg-ocean-950 px-4 py-3 md:hidden">
        <div class="flex flex-col gap-1">
          <RouterLink :to="{ name: 'home' }" class="nav-link-mobile" @click="menuAberto = false">Catálogo</RouterLink>
          <RouterLink v-if="!auth.ehFuncionario" :to="{ name: 'carrinho' }" class="nav-link-mobile" @click="menuAberto = false">
            Carrinho ({{ cart.quantidadeTotal }})
          </RouterLink>
          <RouterLink v-if="auth.ehCliente" :to="{ name: 'pedidos' }" class="nav-link-mobile" @click="menuAberto = false">Meus Pedidos</RouterLink>
          <RouterLink v-if="auth.ehCliente" :to="{ name: 'perfil' }" class="nav-link-mobile" @click="menuAberto = false">Meu Perfil</RouterLink>
          <RouterLink v-if="auth.ehFuncionario" :to="{ name: 'painel' }" class="nav-link-mobile" @click="menuAberto = false">Painel</RouterLink>
          <template v-if="auth.autenticado">
            <button class="nav-link-mobile text-left text-coral-300" @click="sair">Sair</button>
          </template>
          <template v-else>
            <RouterLink :to="{ name: 'login' }" class="nav-link-mobile" @click="menuAberto = false">Entrar</RouterLink>
            <RouterLink :to="{ name: 'cadastro' }" class="nav-link-mobile text-treasure-300" @click="menuAberto = false">Criar conta</RouterLink>
          </template>
        </div>
      </div>
    </transition>
  </header>
</template>

<style scoped>
.nav-link {
  @apply flex items-center rounded-lg px-3 py-2 text-sm font-semibold text-ocean-100 transition hover:bg-ocean-800 hover:text-treasure-300;
}
.router-link-active.nav-link {
  @apply text-treasure-300;
}
.nav-link-mobile {
  @apply rounded-lg px-3 py-2.5 text-sm font-semibold text-ocean-100 hover:bg-ocean-800;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
