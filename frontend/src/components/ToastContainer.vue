<script setup lang="ts">
import { useToastStore } from '@/stores/toast'
const toast = useToastStore()

const estilos: Record<string, string> = {
  sucesso: 'border-emerald-400 bg-emerald-50 text-emerald-800',
  erro: 'border-coral-400 bg-coral-50 text-coral-800',
  info: 'border-ocean-300 bg-ocean-50 text-ocean-800',
}
const icones: Record<string, string> = { sucesso: '✓', erro: '✕', info: 'ⓘ' }
</script>

<template>
  <div class="pointer-events-none fixed bottom-6 right-6 z-[100] flex w-80 flex-col gap-3">
    <transition-group name="toast">
      <div
        v-for="t in toast.toasts"
        :key="t.id"
        class="pointer-events-auto flex items-center gap-3 rounded-xl border-2 px-4 py-3 shadow-card-hover"
        :class="estilos[t.tipo]"
      >
        <span class="grid h-6 w-6 shrink-0 place-items-center rounded-full bg-white/70 text-sm font-black">
          {{ icones[t.tipo] }}
        </span>
        <p class="text-sm font-semibold">{{ t.mensagem }}</p>
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(40px);
}
</style>
