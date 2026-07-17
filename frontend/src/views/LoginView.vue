<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import { extrairErro } from '@/utils/format'
import StrawHatIcon from '@/components/StrawHatIcon.vue'

const auth = useAuthStore()
const toast = useToastStore()
const router = useRouter()
const route = useRoute()

const email = ref('')
const senha = ref('')
const carregando = ref(false)

async function entrar() {
  carregando.value = true
  try {
    await auth.login(email.value, senha.value)
    toast.sucesso(`Bem-vindo a bordo, ${auth.nome}!`)
    const redirect = route.query.redirect as string | undefined
    if (redirect) router.push(redirect)
    else router.push({ name: auth.ehFuncionario ? 'painel' : 'home' })
  } catch (e) {
    toast.erro(extrairErro(e, 'E-mail ou senha inválidos.'))
  } finally {
    carregando.value = false
  }
}

function preencher(tipo: 'cliente' | 'funcionario') {
  if (tipo === 'cliente') {
    email.value = 'luffy@mugiwara.com'
  } else {
    email.value = 'nami@mugiwara.com'
  }
  senha.value = 'senha123'
}
</script>

<template>
  <div class="mx-auto grid min-h-[calc(100vh-4rem)] max-w-6xl items-center gap-10 px-6 py-10 md:grid-cols-2">
    <!-- Ilustração -->
    <div class="hidden rounded-3xl bg-ocean-hero p-10 text-white md:block">
      <StrawHatIcon class="h-16 w-16" />
      <h2 class="mt-6 font-display text-4xl leading-tight text-shadow-hero">
        Bem-vindo de volta,<br />pirata!
      </h2>
      <p class="mt-3 text-ocean-100">Faça login para continuar sua jornada rumo aos tesouros da Grand Line.</p>

      <div class="mt-10 space-y-3 rounded-2xl bg-white/10 p-5 backdrop-blur">
        <p class="text-sm font-semibold text-treasure-200">🔑 Contas de demonstração (senha: senha123)</p>
        <button class="flex w-full items-center justify-between rounded-lg bg-white/10 px-4 py-2 text-left text-sm hover:bg-white/20" @click="preencher('cliente')">
          <span>Cliente — luffy@mugiwara.com</span><span class="text-treasure-200">usar →</span>
        </button>
        <button class="flex w-full items-center justify-between rounded-lg bg-white/10 px-4 py-2 text-left text-sm hover:bg-white/20" @click="preencher('funcionario')">
          <span>Funcionário — nami@mugiwara.com</span><span class="text-treasure-200">usar →</span>
        </button>
      </div>
    </div>

    <!-- Formulário -->
    <div class="mx-auto w-full max-w-md">
      <h1 class="font-display text-4xl text-ocean-900">Entrar</h1>
      <p class="mt-1 text-ocean-500">Acesse sua conta da Mugiwara Store.</p>

      <form class="mt-8 space-y-5" @submit.prevent="entrar">
        <div>
          <label class="label" for="email">E-mail</label>
          <input id="email" v-model="email" type="email" required class="input" placeholder="voce@exemplo.com" autocomplete="email" />
        </div>
        <div>
          <label class="label" for="senha">Senha</label>
          <input id="senha" v-model="senha" type="password" required class="input" placeholder="••••••••" autocomplete="current-password" />
        </div>
        <button type="submit" class="btn-primary w-full text-base" :disabled="carregando">
          <span v-if="carregando">Içando velas...</span>
          <span v-else>Entrar</span>
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-ocean-500">
        Ainda não faz parte da tripulação?
        <RouterLink :to="{ name: 'cadastro' }" class="font-semibold text-coral-600 hover:underline">Criar conta</RouterLink>
      </p>
    </div>
  </div>
</template>
