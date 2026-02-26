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
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 shadow-sm">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold fs-3 text-warning" href="/">RePlay</a>

        <div class="d-flex align-items-center">
          <RouterLink to="/achat" class="nav-link text-white me-3">Acheter</RouterLink>
          <RouterLink to="/vendre" class="nav-link text-white me-3">Vendre</RouterLink>

          <div class="ms-2 d-flex gap-2">
            <RouterLink v-if="!auth.estConnecte" to="/register" class="btn btn-outline-warning btn-sm">
              Inscription
            </RouterLink>
            <button v-if="auth.estConnecte" @click="deconnecter" class="btn btn-info btn-sm">
              Se déconnecter
            </button>
          </div>
        </div>
      </div>
    </nav>
  </header>
  <RouterView />
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
