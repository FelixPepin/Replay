<template>
  <main class="container">
    <div class="container mt-5">
      <h1>Liste de jeux en vente</h1>
    </div>
    <div v-if="notif.message" :class="`alert alert-${notif.type}`">
      {{ notif.message }}
    </div>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="col-md-3">
        <select v-model="tri" class="form-select">
          <option value="alpha">Ordre alphabétique</option>
          <option value="prix_asc">Prix croissant</option>
          <option value="prix_desc">Prix décroissant</option>
        </select>
      </div>
      <div class="col-md-4">
        <input v-model="recherche" class="form-control me-2" type="search" placeholder="Nom du jeu" aria-label="Search">
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-header d-flex justify-content-between align-items-center" style="cursor:pointer"
        @click="filtresOuverts = !filtresOuverts">
        <span class="fw-semibold">Filtres</span>
        <span>{{ filtresOuverts ? '▲' : '▼' }}</span>
      </div>
      <div v-if="filtresOuverts" class="card-body">
        <div class="row g-3">
          <div class="col-md-3">
            <label class="form-label">Console</label>
            <select v-model="filtreConsole" class="form-select">
              <option value="">Toutes</option>
              <option value="PS5">PS5</option>
              <option value="PS4">PS4</option>
              <option value="PS3">PS3</option>
              <option value="Xbox Series X">Xbox Series X</option>
              <option value="Xbox One">Xbox One</option>
              <option value="Xbox 360">Xbox 360</option>
              <option value="Nintendo Switch 2">Nintendo Switch 2</option>
              <option value="Nintendo Switch">Nintendo Switch</option>
              <option value="Wii U">Wii U</option>
              <option value="Wii">Wii</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Livraison</label>
            <select v-model="filtreLivraison" class="form-select">
              <option value="">Tous</option>
              <option value="Par la poste">Par la poste</option>
              <option value="En main propre">En main propre</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Paiement</label>
            <select v-model="filtrePaiement" class="form-select">
              <option value="">Tous</option>
              <option value="En ligne">En ligne</option>
              <option value="En main propre">En main propre</option>
            </select>
          </div>
          <div class="col-md-2">
            <label class="form-label">Prix min ($)</label>
            <input v-model.number="filtrePrixMin" type="number" min="0" class="form-control" placeholder="0"
              @input="limiterDecimales($event, 'filtrePrixMin')">
          </div>
          <div class="col-md-2">
            <label class="form-label">Prix max ($)</label>
            <input v-model.number="filtrePrixMax" type="number" min="0" class="form-control" placeholder="∞"
              @input="limiterDecimales($event, 'filtrePrixMax')">
          </div>
          <div class="col-md-2 d-flex align-items-end">
            <button class="btn btn-outline-secondary w-100" @click="reinitialiserFiltres">Réinitialiser</button>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div v-for="jeu in jeuxTriees" :key="jeu.Id" class="col-lg-6 mb-3">
        <div class="card h-100">
          <img class="card-img-top w-100" :src="`/static/images/ajouts/${jeu.Photo}`" />
          <div class="card-body">
            <h2 class="card-title">Nom du jeu : {{ jeu.NomJeu }}</h2>
            <p class="card-text">Prix : {{ jeu.Prix }}$</p>
            <p class="card-text">Console : {{ jeu.TypeConsole }}</p>
            <p class="card-text">Vendeur : {{ jeu.NomUtilisateur }}</p>
            <p class="card-text">Livraison : {{ jeu.TypeLivraison }}</p>
            <p class="card-text">Paiement : {{ jeu.TypePaiement }}</p>
            <RouterLink :to="`/acheter/${jeu.Id}`" class="btn btn-success rounded-2">
              Acheter
            </RouterLink>
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
const tri = ref('alpha')
const auth = useAuthStore()
const notif = useNotifStore()
const recherche = ref('')
const filtresOuverts = ref(false)
const filtreConsole = ref('')
const filtreLivraison = ref('')
const filtrePaiement = ref('')
const filtrePrixMin = ref(null)
const filtrePrixMax = ref(null)

const limiterDecimales = (event, champ) => {
  const val = event.target.value
  if (val.includes('.') && val.split('.')[1].length > 2) {
    const tronque = parseFloat(val).toFixed(2)
    event.target.value = tronque
    if (champ === 'filtrePrixMin') filtrePrixMin.value = parseFloat(tronque)
    else filtrePrixMax.value = parseFloat(tronque)
  }
}

const reinitialiserFiltres = () => {
  filtreConsole.value = ''
  filtreLivraison.value = ''
  filtrePaiement.value = ''
  filtrePrixMin.value = null
  filtrePrixMax.value = null
}

const jeuxTriees = computed(() => {
  let liste = [...jeux.value]
  if (liste.length === 0) return []

  liste = liste.filter(jeu => !jeu.estVendu && jeu.VendeurId !== auth.userId)

  if (recherche.value.trim() !== '')
    liste = liste.filter(jeu => jeu.NomJeu.toLowerCase().includes(recherche.value.toLowerCase()))

  if (filtreConsole.value !== '')
    liste = liste.filter(jeu => jeu.TypeConsole === filtreConsole.value)

  if (filtreLivraison.value !== '')
    liste = liste.filter(jeu => jeu.TypeLivraison === filtreLivraison.value)

  if (filtrePaiement.value !== '')
    liste = liste.filter(jeu => jeu.TypePaiement === filtrePaiement.value)

  if (filtrePrixMin.value !== null && filtrePrixMin.value !== '')
    liste = liste.filter(jeu => jeu.Prix >= filtrePrixMin.value)

  if (filtrePrixMax.value !== null && filtrePrixMax.value !== '')
    liste = liste.filter(jeu => jeu.Prix <= filtrePrixMax.value)

  if (tri.value === 'alpha')
    return liste.sort((a, b) => a.NomJeu.localeCompare(b.NomJeu))
  else if (tri.value === 'prix_asc')
    return liste.sort((a, b) => a.Prix - b.Prix)
  else if (tri.value === 'prix_desc')
    return liste.sort((a, b) => b.Prix - a.Prix)

  return liste
})

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
