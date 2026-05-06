<template>
  <main class="store-page">

    <div class="store-header">
      <div class="store-header-inner">
        <div>
          <h1 class="store-title">Mes ventes</h1>
          <p class="store-subtitle">{{ ventes.length }} jeu{{ ventes.length !== 1 ? 'x' : '' }} en vente</p>
        </div>
        <RouterLink to="/vendre" class="btn-ajouter">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          Mettre en vente
        </RouterLink>
      </div>
    </div>

    <div v-if="notif.message" :class="`notif-bar notif-${notif.type}`">{{ notif.message }}</div>

    <div class="store-body">

      <div v-if="ventes.length === 0 && !erreurs" class="état-vide">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" />
          <line x1="3" y1="6" x2="21" y2="6" />
          <path d="M16 10a4 4 0 0 1-8 0" />
        </svg>
        <p>Vous n'avez aucune vente.</p>
        <RouterLink to="/vendre" class="btn-ajouter">Mettre un jeu en vente</RouterLink>
      </div>

      <div v-if="erreurs" class="notif-bar notif-error">{{ erreurs }}</div>

      <div v-if="ventes.length > 0" class="games-grid">
        <JeuCard v-for="vente in ventes" :key="vente.Id" :jeu="vente" mode="gestion" />
      </div>

    </div>

  </main>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import JeuCard from '@/components/JeuCard.vue'

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

.btn-ajouter {
  display: flex;
  align-items: center;
  gap: 7px;
  background: #1a1d23;
  color: #fff;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 50px;
  transition: background 0.2s;
  font-family: inherit;
  border: none;
  cursor: pointer;
}

.btn-ajouter svg {
  width: 14px;
  height: 14px;
}

.btn-ajouter:hover {
  background: #6366f1;
  color: #fff;
}

.notif-bar {
  padding: 12px 32px;
  font-size: 14px;
  font-weight: 500;
  max-width: 1400px;
  margin: 0 auto;
}

.notif-success {
  background: #dcfce7;
  color: #16a34a;
  border-radius: 10px;
}

.notif-error {
  background: #fee2e2;
  color: #ef4444;
  border-radius: 10px;
}

.notif-info {
  background: #dbeafe;
  color: #1d4ed8;
  border-radius: 10px;
}

.store-body {
  max-width: 1400px;
  margin: 0 auto;
  padding: 8px 32px 40px;
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

@media (max-width: 768px) {
  .store-body {
    padding: 16px;
  }

  .store-header-inner {
    padding: 0 16px;
  }
}
</style>