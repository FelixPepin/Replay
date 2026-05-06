<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
import '@/assets/main.css'
const auth = useAuthStore()
const notif = useNotifStore()
const router = useRouter()
const message = ref('')
const estConnecte = computed(() => !!localStorage.getItem('token'))
const sidebarOuverte = ref(false)
onMounted(() => {
  message.value = history.state.success || ''
})

function deconnecter() {
  auth.deconnecter()
  notif.setNotif('Vous avez été déconnecté.', 'info')
  router.push('/')
}
</script>


<template>
  <header>
    <nav class="navbar-pill">
      <button @click="sidebarOuverte = !sidebarOuverte" class="navbar-menu-btn">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
          <line x1="2" y1="4" x2="14" y2="4" />
          <line x1="2" y1="8" x2="14" y2="8" />
          <line x1="2" y1="12" x2="14" y2="12" />
        </svg>
      </button>

      <a class="navbar-brand" href="/">RePlay</a>

      <div class="navbar-links">
        <RouterLink to="/achat" class="navbar-link">Acheter</RouterLink>
        <RouterLink to="/louer" class="navbar-link">Louer</RouterLink>
        <RouterLink to="/quiz" class="navbar-link">Quiz</RouterLink>
        <RouterLink to="/forum" class="navbar-link">Forum</RouterLink>
      </div>

      <div class="navbar-actions">
        <template v-if="!auth.estConnecte">
          <RouterLink to="/login" class="navbar-link">Connexion</RouterLink>
          <RouterLink to="/register" class="navbar-btn">Inscription</RouterLink>
        </template>
        <template v-else>
          <span class="navbar-user">{{ auth.nomUtilisateur }}</span>
          <button @click="deconnecter" class="navbar-btn navbar-btn-danger">
            Se déconnecter
          </button>
        </template>
      </div>
    </nav>
  </header>
  <div v-if="sidebarOuverte" @click="sidebarOuverte = false" class="sidebar-overlay"></div>
  <div class="app-layout">
    <aside :class="['sidebar', { 'sidebar-open': sidebarOuverte }]">
      <div class="sb-top">
        <span class="sb-brand">RePlay</span>
        <button @click="sidebarOuverte = false" class="sb-close">✕</button>
      </div>

      <nav class="sb-body" @click="sidebarOuverte = false">
        <p class="sb-section">Découverte</p>
        <RouterLink to="/quiz" class="sb-link">
          <i class="fi fi-br-gamepad"></i>
          Quiz Jeux Vidéo
        </RouterLink>

        <p class="sb-section">Catalogue</p>
        <RouterLink to="/achat" class="sb-link">
          <i class="fi fi-br-shopping-cart"></i>
          Acheter
        </RouterLink>
        <RouterLink to="/louer" class="sb-link">
          <i class="fi fi-br-rent"></i>
          Louer
        </RouterLink>
        <RouterLink to="/forum" class="sb-link">
          <i class="fi fi-br-comment"></i>
          Forum
        </RouterLink>

        <template v-if="auth.estConnecte">
          <p class="sb-section">Ventes</p>
          <RouterLink to="/vendre" class="sb-link">
            <i class="fi fi-br-dollar"></i>
            Mettre en vente
          </RouterLink>
          <RouterLink to="/mesVentes" class="sb-link">
            <i class="fi fi-br-point-of-sale-bill"></i>
            Mes ventes
          </RouterLink>

          <p class="sb-section">Locations</p>
          <RouterLink to="/mettreEnLocation" class="sb-link">
            <i class="fi fi-br-hand-key"></i>
            Mettre en location
          </RouterLink>
          <RouterLink to="/mesLocations" class="sb-link">
            <i class="fi fi-br-document"></i>
            Mes locations
          </RouterLink>

          <p class="sb-section">Évaluation</p>
          <RouterLink to="/mesEvaluations" class="sb-link">
            <i class="fi fi-br-star"></i>
            Évaluer un vendeur
          </RouterLink>

          <p class="sb-section">Mon compte</p>
          <RouterLink to="/profil" class="sb-link">
            <i class="fi fi-br-user"></i>
            Mon profil
          </RouterLink>
        </template>
        <template v-if="auth.role === 'admin'">

          <p class="sb-section">Administration</p>
          <RouterLink to="/manageForum" class="sb-link">
            <i class="fi fi-br-settings"></i>
            Gestion du forum
          </RouterLink>
          <RouterLink to="/users" class="sb-link">
            <i class="fi fi-br-users"></i>
            Gestion des utilisateurs
          </RouterLink>
        </template>
      </nav>

      <div class="sb-footer">
        <div class="sb-avatar" v-if="auth.estConnecte">
          <div class="sb-avatar-circle">{{ auth.initiales }}</div>
          <div>
            <div class="sb-avatar-name">{{ auth.nom }}</div>
            <div class="sb-avatar-role">{{ auth.role }}</div>
          </div>
        </div>
        <button v-if="auth.estConnecte" @click="deconnecter" class="sb-logout">Se déconnecter</button>
        <RouterLink v-if="!auth.estConnecte" to="/login" class="sb-logout">
          Connexion
        </RouterLink>
      </div>
    </aside>
    <div class="main-content d-flex flex-column">
      <RouterView />
      <footer class="site-footer mt-5">
        <div class="footer-inner">

          <div class="footer-brand">
            <span class="footer-logo">RePlay</span>
            <p class="footer-tagline">« Rejoue mieux en donnant une seconde vie aux jeux. »</p>
            <p class="footer-desc">La première plateforme hybride dédiée à la durabilité dans l'univers du gaming.</p>
          </div>

          <div class="footer-col">
            <p class="footer-heading">Explorer</p>
            <RouterLink to="/achat" class="footer-link">Acheter</RouterLink>
            <RouterLink to="/vendre" class="footer-link">Vendre</RouterLink>
            <RouterLink to="/louer" class="footer-link">Louer</RouterLink>
            <RouterLink to="/forum" class="footer-link">Forum</RouterLink>
          </div>

          <div class="footer-col">
            <p class="footer-heading">Support</p>
            <a href="#" class="footer-link">FAQ</a>
            <a href="#" class="footer-link">Système d'évaluations</a>
            <a href="#" class="footer-link">Protection Acheteur</a>
            <a href="#" class="footer-link">Nous contacter</a>
          </div>

          <div class="footer-col footer-newsletter">
            <p class="footer-heading">Restez au courant</p>
            <p class="footer-desc">Recevez les meilleures offres avant tout le monde.</p>
            <div class="footer-input-group">
              <input type="email" placeholder="Ton courriel" class="footer-input" />
              <button class="footer-input-btn">OK</button>
            </div>
          </div>

        </div>

        <div class="footer-bottom">
          <span>© 2026 RePlay Inc. Tous droits réservés.</span>
          <div class="footer-bottom-links">
            <a href="#" class="footer-bottom-link">Confidentialité</a>
            <a href="#" class="footer-bottom-link">Conditions d'utilisation</a>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>
