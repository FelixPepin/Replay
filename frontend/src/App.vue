<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
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
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 shadow-sm">
      <div class="container-fluid container">
        <button @click="sidebarOuverte = !sidebarOuverte" class="btn text-white me-3 p-0 fs-4">
          ☰
        </button>
        <a class="navbar-brand fw-bold fs-3 text-warning me-auto" href="/">RePlay</a>

        <div class="d-flex align-items-center">
          <RouterLink v-if="auth.role === 'admin'" to="/manageForum" class="nav-link text-white me-3 text-uppercase fw-bold">Gestion du forum</RouterLink>
          <RouterLink v-if="auth.role === 'admin'" to="/users" class="nav-link text-white me-3 text-uppercase fw-bold">Gestion des utilisateurs</RouterLink>
          <RouterLink to="/achat" class="nav-link text-white me-3 text-uppercase fw-bold">Acheter</RouterLink>
          <RouterLink to="/louer" class="nav-link text-white me-3 text-uppercase fw-bold">Louer</RouterLink>
          <RouterLink to="/forum" class="nav-link text-white me-3 text-uppercase fw-bold">Forum</RouterLink>
          <RouterLink v-if="auth.role === 'vendeur'" to="/vendre" class="nav-link text-white me-3 text-uppercase fw-bold">Vendre</RouterLink>
          <div class="ms-2 d-flex gap-2">
            <RouterLink v-if="!auth.estConnecte" to="/register" class="btn btn-outline-warning btn-sm">
              Inscription
            </RouterLink>
            <RouterLink v-if="!auth.estConnecte" to="/login" class="btn btn-outline-warning btn-sm">
              Connexion
            </RouterLink>
            <button v-if="auth.estConnecte" @click="deconnecter" class="btn btn-info btn-sm fw-bold text-uppercase">
              Se déconnecter
              <i class="fi fi-br-leave"></i>
            </button>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <div v-if="sidebarOuverte" @click="sidebarOuverte = false" class="sidebar-overlay"></div>
  <div class="app-layout">
    <aside
      :class="['sidebar', 'bg-dark', 'text-white', 'd-flex', 'flex-column', 'py-4', 'px-3', { 'sidebar-open': sidebarOuverte }]">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <span class="fw-bold fs-5 text-warning">Replay</span>
        <button @click="sidebarOuverte = false" class="btn text-white p-0 fs-4">✕</button>
      </div>
      <nav class="d-flex flex-column flex-grow-1">

        <p class="text-uppercase text-secondary small mb-1 mt-3">Achat</p>
        <RouterLink to="/achat" class="sidebar-link rounded text-decoration-none p-1">
          <i class="fi fi-br-selling"></i>
          Acheter
        </RouterLink>
        <template v-if="auth.estConnecte && auth.role === 'vendeur'">
          <p class="text-uppercase text-secondary small mb-1 mt-3">Vendre</p>
          <RouterLink to="/vendre" class="sidebar-link rounded text-decoration-none p-1">
            <i class="fi fi-br-dollar"></i>
            Mettre en vente
          </RouterLink>
          <RouterLink to="/mesVentes" class="sidebar-link rounded text-decoration-none p-1">
            <i class="fi fi-br-point-of-sale-bill"></i>
            Mes ventes
          </RouterLink>
          <p class="text-uppercase text-secondary small mb-1 mt-3">Location</p>
          <RouterLink to="/louer" class="sidebar-link rounded text-decoration-none p-1">
            <i class="fi fi-br-rent"></i>
            Louer
          </RouterLink>
          <RouterLink to="/mettreEnLocation" class="sidebar-link rounded text-decoration-none p-1">
            <i class="fi fi-br-hand-key"></i>
            Mettre en location
          </RouterLink>
          <RouterLink to="/mesLocations" class="sidebar-link rounded text-decoration-none p-1">
            <i class="fi fi-br-document"></i>
            Mes locations
          </RouterLink>
        </template>

      </nav>

      <div class="mt-auto pt-3 border-top border-secondary">
        <template v-if="!auth.estConnecte">
          <RouterLink to="/register" class="btn btn-outline-warning btn-sm w-100 mb-2 fw-bold text-uppercase">
            Inscription
            <i class="fi fi-br-enter"></i>
          </RouterLink>
          <RouterLink to="/login" class="btn btn-outline-light btn-sm w-100 fw-bold text-uppercase">
            Connexion
            <i class="fi fi-br-insert-alt"></i>
          </RouterLink>
        </template>
        <template v-else>
          <p class="text-secondary small mb-2 text-uppercase">Connecté</p>
          <button @click="deconnecter" class="btn btn-danger btn-sm w-100 fw-bold text-uppercase">
            Se déconnecter
            <i class="fi fi-br-leave"></i>
          </button>
        </template>
      </div>
    </aside>

    <div class="main-content d-flex flex-column">
      <RouterView />
      <footer class="footer mt-auto py-5 text-white">
        <div class="container">
          <div class="row g-4">
            <div class="col-lg-4 col-md-6">
              <h4 class="fw-bold text-warning mb-3">RePlay</h4>
              <p class="opacity-75">« Rejoue mieux en donnant une seconde vie aux jeux. »</p>
              <p class="small opacity-50">
                La première plateforme hybride dédiée à la durabilité dans l'univers du gaming.
              </p>
            </div>

            <div class="col-lg-2 col-md-6">
              <h5 class="fw-bold mb-3">Explorer</h5>
              <ul class="list-unstyled opacity-75">
                <li class="mb-2">
                  <RouterLink to="/achat" class="text-white text-decoration-none hover-warning">Acheter</RouterLink>
                </li>
                <li class="mb-2">
                  <RouterLink to="/vendre" class="text-white text-decoration-none hover-warning">Vendre</RouterLink>
                </li>
                <li class="mb-2">
                  <RouterLink to="/louer" class="text-white text-decoration-none hover-warning">Louer</RouterLink>
                </li>
              </ul>
            </div>

            <div class="col-lg-2 col-md-6">
              <h5 class="fw-bold mb-3">Support</h5>
              <ul class="list-unstyled opacity-75">
                <li class="mb-2"><a href="#" class="text-white text-decoration-none">FAQ</a></li>
                <li class="mb-2">
                  <a href="#" class="text-white text-decoration-none">Système d'évaluations</a>
                </li>
                <li class="mb-2">
                  <a href="#" class="text-white text-decoration-none">Protection Acheteur</a>
                </li>
              </ul>
            </div>

            <div class="col-lg-4 col-md-6">
              <h5 class="fw-bold mb-3">Restez au courant</h5>
              <p class="small opacity-75">
                Recevez les meilleures offres de jeux usagés avant tout le monde.
              </p>
              <div class="input-group mb-3 shadow-sm">
                <input type="text" class="form-control border-0" placeholder="Ton courriel" aria-label="Email" />
                <button class="btn btn-warning fw-bold" type="button">OK</button>
              </div>
            </div>
          </div>

          <hr class="my-5 opacity-25" />

          <div class="d-flex flex-column flex-sm-row justify-content-between align-items-center opacity-50 small">
            <p>&copy; 2024 RePlay Inc. Tous droits réservés.</p>
            <ul class="list-inline mb-0">
              <li class="list-inline-item me-4">Confidentialité</li>
              <li class="list-inline-item">Conditions d'utilisation</li>
            </ul>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<style>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 240px;
  z-index: 1050;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.main-content {
  flex: 1;
  overflow-x: hidden;
}

.sidebar-open {
  transform: translateX(0);
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}

.app-layout {
  display: flex;
  min-height: 100vh;
}

body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.nav-link:hover {
  color: #ffca28 !important;
}

.dropdown-menu {
  animation: dropdownFadeIn 0.2s ease forwards;
  transform-origin: top center;
}

@keyframes dropdownFadeIn {
  from {
    opacity: 0;
    transform: translateY(-6px) scaleY(0.95);
  }

  to {
    opacity: 1;
    transform: translateY(0) scaleY(1);
  }
}

.dropdown-item {
  transition: background-color 0.15s ease, color 0.15s ease;
}
</style>
