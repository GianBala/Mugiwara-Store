<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api, resolverImagem } from '@/api/client'
import { moeda, extrairErro } from '@/utils/format'
import { useToastStore } from '@/stores/toast'
import AdminTabs from '@/components/AdminTabs.vue'
import type { Produto, ProdutoInput } from '@/types'

const toast = useToastStore()

const produtos = ref<Produto[]>([])
const carregando = ref(true)
const busca = ref('')

const modalAberto = ref(false)
const editandoId = ref<number | null>(null)
const salvando = ref(false)
const enviandoImagem = ref(false)
const modoImagem = ref<'url' | 'upload'>('url')

const form = reactive<ProdutoInput>({
  nome: '',
  descricao: '',
  preco: 0,
  quantidade_estoque: 0,
  categoria: '',
  fabricado_em_mari: false,
  imagem: '',
})

// Confirmação de exclusão
const confirmandoExclusao = ref<Produto | null>(null)

async function carregar() {
  carregando.value = true
  try {
    const { data } = await api.get<Produto[]>('/produtos', { params: busca.value ? { busca: busca.value } : {} })
    produtos.value = data
  } catch (e) {
    toast.erro(extrairErro(e))
  } finally {
    carregando.value = false
  }
}

function abrirCriar() {
  editandoId.value = null
  Object.assign(form, { nome: '', descricao: '', preco: 0, quantidade_estoque: 0, categoria: '', fabricado_em_mari: false, imagem: '' })
  modoImagem.value = 'url'
  modalAberto.value = true
}

function abrirEditar(p: Produto) {
  editandoId.value = p.id_produto
  Object.assign(form, {
    nome: p.nome,
    descricao: p.descricao || '',
    preco: p.preco,
    quantidade_estoque: p.quantidade_estoque,
    categoria: p.categoria,
    fabricado_em_mari: p.fabricado_em_mari,
    imagem: p.imagem || '',
  })
  modoImagem.value = 'url'
  modalAberto.value = true
}

async function enviarImagem(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files?.length) return
  enviandoImagem.value = true
  try {
    const fd = new FormData()
    fd.append('arquivo', input.files[0])
    const { data } = await api.post('/uploads/imagem', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    form.imagem = data.url
    toast.sucesso('Imagem enviada com sucesso!')
  } catch (err) {
    toast.erro(extrairErro(err, 'Falha no upload da imagem.'))
  } finally {
    enviandoImagem.value = false
  }
}

async function salvar() {
  salvando.value = true
  try {
    const payload = { ...form, preco: Number(form.preco), quantidade_estoque: Number(form.quantidade_estoque) }
    if (editandoId.value) {
      await api.put(`/produtos/${editandoId.value}`, payload)
      toast.sucesso('Produto atualizado!')
    } else {
      await api.post('/produtos', payload)
      toast.sucesso('Produto cadastrado!')
    }
    modalAberto.value = false
    carregar()
  } catch (e) {
    toast.erro(extrairErro(e, 'Verifique os dados do produto.'))
  } finally {
    salvando.value = false
  }
}

async function excluir() {
  if (!confirmandoExclusao.value) return
  try {
    await api.delete(`/produtos/${confirmandoExclusao.value.id_produto}`)
    toast.sucesso('Produto removido.')
    confirmandoExclusao.value = null
    carregar()
  } catch (e) {
    toast.erro(extrairErro(e))
  }
}

onMounted(carregar)
</script>

<template>
  <div class="mx-auto max-w-6xl px-6 py-10">
    <div class="mb-6">
      <h1 class="font-display text-4xl text-ocean-900">Gestão de Produtos</h1>
      <p class="mt-1 text-ocean-500">Cadastre, edite e remova os tesouros do catálogo.</p>
    </div>

    <AdminTabs />

    <!-- Barra de ações -->
    <div class="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="relative w-full sm:w-72">
        <svg class="pointer-events-none absolute left-3.5 top-1/2 h-5 w-5 -translate-y-1/2 text-ocean-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.2-5.2m2.2-5.3a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0Z" />
        </svg>
        <input v-model="busca" class="input pl-11" placeholder="Buscar produto..." @input="carregar" />
      </div>
      <button class="btn-primary" @click="abrirCriar">
        <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        Novo produto
      </button>
    </div>

    <!-- Tabela -->
    <div class="mt-6 card overflow-hidden">
      <div v-if="carregando" class="p-8">
        <div v-for="n in 5" :key="n" class="mb-3 h-12 animate-pulse rounded-lg bg-ocean-100/70" />
      </div>
      <table v-else class="w-full text-sm">
        <thead class="bg-ocean-50 text-left text-ocean-400">
          <tr>
            <th class="px-4 py-3 font-semibold">Produto</th>
            <th class="hidden px-4 py-3 font-semibold md:table-cell">Categoria</th>
            <th class="px-4 py-3 text-center font-semibold">Estoque</th>
            <th class="px-4 py-3 text-right font-semibold">Preço</th>
            <th class="px-4 py-3 text-right font-semibold">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-ocean-100">
          <tr v-for="p in produtos" :key="p.id_produto" class="hover:bg-ocean-50/50">
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <img :src="resolverImagem(p.imagem)" :alt="p.nome" class="h-11 w-11 rounded-lg object-cover" />
                <span class="font-medium text-ocean-800">{{ p.nome }}</span>
              </div>
            </td>
            <td class="hidden px-4 py-3 text-ocean-500 md:table-cell">{{ p.categoria }}</td>
            <td class="px-4 py-3 text-center">
              <span class="badge" :class="p.quantidade_estoque < 5 ? 'bg-coral-100 text-coral-700' : 'bg-emerald-100 text-emerald-700'">
                {{ p.quantidade_estoque }}
              </span>
            </td>
            <td class="px-4 py-3 text-right font-semibold text-ocean-700">{{ moeda(p.preco) }}</td>
            <td class="px-4 py-3">
              <div class="flex justify-end gap-1">
                <button class="rounded-lg p-2 text-ocean-500 hover:bg-ocean-100 hover:text-ocean-800" @click="abrirEditar(p)" aria-label="Editar">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.86 4.49 2.65 2.65m-2.03-3.28a1.87 1.87 0 1 1 2.65 2.65L7.5 21.4l-3.75.94.94-3.75L16.48 3.86Z" />
                  </svg>
                </button>
                <button class="rounded-lg p-2 text-coral-500 hover:bg-coral-100" @click="confirmandoExclusao = p" aria-label="Excluir">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.35 9m-4.78 0L9.26 9M18.16 5.79 17.09 19.67a2.25 2.25 0 0 1-2.24 2.08H8.08a2.25 2.25 0 0 1-2.24-2.08L4.77 5.79m14.46 0a48.11 48.11 0 0 0-3.48-.4m-11 .4c.34-.07.68-.13 1.02-.19m9.96 0V4.87c0-1.18-.91-2.16-2.09-2.2a51.96 51.96 0 0 0-3.32 0c-1.18.04-2.09 1.02-2.09 2.2v.92" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!produtos.length">
            <td colspan="5" class="px-4 py-10 text-center text-ocean-400">Nenhum produto encontrado.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL DE FORMULÁRIO -->
    <transition name="modal">
      <div v-if="modalAberto" class="fixed inset-0 z-[80] flex items-center justify-center bg-ocean-950/60 p-4 backdrop-blur-sm" @click.self="modalAberto = false">
        <div class="max-h-[92vh] w-full max-w-lg overflow-y-auto rounded-3xl bg-white shadow-card-hover">
          <div class="sticky top-0 flex items-center justify-between border-b border-ocean-100 bg-white px-6 py-4">
            <h2 class="font-display text-2xl text-ocean-900">{{ editandoId ? 'Editar produto' : 'Novo produto' }}</h2>
            <button class="text-ocean-400 hover:text-coral-600" @click="modalAberto = false">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M6 18 18 6M6 6l12 12" /></svg>
            </button>
          </div>

          <form class="space-y-4 p-6" @submit.prevent="salvar">
            <div>
              <label class="label">Nome *</label>
              <input v-model="form.nome" required class="input" placeholder="Action Figure Luffy Gear 5" />
            </div>
            <div>
              <label class="label">Descrição</label>
              <textarea v-model="form.descricao" rows="2" class="input" placeholder="Descrição do produto"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="label">Preço (R$) *</label>
                <input v-model.number="form.preco" type="number" min="0.01" step="0.01" required class="input" />
              </div>
              <div>
                <label class="label">Estoque *</label>
                <input v-model.number="form.quantidade_estoque" type="number" min="0" required class="input" />
              </div>
            </div>
            <div>
              <label class="label">Categoria *</label>
              <input v-model="form.categoria" required class="input" placeholder="Action Figures" list="categorias" />
              <datalist id="categorias">
                <option value="Action Figures" /><option value="Réplicas" /><option value="Pôsteres" />
                <option value="Colecionáveis" /><option value="Vestuário" />
              </datalist>
            </div>

            <!-- Imagem: URL ou upload (CA-05) -->
            <div>
              <label class="label">Imagem</label>
              <div class="mb-2 flex gap-2">
                <button type="button" class="chip" :class="modoImagem === 'url' ? 'chip-active' : 'chip-idle'" @click="modoImagem = 'url'">URL externa</button>
                <button type="button" class="chip" :class="modoImagem === 'upload' ? 'chip-active' : 'chip-idle'" @click="modoImagem = 'upload'">Upload local</button>
              </div>
              <input v-if="modoImagem === 'url'" v-model="form.imagem" class="input" placeholder="https://..." />
              <div v-else>
                <input type="file" accept="image/*" class="input !py-2 file:mr-3 file:rounded-md file:border-0 file:bg-ocean-100 file:px-3 file:py-1.5 file:font-semibold file:text-ocean-700" @change="enviarImagem" />
                <p v-if="enviandoImagem" class="mt-1 text-xs text-treasure-600">Enviando imagem...</p>
              </div>
              <img v-if="form.imagem" :src="resolverImagem(form.imagem)" class="mt-3 h-24 w-24 rounded-xl object-cover ring-1 ring-ocean-100" />
            </div>

            <label class="flex cursor-pointer items-center gap-3 rounded-xl border-2 border-ocean-100 p-3 has-[:checked]:border-treasure-400 has-[:checked]:bg-treasure-50">
              <input v-model="form.fabricado_em_mari" type="checkbox" class="h-5 w-5 accent-coral-500" />
              <span class="text-sm font-semibold">★ Edição especial "Fabricado em Mari"</span>
            </label>

            <div class="flex gap-3 pt-2">
              <button type="button" class="btn-outline flex-1" @click="modalAberto = false">Cancelar</button>
              <button type="submit" class="btn-primary flex-1" :disabled="salvando || enviandoImagem">
                {{ salvando ? 'Salvando...' : 'Salvar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- MODAL DE EXCLUSÃO -->
    <transition name="modal">
      <div v-if="confirmandoExclusao" class="fixed inset-0 z-[80] flex items-center justify-center bg-ocean-950/60 p-4 backdrop-blur-sm" @click.self="confirmandoExclusao = null">
        <div class="w-full max-w-sm rounded-3xl bg-white p-6 text-center shadow-card-hover">
          <div class="mx-auto grid h-14 w-14 place-items-center rounded-full bg-coral-100 text-3xl">🗑️</div>
          <h3 class="mt-4 font-display text-2xl text-ocean-900">Remover produto?</h3>
          <p class="mt-2 text-sm text-ocean-500">Tem certeza que deseja remover <strong>{{ confirmandoExclusao.nome }}</strong>? Esta ação não pode ser desfeita.</p>
          <div class="mt-6 flex gap-3">
            <button class="btn-outline flex-1" @click="confirmandoExclusao = null">Cancelar</button>
            <button class="btn-primary flex-1" @click="excluir">Remover</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
