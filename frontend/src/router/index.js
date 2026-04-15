import { createRouter, createWebHistory } from 'vue-router'
import PageVendre from '../views/PageVendre.vue'
import Register from '../views/Register.vue'
import Login from '@/views/Login.vue'
import PageAchat from '@/views/PageAchat.vue'
import HomeView from '../views/HomeView.vue'
import MesVentes from '@/views/MesVentes.vue'
import ModifierVente from '@/views/ModifierVente.vue'
import SupprimerVente from '@/views/SupprimerVente.vue'
import PageLocation from '@/views/PageLocation.vue'
import PageMettreEnLocation from '@/views/PageMettreEnLocation.vue'
import MesLocations from '@/views/MesLocations.vue'
import SupprimerLocation from '@/views/SupprimerLocation.vue'
import ModifierLocation from '@/views/ModifierLocation.vue'
import PageAchatJeu from '@/views/PageAchatJeu.vue'
import PageLouerJeu from '@/views/PageLouerJeu.vue'
import PageGestionUser from '@/views/PageGestionUser.vue'
import PagePaiementSucces from '@/views/PagePaiementSucces.vue'
import PageQuestionForum from '@/views/PageQuestionForum.vue'
import PageGestionForum from '@/views/PageGestionForum.vue'
import QuestionDetails from '@/views/QuestionDetails.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
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
      component: MesVentes,
    },
    {
      path: '/modifierVente/:id',
      name: 'modifierVente',
      component: ModifierVente,
    },
    {
      path: '/supprimerVente/:id',
      name: 'supprimerVente',
      component: SupprimerVente,
    },
    {
      path: '/mettreEnLocation',
      name: 'mettreEnLocation',
      component: PageMettreEnLocation,
    },
    {
      path: '/louer',
      name: 'louer',
      component: PageLocation,
    },
    {
      path: '/mesLocations',
      name: 'mesLocations',
      component: MesLocations,
    },
    {
      path: '/supprimerLocation/:id',
      name: 'supprimerLocation',
      component: SupprimerLocation,
    },
    {
      path: '/modifierLocation/:id',
      name: 'modifierLocation',
      component: ModifierLocation,
    },
    {
      path: '/acheter/:id',
      name: 'acheterJeu',
      component: PageAchatJeu,
    },
    {
      path: '/louer/:id',
      name: 'louerJeu',
      component: PageLouerJeu,
    },
    {
      path: '/users',
      name: 'userManager',
      component: PageGestionUser,
    },
    {
      path: '/paiement/succes',
      name: 'paiementSucces',
      component: PagePaiementSucces,
    },
    {
      path: '/forum',
      name: 'forumQuestions',
      component: PageQuestionForum,
    },
    {
      path: '/manageForum',
      name: 'forumManager',
      component: PageGestionForum,
    },
    {
      path: '/questions/:id',
      name: 'question-detail',
      component: QuestionDetails,
    },
  ],
})

export default router
