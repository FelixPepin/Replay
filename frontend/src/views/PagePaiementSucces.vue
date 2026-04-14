<template>
  <main class="container mt-5 text-center">
    <div class="card p-5 shadow-sm" style="background-color: #fde8e8; border-radius: 20px; max-width: 500px; margin: auto;">
      <div v-if="chargement">
        <div class="spinner-border text-success mb-3" role="status"></div>
        <p class="text-black">Confirmation du paiement en cours...</p>
      </div>

      <div v-else-if="succes">
        <i class="fi fi-br-check-circle" style="font-size: 3rem; color: #198754;"></i>
        <h2 class="fw-bold text-black mt-3">Paiement réussi !</h2>
        <p class="text-black mt-2">{{ messageSucces }}</p>
        <button @click="router.push(routeRetour)" class="btn btn-success rounded-pill px-4 mt-3">
          Retour à l'accueil
        </button>
      </div>

      <div v-else>
        <i class="fi fi-br-cross-circle" style="font-size: 3rem; color: #dc3545;"></i>
        <h2 class="fw-bold text-black mt-3">Erreur de paiement</h2>
        <p class="text-black mt-2">{{ messageErreur }}</p>
        <button @click="router.push('/')" class="btn btn-danger rounded-pill px-4 mt-3">
          Retour à l'accueil
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const chargement = ref(true)
const succes = ref(false)
const messageSucces = ref('')
const messageErreur = ref('Une erreur est survenue.')
const routeRetour = ref('/achat')

onMounted(async () => {
  const sessionId = route.query.session_id
  if (!sessionId) {
    messageErreur.value = 'Session de paiement introuvable.'
    chargement.value = false
    return
  }

  try {
    const res = await fetch(`/api/paiement/confirmer?session_id=${sessionId}`)
    const data = await res.json()

    if (res.ok && data.succes) {
      succes.value = true
      if (data.type === 'achat') {
        messageSucces.value = 'Votre achat a été confirmé. Bonne partie !'
        routeRetour.value = '/achat'
      } else {
        messageSucces.value = 'Votre location a été confirmée. Bonne partie !'
        routeRetour.value = '/louer'
      }
    } else {
      messageErreur.value = data.erreur || 'Le paiement n\'a pas pu être confirmé.'
    }
  } catch (e) {
    console.error('Erreur confirmation paiement:', e)
    messageErreur.value = 'Impossible de contacter le serveur.'
  }

  chargement.value = false
})
</script>
