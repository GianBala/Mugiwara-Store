import axios from 'axios'

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// Base do backend (sem o /api) — usada para montar URLs de imagens estáticas.
export const BACKEND_BASE = API_URL.replace(/\/api\/?$/, '')

export const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
})

// Injeta o token JWT em todas as requisições, quando presente.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('mugiwara_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Em caso de 401, limpa a sessão local.
api.interceptors.response.use(
  (resp) => resp,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('mugiwara_token')
    }
    return Promise.reject(error)
  },
)

/** Resolve a URL de imagem (aceita URL absoluta ou caminho estático do backend). */
export function resolverImagem(caminho: string | null | undefined): string {
  if (!caminho) {
    return 'https://images.unsplash.com/photo-1608889175123-8ee362201f81?w=600&q=80'
  }
  if (caminho.startsWith('http')) return caminho
  return `${BACKEND_BASE}${caminho}`
}
