<template>
  <main>
    <div class="container">
      <h1 class="mb-4">Mes Ventes</h1>
      <div v-if="erreurs" class="alert alert-danger">
        {{ erreurs }}
      </div>
      <div class="row">
        <div v-for="vente in ventes" :key="vente.id" class="col-md-6">
          <div class="card mb-4 shadow-sm">
            <img
              class="card-img-top w-100"
              :src="`http://localhost:5000/static/images/ajouts/${vente.Photo}`"
            />
            <div class="card-body">
              <h2 class="card-title">Nom du jeu : {{ vente.NomJeu }}</h2>
              <p class="card-text">Prix : {{ vente.Prix }}$</p>
              <p class="card-text">Vendeur : {{ vente.NomUtilisateur }}</p>
              <p class="card-text">Livraison : {{ vente.TypeLivraison }}</p>
              <p class="card-text">Paiement : {{ vente.TypePaiement }}</p>
              <RouterLink :to="`/modifier/${vente.Id}`" class="btn btn-primary p-2 text-black ms-5"
                >Modifier</RouterLink
              >
              <RouterLink :to="`/supprimer/${vente.Id}`" class="btn btn-primary p-2 text-black ms-5"
                >Supprimer</RouterLink
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref, onMounted } from 'vue'
const ventes = ref([])
const erreurs = ref('')
const auth = useAuthStore()

onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:5000/mesVentes/${auth.userId}`)
    const data = await res.json()
    if (res.ok) {
      ventes.value = data
    } else {
      erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    }
  } catch (e) {
    erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    return
  }
})
</script>
