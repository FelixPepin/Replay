<template>
  <main>
    <div class="container">
      <h1 class="mb-4 mt-2">Mes Évaluations</h1>
      <div v-if="notif.message" :class="`alert alert-${notif.type}`">
        {{ notif.message }}
      </div>
      <div v-if="erreurs" class="alert alert-danger">
        {{ erreurs }}
      </div>
      <p v-if="evalutions.length === 0 && !erreurs" class="alert alert-info">Vous n'avez aucune évaluation.</p>
      <div class="row">
        <div v-for="evalution in evalutions" :key="evalution.Id" class="col-md-6">
          <div class="card mb-4 shadow-sm">
            <img class="card-img-top w-100" :src="evaluationImg" />
            <div class="card-body">
              <h2 class="card-title">Nom du jeu : {{ evalution.NomJeu }}</h2>
              <p class="card-text">Vendeur : {{ evalution.NomUtilisateur }}</p>

              <RouterLink :to="`/evaluer/${evalution.Id}`" class="btn btn-warning p-2 text-black ms-5"
                >Évaluer</RouterLink
              >
              <button class="btn btn-danger p-2 text-black ms-5" @click="supprimerEvaluation(evalution.Id)">
                Ne pas évaluer
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import evaluationImg from '@/assets/images/evaluation.jpg'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
import { ref, onMounted, onUnmounted } from 'vue'

const evalutions = ref([])
const erreurs = ref('')
const auth = useAuthStore()
const notif = useNotifStore()

onUnmounted(() => notif.clear())

onMounted(async () => {
  try {
    const res = await fetch(`/api/mesEvaluations/${auth.userId}`)
    const data = await res.json()
    if (res.ok) {
      evalutions.value = data
    } else {
      erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    }
  } catch (e) {
    erreurs.value = 'Erreur lors du chargement'
  }
})

async function supprimerEvaluation(id) {
  try {
    const res = await fetch(`/api/evaluation/${id}`, { method: 'DELETE' })
    if (res.ok) {
      evalutions.value = evalutions.value.filter((e) => e.Id !== id)
    } else {
      erreurs.value = 'Erreur lors de la suppression'
    }
  } catch (e) {
    erreurs.value = 'Erreur lors de la suppression'
  }
}
</script>
