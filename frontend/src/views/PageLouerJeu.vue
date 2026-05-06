<template>
  <main class="container mt-5">
    <div class="card p-4 shadow-sm" style="background-color: #fde8e8; border-radius: 20px">
      <div class="row">
        <div class="col-md-6">
          <h2 class="fw-bolder mb-3 text-black">{{ nomJeu }}</h2>
          <p class="text-uppercase fw-bolder mb-2 text-black">Détails du jeu :</p>
          <p class="mb-1 text-black">Prix : {{ prix }} $</p>
          <p class="mb-1 text-black">Vendeur : {{ vendeurNom }}</p>
          <p class="mb-1 text-black">Paiement : {{ choixPaiement }}</p>
          <p class="mb-1 text-black">Adresse : {{ adresse }}</p>
          <p class="mb-1 text-black">Console : {{ typeConsole }}</p>
        </div>
        <div class="col-md-6 d-flex align-items-center justify-content-center">
          <img
            :src="`/static/images/ajouts/${photo}`"
            :alt="nomJeu"
            class="img-fluid rounded"
            style="max-height: 250px; object-fit: cover"
          />
        </div>
      </div>

      <!-- Calendrier -->
      <div class="mt-4">
        <h5 class="fw-bold text-black mb-3">Sélectionner vos dates de location</h5>

        <div v-if="dateDebutLocation && dateFinLocation">
          <p class="text-black mb-3">
            Disponible du <strong>{{ formatDate(dateDebutLocation) }}</strong> au
            <strong>{{ formatDate(dateFinLocation) }}</strong>
          </p>

          <!-- Navigation mois -->
          <div class="d-flex align-items-center justify-content-between mb-2">
            <button @click="moisPrecedent" :disabled="!peutAllerPrecedent" class="btn btn-outline-secondary btn-sm">&#8249;</button>
            <span class="fw-semibold text-black text-capitalize">{{ nomMoisAffiche }}</span>
            <button @click="moisSuivant" :disabled="!peutAllerSuivant" class="btn btn-outline-secondary btn-sm">&#8250;</button>
          </div>

          <!-- Grille calendrier -->
          <div class="cal-grid">
            <div class="cal-row">
              <div v-for="j in ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']" :key="j" class="cal-cell cal-header">
                {{ j }}
              </div>
            </div>
            <div v-for="(sem, i) in semaines" :key="i" class="cal-row">
              <div
                v-for="(jour, j) in sem"
                :key="j"
                class="cal-cell"
                :class="classeJour(jour)"
                @click="selectionnerJour(jour)"
              >
                {{ jour ? jour.getDate() : '' }}
              </div>
            </div>
          </div>

          <!-- Dates choisies -->
          <div class="mt-3 d-flex align-items-center gap-3 text-black">
            <div>
              <span v-if="dateDebutChoisie">
                Début : <strong>{{ formatDate(toStr(dateDebutChoisie)) }}</strong>
              </span>
              <span v-if="dateFinChoisie">
                &nbsp;— Fin : <strong>{{ formatDate(toStr(dateFinChoisie)) }}</strong>
              </span>
              <span v-if="!dateDebutChoisie" class="fst-italic text-black">
                Cliquez sur une date pour commencer la sélection
              </span>
              <span v-else-if="!dateFinChoisie" class="fst-italic text-black ms-2">
                Cliquez sur une date de fin
              </span>
            </div>
            <button
              v-if="dateDebutChoisie"
              @click="dateDebutChoisie = null; dateFinChoisie = null"
              class="btn btn-outline-secondary btn-sm"
            >
              Effacer
            </button>
          </div>

          <!-- Légende -->
          <div class="d-flex gap-3 mt-2 flex-wrap small">
            <span class="d-flex align-items-center gap-1">
              <span class="legende-carre" style="background:#d1e7dd"></span> Disponible
            </span>
            <span class="d-flex align-items-center gap-1">
              <span class="legende-carre" style="background:#f8d7da"></span> Réservé
            </span>
            <span class="d-flex align-items-center gap-1">
              <span class="legende-carre" style="background:#0d6efd"></span> Sélectionné
            </span>
            <span class="d-flex align-items-center gap-1">
              <span class="legende-carre" style="background:#e9ecef"></span> Hors période
            </span>
          </div>
        </div>

        <p v-else class="text-muted fst-italic">Chargement du calendrier...</p>
      </div>

      <div class="d-flex justify-content-end gap-3 mt-4">
        <button @click="router.back()" class="btn btn-danger rounded-pill px-4">
          <i class="fi fi-br-arrow-left me-1"></i> Retour
        </button>
        <button
          @click="louer"
          :disabled="!dateDebutChoisie || !dateFinChoisie"
          class="btn btn-success rounded-pill px-4"
        >
          <i class="fi fi-br-shopping-cart me-1"></i> Louer
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'

const auth = useAuthStore()
const notif = useNotifStore()
const router = useRouter()
const route = useRoute()

const idLocation = route.params.id

const photo = ref('')
const nomJeu = ref('')
const prix = ref('')
const choixPaiement = ref('')
const adresse = ref('')
const vendeurId = ref('')
const typeConsole = ref('')
const vendeurNom = ref('')
const dateDebutLocation = ref('')
const dateFinLocation = ref('')

// Ensemble des dates réservées (format "YYYY-MM-DD")
const datesReservees = ref(new Set())

// Sélection de l'utilisateur
const dateDebutChoisie = ref(null)
const dateFinChoisie = ref(null)

// Navigation du calendrier
const moisAffiche = ref({ annee: new Date().getFullYear(), mois: new Date().getMonth() })

function parseDate(str) {
  if (!str) return null
  const d = new Date(str)
  if (isNaN(d)) return null
  return new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate())
}

function toStr(date) {
  if (!date) return ''
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

function formatDate(str) {
  if (!str) return ''
  const d = parseDate(str)
  if (!d || isNaN(d)) return str
  const s = d.toLocaleDateString('fr-CA', { day: 'numeric', month: 'long', year: 'numeric' })
  return s.charAt(0).toUpperCase() + s.slice(1)
}

const nomMoisAffiche = computed(() => {
  const d = new Date(moisAffiche.value.annee, moisAffiche.value.mois, 1)
  return d.toLocaleDateString('fr-CA', { month: 'long', year: 'numeric' })
})

const peutAllerPrecedent = computed(() => {
  const debut = parseDate(dateDebutLocation.value)
  if (!debut) return false
  return (
    moisAffiche.value.annee > debut.getFullYear() ||
    (moisAffiche.value.annee === debut.getFullYear() && moisAffiche.value.mois > debut.getMonth())
  )
})

const peutAllerSuivant = computed(() => {
  const fin = parseDate(dateFinLocation.value)
  if (!fin) return false
  return (
    moisAffiche.value.annee < fin.getFullYear() ||
    (moisAffiche.value.annee === fin.getFullYear() && moisAffiche.value.mois < fin.getMonth())
  )
})

function moisPrecedent() {
  if (!peutAllerPrecedent.value) return
  if (moisAffiche.value.mois === 0) {
    moisAffiche.value = { annee: moisAffiche.value.annee - 1, mois: 11 }
  } else {
    moisAffiche.value = { annee: moisAffiche.value.annee, mois: moisAffiche.value.mois - 1 }
  }
}

function moisSuivant() {
  if (!peutAllerSuivant.value) return
  if (moisAffiche.value.mois === 11) {
    moisAffiche.value = { annee: moisAffiche.value.annee + 1, mois: 0 }
  } else {
    moisAffiche.value = { annee: moisAffiche.value.annee, mois: moisAffiche.value.mois + 1 }
  }
}

const semaines = computed(() => {
  const { annee, mois } = moisAffiche.value
  const premierJour = new Date(annee, mois, 1)
  const dernierJour = new Date(annee, mois + 1, 0)

  const jours = []
  // Décalage lundi = 0 (convention française)
  const decalage = (premierJour.getDay() + 6) % 7
  for (let i = 0; i < decalage; i++) jours.push(null)
  for (let d = 1; d <= dernierJour.getDate(); d++) jours.push(new Date(annee, mois, d))
  while (jours.length % 7 !== 0) jours.push(null)

  const result = []
  for (let i = 0; i < jours.length; i += 7) result.push(jours.slice(i, i + 7))
  return result
})

function estDansRange(jour) {
  if (!jour) return false
  const debut = parseDate(dateDebutLocation.value)
  const fin = parseDate(dateFinLocation.value)
  if (!debut || !fin) return false
  return jour >= debut && jour <= fin
}

function estReserve(jour) {
  return datesReservees.value.has(toStr(jour))
}

function estDisponible(jour) {
  return estDansRange(jour) && !estReserve(jour)
}

// Vérifie qu'il n'y a aucune date réservée entre debut et fin (inclus)
function rangeValide(debut, fin) {
  let d = new Date(debut)
  while (d <= fin) {
    if (datesReservees.value.has(toStr(d))) return false
    d = new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1)
  }
  return true
}

function classeJour(jour) {
  if (!jour) return ['cal-vide']

  if (!estDansRange(jour)) return ['cal-hors-range']
  if (estReserve(jour)) return ['cal-reserve']

  const classes = ['cal-dispo', 'cal-cliquable']
  const str = toStr(jour)

  if (
    (dateDebutChoisie.value && str === toStr(dateDebutChoisie.value)) ||
    (dateFinChoisie.value && str === toStr(dateFinChoisie.value))
  ) {
    classes.push('cal-extremite')
  } else if (
    dateDebutChoisie.value &&
    dateFinChoisie.value &&
    jour > dateDebutChoisie.value &&
    jour < dateFinChoisie.value
  ) {
    classes.push('cal-dans-range')
  }

  return classes
}

function selectionnerJour(jour) {
  if (!jour || !estDisponible(jour)) return

  // Aucune sélection ou sélection complète → nouveau début
  if (!dateDebutChoisie.value || dateFinChoisie.value) {
    dateDebutChoisie.value = jour
    dateFinChoisie.value = null
    return
  }

  // Deuxième clic → définir la fin
  let debut = dateDebutChoisie.value
  let fin = jour
  if (jour < debut) {
    debut = jour
    fin = dateDebutChoisie.value
  }

  if (rangeValide(debut, fin)) {
    dateDebutChoisie.value = debut
    dateFinChoisie.value = fin
  } else {
    // Réservation dans le range → recommencer depuis ce clic
    dateDebutChoisie.value = jour
    dateFinChoisie.value = null
  }
}

onMounted(async () => {
  try {
    const res = await fetch(`/api/location/${idLocation}`)
    const data = await res.json()
    if (res.ok) {
      prix.value = data.Prix
      choixPaiement.value = data.TypePaiement
      adresse.value = data.Adresse
      photo.value = data.Photo
      vendeurNom.value = data.NomUtilisateur
      nomJeu.value = data.NomJeu
      vendeurId.value = data.LocateurId
      typeConsole.value = data.TypeConsole
      dateDebutLocation.value = data.DateDebut
      dateFinLocation.value = data.DateFin

      const debutLoc = parseDate(data.DateDebut)
      if (debutLoc) {
        moisAffiche.value = { annee: debutLoc.getFullYear(), mois: debutLoc.getMonth() }
      }
    } else if (res.status >= 500) {
      router.push('/erreur/500')
      return
    }
  } catch (e) {
    router.push('/erreur/500')
    return
  }

  try {
    const res2 = await fetch(`/api/reservation/${idLocation}`)
    const data2 = await res2.json()
    if (res2.ok && Array.isArray(data2)) {
      const set = new Set()
      data2.forEach(r => {
        let d = parseDate(r.DateDebutReservation)
        const fin = parseDate(r.DateFinReservation)
        if (d && fin) {
          while (d <= fin) {
            set.add(toStr(d))
            d = new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1)
          }
        }
      })
      datesReservees.value = set
    }
  } catch (e) {
    console.error('Erreur chargement réservations:', e)
  }
})

async function louer() {
  if (!dateDebutChoisie.value || !dateFinChoisie.value) return

  try {
    if (choixPaiement.value === 'En ligne') {
      const res = await fetch('/api/paiement/checkout-location', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location_id: idLocation,
          locataire_id: auth.userId,
          nom_jeu: nomJeu.value,
          prix_par_jour: prix.value,
          date_debut: toStr(dateDebutChoisie.value),
          date_fin: toStr(dateFinChoisie.value),
        }),
      })
      const data = await res.json()
      if (res.ok && data.url) {
        window.location.href = data.url
      } else if (res.status >= 500) {
        router.push('/erreur/500')
      } else {
        notif.setNotif('Erreur lors de la création du paiement', 'danger')
      }
    } else {
      const formData = new FormData()
      formData.append('dateDebut', toStr(dateDebutChoisie.value))
      formData.append('dateFin', toStr(dateFinChoisie.value))
      formData.append('locataireId', auth.userId)

      const res = await fetch(`/api/reservation/${idLocation}`, {
        method: 'POST',
        body: formData,
      })
      if (res.ok) {
        const evalData = new FormData()
        evalData.append('nomJeu', nomJeu.value)
        evalData.append('vendeurId', vendeurId.value)
        evalData.append('evaluateurId', auth.userId)
        await fetch('/api/evaluation', { method: 'POST', body: evalData })
        notif.setNotif('Jeu loué avec succès !')
        router.push('/louer')
      } else if (res.status === 400) {
        notif.setNotif('Dates invalides ou champs manquants.', 'danger')
      } else if (res.status === 405) {
        router.push('/erreur/405')
      } else if (res.status >= 500) {
        router.push('/erreur/500')
      }
    }
  } catch (e) {
    router.push('/erreur/500')
  }
}
</script>

<style scoped>
.cal-grid {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
  user-select: none;
}

.cal-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.cal-cell {
  text-align: center;
  padding: 8px 4px;
  font-size: 0.9rem;
  border: 1px solid #f0f0f0;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cal-header {
  background-color: #6c757d;
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
}

.cal-vide {
  background-color: #f8f9fa;
}

.cal-hors-range {
  background-color: #e9ecef;
  color: #adb5bd;
}

.cal-reserve {
  background-color: #f8d7da;
  color: #842029;
  text-decoration: line-through;
  cursor: not-allowed;
}

.cal-dispo {
  background-color: #d1e7dd;
  color: #0a3622;
}

.cal-cliquable {
  cursor: pointer;
}

.cal-cliquable:hover {
  filter: brightness(0.88);
}

.cal-dans-range {
  background-color: #cfe2ff !important;
  color: #084298 !important;
}

.cal-extremite {
  background-color: #0d6efd !important;
  color: white !important;
  font-weight: bold;
  border-radius: 50%;
}

.legende-carre {
  display: inline-block;
  width: 14px;
  height: 14px;
  border-radius: 3px;
  flex-shrink: 0;
}
</style>
