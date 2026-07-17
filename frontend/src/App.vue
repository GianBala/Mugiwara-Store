<script setup lang="ts">
import TheNavbar from '@/components/TheNavbar.vue'
import TheFooter from '@/components/TheFooter.vue'
import ToastContainer from '@/components/ToastContainer.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <TheNavbar />
    <main class="flex-1">
      <RouterView v-slot="{ Component, route }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </RouterView>
    </main>
    <TheFooter />
    <ToastContainer />
  </div>
</template>

<style scoped>
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
