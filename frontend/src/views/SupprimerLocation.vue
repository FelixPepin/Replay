<template>
  <main>
    <div class="container mt-2">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <h1 class="mb-4 text-center">Supprimer une location</h1>
          <div v-if="auth.userId === locateurId">
            <div class="card mb-4 shadow-sm">
              <img class="card-img-top w-100" :src="`/static/images/ajouts/${photo}`" />
              <div class="card-body">
                <h2 class="card-title">Nom du jeu : {{ nomJeu }}</h2>
                <p class="card-text">Prix : {{ prix }}$</p>
                <p class="card-text">Paiement : {{ choixPaiement }}</p>
                <p class="card-text">Adresse : {{ adresse }}</p>
                <p class="card-text">Console : {{typeConsole}}</p>
                <p class="card-text">Date début : {{ formatDate(dateDebut) }}</p>
                <p class="card-text">Date fin : {{ formatDate(dateFin) }}</p>
              </div>
            </div>
            <form
              @submit.prevent="supprimerLocation"
              method="post"
              enctype="multipart/form-data"
              novalidate
            >
              <button type="submit" class="btn btn-danger w-100">Supprimer la location</button>
            </form>
          </div>
          <div v-else>
            <p class="alert alert-warning">Vous devez être le locateur pour supprimer cette location.</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
const auth = useAuthStore()
const notif = useNotifStore()
const router = useRouter()
const route = useRoute()

const idVente = route.params.id

const nomJeu = ref('')
const prix = ref('')
const choixPaiement = ref('')
const choixLivraison = ref('')
const adresse = ref('')
const locateurId = ref('')
const photo = ref('')
const dateDebut = ref('')
const dateFin = ref('')
const typeConsole = ref('')
const estLoue = ref('')

function formatDate(date) {
  const str = new Date(date).toLocaleDateString('fr-CA', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
  return str.charAt(0).toUpperCase() + str.slice(1)
}

onMounted(async () => {
  try {
    const res = await fetch(`/api/location/${idVente}`)
    const data = await res.json()
    if (res.ok) {
      prix.value = data.Prix
      choixLivraison.value = data.TypeLivraison
      choixPaiement.value = data.TypePaiement
      adresse.value = data.Adresse ?? ''
      nomJeu.value = data.NomJeu
      locateurId.value = data.LocateurId
      photo.value = data.Photo
      dateDebut.value = data.DateDebut
      dateFin.value = data.DateFin
      typeConsole.value = data.TypeConsole
      estLoue.value = data.EstLoue
    } else {
      erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    }
  } catch (e) {
    erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    return
  }
})

// TODO: Empêcher la suppression si la location est actuellement en cours (dateDebut <= aujourd'hui <= dateFin)

async function supprimerLocation() {
  try {
    const reponse = await fetch(`/api/supprimerLocation/${idVente}`, {
      method: 'POST',
    })

    const data = await reponse.json()

    if (reponse.ok) {
      notif.setNotif('Location supprimée avec succès')
      router.push('/mesLocations')
    } else {
      Object.assign(erreurs, data.erreurs)
    }
  } catch (e) {
    erreurs.serveur = 'Impossible de contacter le serveur'
  }
}
</script>
