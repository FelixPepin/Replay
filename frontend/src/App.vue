<script setup>
import { ref, computed } from 'vue';
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
const router = useRouter()
const estConnecte = computed(() => !!localStorage.getItem('token'))


function deconnecter() {
  auth.deconnecter()
  router.push('/login')
}
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg">
      <a class="navbar-brand" href="/">Replay</a>
      <RouterLink to="/achat" class="btn btn-primary p-2 text-black m-2">Achat</RouterLink>
      <RouterLink to="/vendre" class="btn btn-primary p-2 text-black m-2">Vendre un jeu</RouterLink>
      <RouterLink to="/mesVentes" class="btn btn-primary p-2 text-black m-2">Mes ventes</RouterLink>
      <RouterLink to="/register" class="btn btn-primary p-2 text-black m-2">Inscription</RouterLink>
      <button v-show="auth.estConnecte" id="deconnexion" @click="deconnecter" class="btn btn-info p-2 text-black m-2">Se
        déconnecter</button>
    </nav>
  </header>

  <body>
    <div id="carouselExample" class="carousel slide">
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="..." class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item">
          <img src="..." class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item">
          <img src="..." class="d-block w-100" alt="...">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </body>

  <RouterView />
</template>
