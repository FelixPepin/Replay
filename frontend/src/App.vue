<script setup>
import { ref , computed} from 'vue';
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
      <nav class="navbar navbar-expand">
        <RouterLink to="/vendre" class="btn btn-primary p-2 text-black m-2">Vendre un jeu</RouterLink>
        <RouterLink to="/register" class="btn btn-primary p-2 text-black m-2">Inscription</RouterLink>
        <button v-show="auth.estConnecte" id="deconnexion" @click="deconnecter" class="btn btn-info p-2 text-black m-2">Se déconnecter</button>
      </nav>
  </header>

  <RouterView />
</template>


