<script setup>
import { ref, computed, onMounted } from 'vue';
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
const router = useRouter()
const message = ref("")
const estConnecte = computed(() => !!localStorage.getItem('token'))
onMounted(() => {
  message.value = history.state.success || ""
})

function deconnecter() {
  auth.deconnecter()
  router.push('/login')
}
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 shadow-sm">
      <div class="container-fluid container">
        <a class="navbar-brand fw-bold fs-3 text-warning" href="/">RePlay</a>

        <div class="d-flex align-items-center">
          <RouterLink to="/achat" class="nav-link text-white me-3">Acheter</RouterLink>
          <RouterLink to="/vendre" class="nav-link text-white me-3">Vendre</RouterLink>
          <RouterLink v-if="auth.estConnecte" to="/mesVentes" class="nav-link text-white me-3">
            Mes Ventes
          </RouterLink>
          <div class="ms-2 d-flex gap-2">
            <RouterLink v-if="!auth.estConnecte" to="/register" class="btn btn-outline-warning btn-sm">
              Inscription
            </RouterLink>
            <RouterLink v-if="!auth.estConnecte" to="/login" class="btn btn-outline-warning btn-sm">
              Connexion
            </RouterLink>
            <button v-if="auth.estConnecte" @click="deconnecter" class="btn btn-info btn-sm">
              Se déconnecter
            </button>
          </div>
        </div>
      </div>
    </nav>
    <div v-if="message" class="text-w">
      {{ message }}
    </div>
  </header>

  <RouterView />
  <footer class="footer mt-auto py-5 text-white">
    <div class="container">
      <div class="row g-4">
        <div class="col-lg-4 col-md-6">
          <h4 class="fw-bold text-warning mb-3">RePlay</h4>
          <p class="opacity-75">
            « Rejoue mieux en donnant une seconde vie aux jeux. »
          </p>
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
              <RouterLink to="/location" class="text-white text-decoration-none hover-warning">Louer</RouterLink>
            </li>
          </ul>
        </div>

        <div class="col-lg-2 col-md-6">
          <h5 class="fw-bold mb-3">Support</h5>
          <ul class="list-unstyled opacity-75">
            <li class="mb-2"><a href="#" class="text-white text-decoration-none">FAQ</a></li>
            <li class="mb-2"><a href="#" class="text-white text-decoration-none">Système d'évaluations</a></li>
            <li class="mb-2"><a href="#" class="text-white text-decoration-none">Protection Acheteur</a></li>
          </ul>
        </div>

        <div class="col-lg-4 col-md-6">
          <h5 class="fw-bold mb-3">Restez au courant</h5>
          <p class="small opacity-75">Recevez les meilleures offres de jeux usagés avant tout le monde.</p>
          <div class="input-group mb-3 shadow-sm">
            <input type="text" class="form-control border-0" placeholder="Ton courriel" aria-label="Email">
            <button class="btn btn-warning fw-bold" type="button">OK</button>
          </div>
        </div>
      </div>

      <hr class="my-5 opacity-25">

      <div class="d-flex flex-column flex-sm-row justify-content-between align-items-center opacity-50 small">
        <p>&copy; 2024 RePlay Inc. Tous droits réservés.</p>
        <ul class="list-inline mb-0">
          <li class="list-inline-item me-4">Confidentialité</li>
          <li class="list-inline-item">Conditions d'utilisation</li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<style>
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.nav-link:hover {
  color: #ffca28 !important;
}
</style>
