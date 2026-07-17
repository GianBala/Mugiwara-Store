<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import { extrairErro } from '@/utils/format'
import StrawHatIcon from '@/components/StrawHatIcon.vue'

const auth = useAuthStore()
const toast = useToastStore()
const router = useRouter()

const form = ref({
  nome: '',
  email: '',
  senha: '',
  cep: '',
  numero_endereco: '',
  complemento_endereco: '',
  telefone: '',
  torce_flamengo: false,
  assiste_one_piece: false,
  natural_de_sousa: false,
})
const carregando = ref(false)

async function cadastrar() {
  carregando.value = true
  try {
    const payload = {
      nome: form.value.nome,
      email: form.value.email,
      senha: form.value.senha,
      cep: form.value.cep || null,
      numero_endereco: form.value.numero_endereco || null,
      complemento_endereco: form.value.complemento_endereco || null,
      telefones: form.value.telefone ? [form.value.telefone] : [],
      torce_flamengo: form.value.torce_flamengo,
      assiste_one_piece: form.value.assiste_one_piece,
      natural_de_sousa: form.value.natural_de_sousa,
    }
    await api.post('/auth/register', payload)
    // Login automático após cadastro
    await auth.login(form.value.email, form.value.senha)
    toast.sucesso('Conta criada! Bem-vindo à tripulação! 🏴‍☠️')
    router.push({ name: 'home' })
  } catch (e) {
    toast.erro(extrairErro(e, 'Não foi possível criar a conta.'))
  } finally {
    carregando.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-2xl px-6 py-10">
    <div class="mb-8 flex flex-col items-center text-center">
      <StrawHatIcon class="h-12 w-12" />
      <h1 class="mt-3 font-display text-4xl text-ocean-900">Junte-se à tripulação</h1>
      <p class="mt-1 text-ocean-500">Crie sua conta e ganhe descontos exclusivos de nakama.</p>
    </div>

    <form class="card space-y-6 p-6 sm:p-8" @submit.prevent="cadastrar">
      <!-- Dados de acesso -->
      <div>
        <h2 class="mb-4 flex items-center gap-2 font-display text-2xl text-ocean-800">
          <span class="grid h-7 w-7 place-items-center rounded-full bg-coral-500 text-sm text-white">1</span> Dados de acesso
        </h2>
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="sm:col-span-2">
            <label class="label">Nome completo *</label>
            <input v-model="form.nome" required class="input" placeholder="Monkey D. Luffy" />
          </div>
          <div>
            <label class="label">E-mail *</label>
            <input v-model="form.email" type="email" required class="input" placeholder="voce@exemplo.com" />
          </div>
          <div>
            <label class="label">Senha * (mín. 6)</label>
            <input v-model="form.senha" type="password" required minlength="6" class="input" placeholder="••••••••" />
          </div>
        </div>
      </div>

      <!-- Endereço -->
      <div>
        <h2 class="mb-4 flex items-center gap-2 font-display text-2xl text-ocean-800">
          <span class="grid h-7 w-7 place-items-center rounded-full bg-coral-500 text-sm text-white">2</span> Endereço
        </h2>
        <div class="grid gap-4 sm:grid-cols-3">
          <div>
            <label class="label">CEP</label>
            <input v-model="form.cep" class="input" placeholder="58800-000" maxlength="9" />
          </div>
          <div>
            <label class="label">Número</label>
            <input v-model="form.numero_endereco" class="input" placeholder="100" />
          </div>
          <div>
            <label class="label">Complemento</label>
            <input v-model="form.complemento_endereco" class="input" placeholder="Casa / Apto" />
          </div>
          <div class="sm:col-span-3">
            <label class="label">Telefone</label>
            <input v-model="form.telefone" class="input" placeholder="(83) 99999-0000" />
          </div>
        </div>
        <p class="mt-2 text-xs text-ocean-400">O logradouro é preenchido automaticamente a partir do CEP.</p>
      </div>

      <!-- Descontos -->
      <div>
        <h2 class="mb-2 flex items-center gap-2 font-display text-2xl text-ocean-800">
          <span class="grid h-7 w-7 place-items-center rounded-full bg-treasure-400 text-sm text-ocean-950">★</span> Descontos de nakama
        </h2>
        <p class="mb-4 text-sm text-ocean-500">Marque o que se aplica a você e ganhe <strong>10% de desconto</strong> nas compras:</p>
        <div class="grid gap-3 sm:grid-cols-3">
          <label class="flex cursor-pointer items-center gap-3 rounded-xl border-2 border-ocean-100 p-3 transition hover:border-treasure-300 has-[:checked]:border-treasure-400 has-[:checked]:bg-treasure-50">
            <input v-model="form.assiste_one_piece" type="checkbox" class="h-5 w-5 accent-coral-500" />
            <span class="text-sm font-semibold">⚓ Assisto One Piece</span>
          </label>
          <label class="flex cursor-pointer items-center gap-3 rounded-xl border-2 border-ocean-100 p-3 transition hover:border-treasure-300 has-[:checked]:border-treasure-400 has-[:checked]:bg-treasure-50">
            <input v-model="form.torce_flamengo" type="checkbox" class="h-5 w-5 accent-coral-500" />
            <span class="text-sm font-semibold">🔴 Torço pelo Flamengo</span>
          </label>
          <label class="flex cursor-pointer items-center gap-3 rounded-xl border-2 border-ocean-100 p-3 transition hover:border-treasure-300 has-[:checked]:border-treasure-400 has-[:checked]:bg-treasure-50">
            <input v-model="form.natural_de_sousa" type="checkbox" class="h-5 w-5 accent-coral-500" />
            <span class="text-sm font-semibold">🏴‍☠️ Sou de Sousa-PB</span>
          </label>
        </div>
      </div>

      <button type="submit" class="btn-primary w-full text-base" :disabled="carregando">
        <span v-if="carregando">Criando conta...</span>
        <span v-else>Criar conta e embarcar</span>
      </button>
      <p class="text-center text-sm text-ocean-500">
        Já tem conta?
        <RouterLink :to="{ name: 'login' }" class="font-semibold text-coral-600 hover:underline">Entrar</RouterLink>
      </p>
    </form>
  </div>
</template>
