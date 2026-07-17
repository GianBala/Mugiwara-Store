import { defineStore } from 'pinia'
import { api } from '@/api/client'
import type { TokenResposta } from '@/types'

interface AuthState {
  token: string | null
  role: 'cliente' | 'funcionario' | null
  nome: string | null
  uid: number | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('mugiwara_token'),
    role: (localStorage.getItem('mugiwara_role') as AuthState['role']) || null,
    nome: localStorage.getItem('mugiwara_nome'),
    uid: localStorage.getItem('mugiwara_uid') ? Number(localStorage.getItem('mugiwara_uid')) : null,
  }),
  getters: {
    autenticado: (s) => !!s.token,
    ehFuncionario: (s) => s.role === 'funcionario',
    ehCliente: (s) => s.role === 'cliente',
  },
  actions: {
    async login(email: string, senha: string) {
      // O endpoint de login usa OAuth2 password flow (form-urlencoded).
      const params = new URLSearchParams()
      params.append('username', email)
      params.append('password', senha)
      const { data } = await api.post<TokenResposta>('/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      this.aplicarSessao(data)
    },
    aplicarSessao(data: TokenResposta) {
      this.token = data.access_token
      this.role = data.role
      this.nome = data.nome
      this.uid = data.uid
      localStorage.setItem('mugiwara_token', data.access_token)
      localStorage.setItem('mugiwara_role', data.role)
      localStorage.setItem('mugiwara_nome', data.nome)
      localStorage.setItem('mugiwara_uid', String(data.uid))
    },
    logout() {
      this.token = null
      this.role = null
      this.nome = null
      this.uid = null
      localStorage.removeItem('mugiwara_token')
      localStorage.removeItem('mugiwara_role')
      localStorage.removeItem('mugiwara_nome')
      localStorage.removeItem('mugiwara_uid')
    },
  },
})
