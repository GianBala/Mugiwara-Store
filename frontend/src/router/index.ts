import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
    { path: '/produto/:id', name: 'produto', component: () => import('@/views/ProductDetailView.vue') },
    { path: '/carrinho', name: 'carrinho', component: () => import('@/views/CartView.vue') },
    { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
    { path: '/cadastro', name: 'cadastro', component: () => import('@/views/RegisterView.vue') },
    {
      path: '/pedidos',
      name: 'pedidos',
      component: () => import('@/views/OrdersView.vue'),
      meta: { requerCliente: true },
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requerCliente: true },
    },
    {
      path: '/painel',
      name: 'painel',
      component: () => import('@/views/admin/DashboardView.vue'),
      meta: { requerFuncionario: true },
    },
    {
      path: '/painel/produtos',
      name: 'painel-produtos',
      component: () => import('@/views/admin/ProductsAdminView.vue'),
      meta: { requerFuncionario: true },
    },
    {
      path: '/painel/relatorios',
      name: 'painel-relatorios',
      component: () => import('@/views/admin/ReportsView.vue'),
      meta: { requerFuncionario: true },
    },
    { path: '/:pathMatch(.*)*', name: 'nao-encontrado', component: () => import('@/views/NotFoundView.vue') },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requerFuncionario && !auth.ehFuncionario) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.requerCliente && !auth.ehCliente) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  return true
})

export default router
