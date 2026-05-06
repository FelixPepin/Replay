<template>
  <main>
    <div class="container mt-4" style="max-width: 500px">
      <h1 class="mb-4">Évaluer un vendeur</h1>

      <div v-if="erreurs" class="alert alert-danger">{{ erreurs }}</div>

      <div v-if="resultat" class="card shadow-sm p-4">
        <h5 class="mb-3">Évaluation soumise pour <strong>{{ evaluation.NomUtilisateur }}</strong></h5>
        <div class="d-flex justify-content-around text-center">
          <div>
            <div class="text-muted small mb-1">Avant</div>
            <div class="fs-4 fw-bold">{{ resultat.ancienneNote }}<span class="text-muted fs-6">/5</span></div>
            <div class="text-muted small">{{ resultat.ancienNbEvaluation }} évaluation{{ resultat.ancienNbEvaluation !== 1 ? 's' : '' }}</div>
          </div>
          <div class="d-flex align-items-center text-muted fs-4">→</div>
          <div>
            <div class="text-muted small mb-1">Après</div>
            <div class="fs-4 fw-bold text-success">{{ resultat.nouvelleNote }}<span class="text-muted fs-6">/5</span></div>
            <div class="text-muted small">{{ resultat.nouveauNbEvaluation }} évaluation{{ resultat.nouveauNbEvaluation !== 1 ? 's' : '' }}</div>
          </div>
        </div>
        <button class="btn btn-primary w-100 mt-4" @click="router.push('/mesEvaluations')">
          Retour à mes évaluations
        </button>
      </div>

      <div v-else-if="evaluation" class="card shadow-sm p-4">
        <p class="mb-1"><strong>Jeu :</strong> {{ evaluation.NomJeu }}</p>
        <p class="mb-1"><strong>Vendeur :</strong> {{ evaluation.NomUtilisateur }}</p>
        <p class="mb-3 text-muted small">
          Note actuelle : <strong>{{ evaluation.note }}/5</strong> — {{ evaluation.nbEvaluation }} évaluation{{ evaluation.nbEvaluation !== 1 ? 's' : '' }}
        </p>

        <label class="form-label fw-bold" for="note">Note :</label>
        <select id="note" v-model="note" class="form-select mb-4">
          <option value="0">0</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>

        <button class="btn btn-success w-100" @click="soumettre">
          Soumettre l'évaluation
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNotifStore } from '@/stores/notif'

const route = useRoute()
const router = useRouter()
const notif = useNotifStore()
const evaluation = ref(null)
const note = ref(0)
const erreurs = ref('')
const resultat = ref(null)

onMounted(async () => {
  try {
    const res = await fetch(`/api/evaluer/${route.params.idEvaluation}`)
    const data = await res.json()
    if (res.ok) {
      evaluation.value = data
    } else {
      erreurs.value = 'Erreur lors du chargement'
    }
  } catch (e) {
    erreurs.value = 'Erreur lors du chargement'
  }
})

async function soumettre() {
  try {
    const res = await fetch(`/api/evaluer/${evaluation.value.IdVendeur}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ note: note.value }),
    })
    if (!res.ok) {
      erreurs.value = "Erreur lors de l'envoi"
      return
    }

    const data = await res.json()
    await fetch(`/api/evaluation/${evaluation.value.Id}`, { method: 'DELETE' })

    notif.setNotif('Évaluation soumise avec succès !')
    resultat.value = data
  } catch (e) {
    erreurs.value = "Erreur lors de l'envoi"
  }
}
</script>
