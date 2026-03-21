<template>
  <main class="container">
    <div class="container mt-5">
      <h1>Liste de jeux en vente</h1>
    </div>
    <div v-if="notif.message" :class="`alert alert-${notif.type}`">
      {{ notif.message }}
    </div>

    <div class="row">
      <div v-for="jeu in jeux" :key="jeu.Id" class="col-lg-6 mb-3">
        <div class="card h-100">
          <img class="card-img-top w-100" :src="`/static/images/ajouts/${jeu.Photo}`" />
          <div class="card-body">
            <h2 class="card-title">Nom du jeu : {{ jeu.NomJeu }}</h2>
            <p class="card-text">Prix : {{ jeu.Prix }}$</p>
            <p class="card-text">Vendeur : {{ jeu.NomUtilisateur }}</p>
            <p class="card-text">Livraison : {{ jeu.TypeLivraison }}</p>
            <p class="card-text">Paiement : {{ jeu.TypePaiement }}</p>
            <RouterLink v-if="!jeu.estVendu" :to="`/acheter/${jeu.Id}`" class="btn btn-success rounded-2">
              Acheter
            </RouterLink>
            <button v-else class="btn btn-danger rounded-2" disabled>
              Vendu
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue';
import axios from 'axios'
import { useAuthStore } from '@/stores/auth';
import { useNotifStore } from '@/stores/notif';
const jeux = ref([])
const auth = useAuthStore()
const notif = useNotifStore()


onMounted(async () => {
  try {
    const response = await axios.get('/api/ventes')
    console.log(response.data[0])
    jeux.value = Array.isArray(response.data) ? response.data : []
  } catch (err) {
    console.error('Erreur:', err)
  }
})
</script>
