<script setup lang="ts">
import StrawHatIcon from './StrawHatIcon.vue'
</script>

<template>
  <footer class="mt-20 border-t-4 border-treasure-400 bg-ocean-950 text-ocean-200">
    <div class="mx-auto grid max-w-7xl gap-8 px-6 py-12 md:grid-cols-3">
      <div>
        <div class="flex items-center gap-2.5">
          <StrawHatIcon class="h-8 w-8" />
          <span class="font-display text-2xl text-treasure-300">Mugiwara<span class="text-coral-400">Store</span></span>
        </div>
        <p class="mt-3 max-w-xs text-sm leading-relaxed text-ocean-300">
          Sua loja de tesouros do universo One Piece. Action figures, réplicas, pôsteres e
          colecionáveis dignos do Rei dos Piratas.
        </p>
      </div>

      <div>
        <h3 class="mb-3 font-display text-lg text-treasure-300">Navegação</h3>
        <ul class="space-y-2 text-sm">
          <li><RouterLink :to="{ name: 'home' }" class="hover:text-treasure-300">Catálogo</RouterLink></li>
          <li><RouterLink :to="{ name: 'carrinho' }" class="hover:text-treasure-300">Carrinho</RouterLink></li>
          <li><RouterLink :to="{ name: 'login' }" class="hover:text-treasure-300">Entrar</RouterLink></li>
        </ul>
      </div>

      <div>
        <h3 class="mb-3 font-display text-lg text-treasure-300">Descontos da Tripulação</h3>
        <ul class="space-y-2 text-sm text-ocean-300">
          <li>⚓ Assiste One Piece</li>
          <li>🔴 Torce pelo Flamengo</li>
          <li>🏴‍☠️ Natural de Sousa-PB</li>
        </ul>
        <p class="mt-3 text-xs text-ocean-400">Atenda a um critério e ganhe 10% de desconto!</p>
      </div>
    </div>
    <div class="border-t border-ocean-800 py-4 text-center text-xs text-ocean-400">
      © 2026 Mugiwara Store · Projeto acadêmico — Tópicos Avançados em Ciência da Computação XI
    </div>
  </footer>
</template>
