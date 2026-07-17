<script setup lang="ts">
defineProps<{ class?: string }>()
</script>

<template>
  <!-- Ícone do chapéu de palha do Luffy -->
  <svg viewBox="0 0 64 40" fill="none" xmlns="http://www.w3.org/2000/svg" :class="$props.class">
    <ellipse cx="32" cy="33" rx="30" ry="6" fill="#f0c254" />
    <ellipse cx="32" cy="31" rx="30" ry="6" fill="#eaad2f" />
    <path
      d="M14 31c0-11 8-20 18-20s18 9 18 20"
      fill="#f5d98e"
    />
    <path
      d="M14 31c0-11 8-20 18-20s18 9 18 20"
      stroke="#bd6f15"
      stroke-width="1.5"
      fill="none"
    />
    <rect x="13" y="27" width="38" height="5.5" rx="2.75" fill="#e2493a" />
    <ellipse cx="32" cy="11.5" rx="10" ry="4" fill="#f0c254" />
  </svg>
</template>
