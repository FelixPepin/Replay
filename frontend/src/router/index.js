import { createRouter, createWebHistory } from 'vue-router'
import PageVendre from '../views/PageVendre.vue' 
import Register from '../views/Register.vue'
import Login from '@/views/Login.vue'
import PageAchat from '@/views/PageAchat.vue'
import MesVentes from '@/views/MesVentes.vue'
import ModifierVente from '@/views/ModifierVente.vue'
import SupprimerVente from '@/views/SupprimerVente.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/vendre',
      name: 'vendre',
      component: PageVendre,
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/achat',
      name: 'achat',
      component: PageAchat,
    },
    {
      path: '/mesVentes',
      name: 'mesVentes',
      component: MesVentes
    },
    {
      path: "/modifier/:id",
      name: "modifierVente",
      component: ModifierVente
    },
    {
      path: "/supprimer/:id",
      name: "supprimerVente",
      component: SupprimerVente
    }
  ],
})

export default router
