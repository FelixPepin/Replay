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
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Mettre en vente
        </RouterLink>
      </div>
    </div>

    <div v-if="notif.message" :class="`notif-bar notif-${notif.type}`">{{ notif.message }}</div>

    <div class="store-body">

      <div v-if="ventes.length === 0 && !erreurs" class="état-vide">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
          <line x1="3" y1="6" x2="21" y2="6"/>
          <path d="M16 10a4 4 0 0 1-8 0"/>
        </svg>
        <p>Vous n'avez aucune vente.</p>
        <RouterLink to="/vendre" class="btn-ajouter">Mettre un jeu en vente</RouterLink>
      </div>

      <div v-if="erreurs" class="notif-bar notif-error">{{ erreurs }}</div>

      <div v-if="ventes.length > 0" class="games-grid">
        <div v-for="vente in ventes" :key="vente.Id" class="game-card" :class="{ 'game-card--vendu': vente.estVendu }">

          <div class="game-img-wrap">
            <img :src="`/static/images/ajouts/${vente.Photo}`" :alt="vente.NomJeu" class="game-img" />
            <span class="game-console-badge">{{ vente.TypeConsole }}</span>
            <span v-if="vente.estVendu" class="vendu-overlay">Vendu</span>
          </div>

          <div class="game-body">
            <h3 class="game-title">{{ vente.NomJeu }}</h3>
            <div class="game-meta">
              <span class="meta-tag">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
                {{ vente.TypeLivraison }}
              </span>
              <span class="meta-tag">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="1" y="4" width="22" height="16" rx="2"/>
                  <line x1="1" y1="10" x2="23" y2="10"/>
                </svg>
                {{ vente.TypePaiement }}
              </span>
            </div>
          </div>

          <div class="game-footer">
            <span class="game-price">{{ vente.Prix }} $</span>
            <div class="game-actions">
              <RouterLink :to="`/modifierVente/${vente.Id}`" class="btn-modifier">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </RouterLink>
              <RouterLink :to="`/supprimerVente/${vente.Id}`" class="btn-supprimer">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6l-1 14H6L5 6"/>
                  <path d="M10 11v6"/><path d="M14 11v6"/>
                  <path d="M9 6V4h6v2"/>
                </svg>
              </RouterLink>
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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.store-page {
  font-family: 'DM Sans', sans-serif;
  background: transparent;
  min-height: 100vh;
  color: #1a1d23;
}

/* ── Header ── */
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
.btn-ajouter svg { width: 14px; height: 14px; }
.btn-ajouter:hover { background: #6366f1; color: #fff; }

/* ── Notif ── */
.notif-bar {
  padding: 12px 32px;
  font-size: 14px;
  font-weight: 500;
  max-width: 1400px;
  margin: 0 auto;
}
.notif-success { background: #dcfce7; color: #16a34a; border-radius: 10px; }
.notif-error   { background: #fee2e2; color: #ef4444; border-radius: 10px; }
.notif-info    { background: #dbeafe; color: #1d4ed8; border-radius: 10px; }

/* ── Body ── */
.store-body {
  max-width: 1400px;
  margin: 0 auto;
  padding: 8px 32px 40px;
}

/* ── Grid ── */
.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

/* ── Card ── */
.game-card {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(8px);
  border-radius: 16px;
  border: 1.5px solid rgba(255,255,255,0.6);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}
.game-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(99,102,241,0.15);
  border-color: #6366f1;
}
.game-card--vendu { opacity: 0.6; }

.game-img-wrap {
  position: relative;
  height: 180px;
  background: #f0f2f6;
  overflow: hidden;
}
.game-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.game-card:hover .game-img { transform: scale(1.04); }

.game-console-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(26,29,35,0.85);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 50px;
  backdrop-filter: blur(4px);
}

.vendu-overlay {
  position: absolute;
  inset: 0;
  background: rgba(26,29,35,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Syne', sans-serif;
  font-size: 20px;
  font-weight: 800;
  color: #fff;
  letter-spacing: 2px;
  backdrop-filter: blur(2px);
}

.game-body {
  padding: 14px 16px 10px;
  flex: 1;
}

.game-title {
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1d23;
  margin-bottom: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.game-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.meta-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #f4f5f7;
  border: 1px solid #e8eaf0;
  border-radius: 50px;
  padding: 3px 10px;
  font-size: 11.5px;
  color: #4b5263;
  font-weight: 500;
}
.meta-tag svg { width: 11px; height: 11px; }

.game-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-top: 1px solid #f0f2f6;
}

.game-price {
  font-family: 'Syne', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #1a1d23;
}

.game-actions { display: flex; gap: 8px; }

.btn-modifier, .btn-supprimer {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  border: 1.5px solid transparent;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
  text-decoration: none;
}
.btn-modifier svg, .btn-supprimer svg { width: 15px; height: 15px; }

.btn-modifier       { color: #6366f1; }
.btn-modifier:hover { background: #ede9fe; border-color: #c4b5fd; }

.btn-supprimer       { color: #ef4444; }
.btn-supprimer:hover { background: #fee2e2; border-color: #fca5a5; }

/* ── État vide ── */
.état-vide {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 16px;
  color: #9ba3b0;
}
.état-vide svg { width: 48px; height: 48px; }
.état-vide p { font-size: 15px; }

/* ── Responsive ── */
@media (max-width: 768px) {
  .store-body { padding: 16px; }
  .store-header-inner { padding: 0 16px; }
}
</style>