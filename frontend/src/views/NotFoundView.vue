<script setup lang="ts">
import StrawHatIcon from '@/components/StrawHatIcon.vue'
</script>

<template>
  <div class="mx-auto flex min-h-[60vh] max-w-lg flex-col items-center justify-center px-6 text-center">
    <StrawHatIcon class="h-20 w-20 animate-float-slow opacity-70" />
    <h1 class="mt-6 font-display text-7xl text-ocean-900">404</h1>
    <p class="mt-2 font-display text-2xl text-coral-600">Ilha não encontrada no mapa</p>
    <p class="mt-2 text-ocean-500">Nem o Log Pose conseguiu localizar esta página.</p>
    <RouterLink :to="{ name: 'home' }" class="btn-treasure mt-6">Voltar ao porto seguro</RouterLink>
  </div>
</template>
