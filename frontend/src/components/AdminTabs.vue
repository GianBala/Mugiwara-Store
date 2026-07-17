<script setup lang="ts">
const tabs = [
  { name: 'painel', label: 'Visão Geral', icone: '📊' },
  { name: 'painel-produtos', label: 'Produtos', icone: '📦' },
  { name: 'painel-relatorios', label: 'Relatórios', icone: '📈' },
]
</script>

<template>
  <div class="flex flex-wrap gap-2 rounded-2xl border border-ocean-100 bg-white p-1.5 shadow-card">
    <RouterLink
      v-for="t in tabs"
      :key="t.name"
      :to="{ name: t.name }"
      class="flex flex-1 items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold text-ocean-500 transition hover:bg-ocean-50"
      active-class="!bg-ocean-hero !text-treasure-300"
    >
      <span>{{ t.icone }}</span>{{ t.label }}
    </RouterLink>
  </div>
</template>
