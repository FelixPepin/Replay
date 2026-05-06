<template>
  <main>
    <div class="container">
      <h1 class="mb-4 mt-2">Mes Ventes</h1>
      <div v-if="notif.message" :class="`alert alert-${notif.type}`">
        {{ notif.message }}
      </div>
      <div v-if="erreurs" class="alert alert-danger">
        {{ erreurs }}
      </div>
      <p v-if="ventes.length === 0 && !erreurs" class="alert alert-info">Vous n'avez aucune vente.</p>
      <div class="row">
        <div v-for="vente in ventes" :key="vente.id" class="col-md-6">
          <div class="card mb-4 shadow-sm">
            <img class="card-img-top w-100" :src="`/static/images/ajouts/${vente.Photo}`" />
            <div class="card-body">
              <h2 class="card-title">Nom du jeu : {{ vente.NomJeu }}</h2>
              <p class="card-text">Prix : {{ vente.Prix }}$</p>
              <p class="card-text">Vendeur : {{ vente.NomUtilisateur }}</p>
              <p class="card-text">Livraison : {{ vente.TypeLivraison }}</p>
              <p class="card-text">Paiement : {{ vente.TypePaiement }}</p>
              <RouterLink :to="`/modifierVente/${vente.Id}`" class="btn btn-warning p-2 text-black ms-5"
                >Modifier</RouterLink
              >
              <RouterLink :to="`/supprimerVente/${vente.Id}`" class="btn btn-danger p-2 text-black ms-5"
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
import { useRouter } from 'vue-router'
const ventes = ref([])
const erreurs = ref('')
const auth = useAuthStore()
const notif = useNotifStore()
const router = useRouter()

onUnmounted(() => notif.clear())

onMounted(async () => {
  try {
    const res = await fetch(`/api/mesVentes/${auth.userId}`)
    const data = await res.json()
    if (res.ok) {
      ventes.value = data
    } else if (res.status >= 500) {
      router.push('/erreur/500')
    } else {
      erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    }
  } catch (e) {
    router.push('/erreur/500')
  }
})
</script>
