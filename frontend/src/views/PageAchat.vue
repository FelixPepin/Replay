<template>
  <main class="store-page">

    <div class="store-header">
      <div class="store-header-inner">
        <div>
          <h1 class="store-title">Jeux en vente</h1>
          <p class="store-subtitle">{{ jeuxFiltrees.length }} jeu{{ jeuxFiltrees.length !== 1 ? 'x' : '' }} disponible{{
            jeuxFiltrees.length !== 1 ? 's' : '' }}</p>
        </div>
        <div class="store-search-wrap">
          <svg class="search-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input v-model="recherche" type="search" placeholder="Rechercher un jeu..." class="store-search" />
        </div>
      </div>
    </div>

    <div v-if="notif.message" :class="`notif-bar notif-${notif.type}`">{{ notif.message }}</div>

    <div class="store-body">

      <aside class="sidebar-filters">
        <div class="filter-header">
          <span>Filtres</span>
          <button class="reset-btn" @click="reinitialiserFiltres">Réinitialiser</button>
        </div>

        <div class="filter-group">
          <label class="filter-label">Trier par</label>
          <select v-model="tri" class="filter-select">
            <option value="alpha">A → Z</option>
            <option value="prix_asc">Prix croissant</option>
            <option value="prix_desc">Prix décroissant</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label">Console</label>
          <select v-model="filtreConsole" class="filter-select">
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

        <div class="filter-group">
          <label class="filter-label">Livraison</label>
          <select v-model="filtreLivraison" class="filter-select">
            <option value="">Toutes</option>
            <option value="Par la poste">Par la poste</option>
            <option value="En main propre">En main propre</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label">Paiement</label>
          <select v-model="filtrePaiement" class="filter-select">
            <option value="">Tous</option>
            <option value="En ligne">En ligne</option>
            <option value="En main propre">En main propre</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label">Fourchette de prix</label>
          <div class="prix-range">
            <input v-model.number="filtrePrixMin" type="number" min="0" class="filter-input" placeholder="Min $"
              @input="limiterDecimales($event, 'filtrePrixMin')" />
            <span class="prix-sep">—</span>
            <input v-model.number="filtrePrixMax" type="number" min="0" class="filter-input" placeholder="Max $"
              @input="limiterDecimales($event, 'filtrePrixMax')" />
          </div>
        </div>
      </aside>

      <section class="games-grid-wrap">

        <div v-if="chargement" class="état-vide">
          <div class="spinner"></div>
          <p>Chargement...</p>
        </div>

        <div v-else-if="jeuxFiltrees.length === 0" class="état-vide">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <p>Aucun jeu trouvé.</p>
          <button class="reset-btn-lg" @click="reinitialiserFiltres">Réinitialiser les filtres</button>
        </div>

        <div v-else class="games-grid">
          <JeuCard v-for="jeu in jeuxFiltrees" :key="jeu.Id" :jeu="jeu" mode="achat" />
        </div>

      </section>
    </div>

  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
import JeuCard from '@/components/JeuCard.vue'

const jeux = ref([])
const chargement = ref(true)
const tri = ref('alpha')
const auth = useAuthStore()
const notif = useNotifStore()
const recherche = ref('')
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
  tri.value = 'alpha'
  filtreConsole.value = ''
  filtreLivraison.value = ''
  filtrePaiement.value = ''
  filtrePrixMin.value = null
  filtrePrixMax.value = null
  recherche.value = ''
}

const jeuxFiltrees = computed(() => {
  let liste = jeux.value.filter(jeu => !jeu.estVendu && jeu.VendeurId !== auth.userId)
  if (liste.length === 0) return []


  if (recherche.value.trim())
    liste = liste.filter(jeu => jeu.NomJeu.toLowerCase().includes(recherche.value.toLowerCase()))
  if (filtreConsole.value)
    liste = liste.filter(jeu => jeu.TypeConsole === filtreConsole.value)
  if (filtreLivraison.value)
    liste = liste.filter(jeu => jeu.TypeLivraison === filtreLivraison.value)
  if (filtrePaiement.value)
    liste = liste.filter(jeu => jeu.TypePaiement === filtrePaiement.value)
  if (filtrePrixMin.value !== null && filtrePrixMin.value !== '')
    liste = liste.filter(jeu => jeu.Prix >= filtrePrixMin.value)
  if (filtrePrixMax.value !== null && filtrePrixMax.value !== '')
    liste = liste.filter(jeu => jeu.Prix <= filtrePrixMax.value)

  if (tri.value === 'alpha') return liste.sort((a, b) => a.NomJeu.localeCompare(b.NomJeu))
  if (tri.value === 'prix_asc') return liste.sort((a, b) => a.Prix - b.Prix)
  if (tri.value === 'prix_desc') return liste.sort((a, b) => b.Prix - a.Prix)
  return liste
})

onMounted(async () => {
  try {
    const response = await axios.get('/api/ventes')
    jeux.value = Array.isArray(response.data) ? response.data : []
  } catch (err) {
    console.error('Erreur:', err)
  } finally {
    chargement.value = false
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.store-page {
  font-family: 'DM Sans', sans-serif;
  background: transparent;
  min-height: 100vh;
  color: #1a1d23;
}

.store-header {
  background: transparent;
  padding: 28px 0;
  width: 100%;
}

.store-header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.store-title {
  font-family: 'Syne', sans-serif;
  font-size: 28px;
  font-weight: 800;
  color: #1a1d23;
  letter-spacing: -0.5px;
}

.store-subtitle {
  font-size: 13px;
  color: #4b5263;
  margin-top: 2px;
}

.store-search-wrap {
  position: relative;
  flex: 1;
  max-width: 360px;
}

.search-ico {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #6b7280;
}

.store-search {
  width: 100%;
  background: rgba(255, 255, 255, 0.7);
  border: 1.5px solid rgba(255, 255, 255, 0.5);
  border-radius: 50px;
  padding: 10px 16px 10px 40px;
  font-family: inherit;
  font-size: 14px;
  color: #1a1d23;
  outline: none;
  backdrop-filter: blur(8px);
  transition: border-color 0.2s;
}

.store-search::placeholder {
  color: #6b7280;
}

.store-search:focus {
  border-color: #1a1d23;
}

.notif-bar {
  padding: 12px 32px;
  font-size: 14px;
  font-weight: 500;
}

.notif-success {
  background: #dcfce7;
  color: #16a34a;
}

.notif-error {
  background: #fee2e2;
  color: #ef4444;
}

.notif-info {
  background: #dbeafe;
  color: #1d4ed8;
}

.store-body {
  max-width: 1400px;
  margin: 0 auto;
  padding: 28px 32px;
  display: flex;
  gap: 28px;
  align-items: flex-start;
}

.sidebar-filters {
  width: 240px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1.5px solid rgba(255, 255, 255, 0.6);
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 20px;
}

.filter-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1d23;
}

.reset-btn {
  font-size: 12px;
  color: #6366f1;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
  font-weight: 500;
}

.reset-btn:hover {
  text-decoration: underline;
}

.filter-group {
  margin-bottom: 16px;
}

.filter-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
}

.filter-select,
.filter-input {
  width: 100%;
  border: 1.5px solid #e2e6ed;
  border-radius: 10px;
  padding: 8px 12px;
  font-family: inherit;
  font-size: 13.5px;
  color: #1a1d23;
  background: #fff;
  outline: none;
  transition: border-color 0.2s;
}

.filter-select:focus,
.filter-input:focus {
  border-color: #6366f1;
}

.prix-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.prix-range .filter-input {
  flex: 1;
}

.prix-sep {
  color: #9ba3b0;
  font-size: 13px;
}

.games-grid-wrap {
  flex: 1;
  min-width: 0;
}

.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.état-vide {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 16px;
  color: #9ba3b0;
}

.état-vide svg {
  width: 48px;
  height: 48px;
}

.état-vide p {
  font-size: 15px;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e8eaf0;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.reset-btn-lg {
  background: #1a1d23;
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 9px 20px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.reset-btn-lg:hover {
  background: #6366f1;
}

@media (max-width: 768px) {
  .store-body {
    flex-direction: column;
    padding: 16px;
  }

  .sidebar-filters {
    width: 100%;
    position: static;
  }

  .store-header-inner {
    flex-direction: column;
    align-items: flex-start;
  }

  .store-search-wrap {
    max-width: 100%;
    width: 100%;
  }
}
</style>