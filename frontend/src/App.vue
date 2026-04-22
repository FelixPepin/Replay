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
          <RouterLink to="/achat" class="nav-link text-white me-3 text-uppercase fw-bold">Acheter</RouterLink>
          <RouterLink to="/louer" class="nav-link text-white me-3 text-uppercase fw-bold">Louer</RouterLink>
          <RouterLink to="/forum" class="nav-link text-white me-3 text-uppercase fw-bold">Forum</RouterLink>
          <RouterLink v-if="auth.role === 'vendeur'" to="/vendre"
            class="nav-link text-white me-3 text-uppercase fw-bold">Vendre</RouterLink>
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
            <p>&copy; 2026 RePlay Inc. Tous droits réservés.</p>
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
.sb-link i {
  font-size: 15px;
  opacity: 0.7;
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.sb-link:hover i,
.sb-link.router-link-active i {
  opacity: 1;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 240px;
  z-index: 1050;
  transform: translateX(-100%);
  transition: transform 0.25s ease;
  background: #1a1f2e;
  display: flex;
  flex-direction: column;
}

.sidebar-open {
  transform: translateX(0);
}

.sb-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 0.5px solid rgba(255, 255, 255, 0.08);
}

.sb-brand {
  font-size: 16px;
  font-weight: 500;
  color: #f5c33b;
}

.sb-close {
  background: none;
  border: none;
  color: #8892a4;
  cursor: pointer;
  font-size: 16px;
}

.sb-close:hover {
  color: #c8cdd8;
}

.sb-body {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.sb-section {
  padding: 16px 16px 4px;
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: #4e5568;
  margin: 0;
}

.sb-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 16px;
  color: #9aa0af;
  text-decoration: none;
  font-size: 13px;
  transition: background 0.12s, color 0.12s;
}

.sb-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #e0e4ed;
}

.sb-link.router-link-active {
  background: rgba(93, 130, 255, 0.15);
  color: #7e9eff;
  border-left: 2px solid #5d82ff;
  padding-left: 14px;
}

.sb-divider {
  height: 0.5px;
  background: rgba(255, 255, 255, 0.07);
  border: none;
  margin: 8px 0;
}

.sb-footer {
  padding: 12px 16px;
  border-top: 0.5px solid rgba(255, 255, 255, 0.08);
}

.sb-avatar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}

.sb-avatar-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #2e3b6e;
  color: #7e9eff;
  font-size: 11px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sb-avatar-name {
  font-size: 13px;
  color: #c8cdd8;
  font-weight: 500;
}

.sb-avatar-role {
  font-size: 11px;
  color: #4e5568;
}

.sb-logout {
  margin-top: 8px;
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 10px;
  border-radius: 6px;
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  background: none;
  color: #9aa0af;
  font-size: 12px;
  cursor: pointer;
  text-decoration: none;

}

.sb-logout:hover {
  background: lightblue;
  color: black;
  text-decoration: none;
}

.main-content {
  flex: 1;
  overflow-x: hidden;
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

.sb-body::-webkit-scrollbar {
  width: 5px;
}
.sb-body::-webkit-scrollbar-track {
  background: transparent;
}
.sb-body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}
.sb-body::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>
