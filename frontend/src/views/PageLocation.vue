<template>
    <main class="container">
        <div class="container mt-5">
            <h1>Liste de jeux disponible en location</h1>
                <div v-if="notif.message" :class="`alert alert-${notif.type}`">
                    {{ notif.message }}
                </div>
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
                <input v-model="recherche" class="form-control me-2" type="search" placeholder="Nom du jeu"
                    aria-label="Search">
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
                        <label class="form-label">Début disponibilité</label>
                        <input v-model="filtreDateDebut" type="date" class="form-control">
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Fin disponibilité</label>
                        <input v-model="filtreDateFin" type="date" class="form-control">
                    </div>
                    <div class="col-md-2">
                        <label class="form-label">Prix min ($)</label>
                        <input v-model.number="filtrePrixMin" type="number" min="0" class="form-control" placeholder="0" @input="limiterDecimales($event, 'filtrePrixMin')">
                    </div>
                    <div class="col-md-2">
                        <label class="form-label">Prix max ($)</label>
                        <input v-model.number="filtrePrixMax" type="number" min="0" class="form-control" placeholder="∞" @input="limiterDecimales($event, 'filtrePrixMax')">
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
                        <h2 class="card-title h5">{{ jeu.NomJeu }}</h2>
                        <p class="card-text text-primary fw-bold">
                            <span class="text-black">Prix : </span> {{ jeu.Prix }} $
                        </p>
                        <p class="card-text text-primary fw-bold">
                            <span class="text-black">Console : </span> {{ jeu.TypeConsole }}
                        </p>
                        <p class="card-text text-primary fw-bold">
                            <span class="text-black">Date début : </span> {{ formatDate(jeu.DateDebut) }}
                        </p>
                        <p class="card-text text-primary fw-bold">
                            <span class="text-black">Date fin : </span> {{ formatDate(jeu.DateFin) }}
                        </p>
                        <RouterLink :to="`/louer/${jeu.Id}`" class="btn btn-success rounded-2">
                            Louer
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue';
import { useNotifStore } from '@/stores/notif'
import { useAuthStore } from '@/stores/auth'

function formatDate(date) {
    const d = new Date(date)
    if (isNaN(d)) return date
    const str = new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate())
        .toLocaleDateString('fr-CA', { day: 'numeric', month: 'long', year: 'numeric' })
    return str.charAt(0).toUpperCase() + str.slice(1)
}
import axios from 'axios'
const tri = ref('alpha')
const auth = useAuthStore()
const notif = useNotifStore()
const recherche = ref('')
const jeux = ref([])
const filtresOuverts = ref(false)
const filtreConsole = ref('')
const filtreDateDebut = ref('')
const filtreDateFin = ref('')
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
    filtreDateDebut.value = ''
    filtreDateFin.value = ''
    filtrePrixMin.value = null
    filtrePrixMax.value = null
}

const jeuxTriees = computed(() => {
    let liste = [...jeux.value]
    if (liste.length === 0) return []

    liste = liste.filter(jeu => jeu.estDisponible !== 0 && jeu.LocateurId !== auth.userId)

    if (recherche.value.trim() !== '')
        liste = liste.filter(jeu => jeu.NomJeu.toLowerCase().includes(recherche.value.toLowerCase()))

    if (filtreConsole.value !== '')
        liste = liste.filter(jeu => jeu.TypeConsole === filtreConsole.value)

    if (filtreDateDebut.value !== '' || filtreDateFin.value !== '') {
        const toLocalDate = d => { const dt = new Date(d); return new Date(dt.getFullYear(), dt.getMonth(), dt.getDate()) }
        const debut = filtreDateDebut.value ? toLocalDate(filtreDateDebut.value) : new Date('0000-01-01')
        const fin = filtreDateFin.value ? toLocalDate(filtreDateFin.value) : new Date('9999-12-31')
        liste = liste.filter(jeu => {
            const jeuDebut = toLocalDate(jeu.DateDebut)
            const jeuFin = toLocalDate(jeu.DateFin)
            return jeuDebut <= fin && jeuFin >= debut
        })
    }

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
    setTimeout(() => notif.clear(), 4000)
    try {
        const response = await axios.get('/api/locations')
        console.log('type:', typeof response.data)
        console.log('données:', response.data)

        jeux.value = Array.isArray(response.data) ? response.data : []
    } catch (err) {
        console.error('Erreur:', err)
    }
})

</script>
