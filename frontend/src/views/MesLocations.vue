<template>
  <main>
    <div class="container">
      <h1 class="mb-4 mt-2">Mes Locations</h1>
      <div v-if="notif.message" :class="`alert alert-${notif.type}`">
        {{ notif.message }}
      </div>
      <div v-if="erreurs" class="alert alert-danger">
        {{ erreurs }}
      </div>
      <p v-if="locations.length === 0 && !erreurs" class="alert alert-info">Vous n'avez aucune location.</p>
      <div class="row">
        <div v-for="location in locations" :key="location.id" class="col-md-6">
          <div class="card mb-4 shadow-sm">
            <img class="card-img-top w-100" :src="`/static/images/ajouts/${location.Photo}`" />
            <div class="card-body">
              <h2 class="card-title">Nom du jeu : {{ location.NomJeu }}</h2>
              <p class="card-text">Prix : {{ location.Prix }}$</p>
              <p class="card-text">Vendeur : {{ location.NomUtilisateur }}</p>
              <p class="card-text">Adresse : {{location.Adresse}}</p>
              <p class="card-text">Début : {{ formatDate(location.DateDebut) }}</p>
              <p class="card-text">Fin : {{ formatDate(location.DateFin) }}</p>
              
              <RouterLink :to="`/modifierLocation/${location.Id}`" class="btn btn-warning p-2 text-black ms-5"
                >Modifier</RouterLink
              >
              <RouterLink :to="`/supprimerLocation/${location.Id}`" class="btn btn-danger p-2 text-black ms-5"
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
import { useNotifStore } from '@/stores/notif'
import { ref, onMounted, onUnmounted } from 'vue'
const locations = ref([])
const erreurs = ref('')

function formatDate(date) {
  const d = new Date(date)
  if (isNaN(d)) return date
  const str = new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate())
      .toLocaleDateString('fr-CA', { day: 'numeric', month: 'long', year: 'numeric' })
  return str.charAt(0).toUpperCase() + str.slice(1)
}
const auth = useAuthStore()
const notif = useNotifStore()

onUnmounted(() => notif.clear())

onMounted(async () => {
  try {
    const res = await fetch(`/api/mesLocations/${auth.userId}`)
    const data = await res.json()
    if (res.ok) {
      locations.value = data
    } else {
      erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    }
  } catch (e) {
    erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    return
  }
})
</script>
