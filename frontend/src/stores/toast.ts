import { defineStore } from 'pinia'

export interface Toast {
  id: number
  tipo: 'sucesso' | 'erro' | 'info'
  mensagem: string
}

let contador = 0

export const useToastStore = defineStore('toast', {
  state: () => ({ toasts: [] as Toast[] }),
  actions: {
    mostrar(mensagem: string, tipo: Toast['tipo'] = 'info') {
      const id = ++contador
      this.toasts.push({ id, tipo, mensagem })
      setTimeout(() => this.remover(id), 3800)
    },
    sucesso(msg: string) {
      this.mostrar(msg, 'sucesso')
    },
    erro(msg: string) {
      this.mostrar(msg, 'erro')
    },
    remover(id: number) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },
  },
})
