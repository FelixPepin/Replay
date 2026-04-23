<template>
  <main>
    <div class="container mt-2">
      <div class="row">
        <div v-if="auth.userId === vendeurId" class="col-mb-3">
          <h1 class="mb-4">Modifier une location</h1>
          <div v-if="Object.keys(erreurs).length" class="alert alert-danger">
            <ul class="mb-0">
              <li v-for="(msg, champ) in erreurs" :key="champ">{{ msg }}</li>
            </ul>
          </div>

          <form
            @submit.prevent="modifierLocation"
            method="post"
            enctype="multipart/form-data"
            novalidate
            action="/api/location"
          >
            <div class="mb-3">
              <label for="prix" class="form-label fw-bold">Prix</label>
              <input v-model="prix" type="number" step="0.01" id="prix" name="prix" class="form-control" />
            </div>
            <div class="mb-3">
              <fieldset>
                <legend class="col-form-label pt-0 fw-bold">Mode de paiement</legend>
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="choixPaiement"
                    id="choixPaiementEnLigne"
                    v-model="choixPaiement"
                    value="En ligne"
                  />
                  <label class="form-check-label" for="choixPaiementEnLigne"
                    >Paiement en ligne</label
                  >
                </div>
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="choixPaiement"
                    id="choixPaiementEnMainPropre"
                    v-model="choixPaiement"
                    value="En main propre"
                  />
                  <label class="form-check-label" for="choixPaiementEnMainPropre"
                    >Paiement en main propre</label
                  >
                </div>
              </fieldset>
            </div>
            <div class="mb-3">
              <label for="adresse" class="form-label fw-bold">Adresse</label>
              <input
                v-model="adresse"
                type="text"
                id="adresse"
                name="adresse"
                class="form-control"
              />
            </div>
            <div class="mb-3">
              <label for="dateDebut" class="form-label fw-bold">Date de début</label>
              <input v-model="dateDebut" type="date" id="dateDebut" name="dateDebut" class="form-control" />
            </div>
            <div class="mb-3">
              <label for="dateFin" class="form-label fw-bold">Date de fin</label>
              <input v-model="dateFin" type="date" id="dateFin" name="dateFin" class="form-control" />
            </div>
            <button type="submit" class="btn btn-primary w-100">Modifier la location.</button>
          </form>
        </div>
        <div v-else>
          <p class="alert alert-warning">Vous devez être le vendeur pour modifier cette vente.</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
const auth = useAuthStore()
const notif = useNotifStore()
const router = useRouter()
const route = useRoute()

const idVente = route.params.id

const prix = ref('')
const choixPaiement = ref('')
const adresse = ref('')
const dateDebut = ref('')
const dateFin = ref('')
const erreurs = reactive({})
const vendeurId = ref('')

onMounted(async () => {
  try {
    const res = await fetch(`/api/location/${idVente}`)
    const data = await res.json()
    if (res.ok) {
      prix.value = data.Prix
      choixPaiement.value = data.TypePaiement
      adresse.value = data.Adresse ?? ''
      dateDebut.value = data.DateDebut ? new Date(data.DateDebut).toISOString().split('T')[0] : ''
      dateFin.value = data.DateFin ? new Date(data.DateFin).toISOString().split('T')[0] : ''
      vendeurId.value = data.LocateurId
    } else {
      erreurs.serveur = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    }
  } catch (e) {
    erreurs.serveur = 'Erreur lors du chargement'
    return
  }
})

async function modifierLocation() {
  console.log('AppelleModifierLocation')
  Object.keys(erreurs).forEach((k) => delete erreurs[k])

  if (!prix.value) erreurs.prix = 'Le prix du jeu est requis'
  if (prix.value > 60) erreurs.prix = 'Un jeu en revente ne peut pas valoir plus de 60$'
  if (!choixPaiement.value)
    erreurs.choixPaiement = 'Veuillez choisir la méthode de paiement désirée'
  if (!adresse.value)
    erreurs.adresse = "L'adresse est requise."
  if (!dateDebut.value) erreurs.dateDebut = 'Veuillez entrez une date de début'
  if (dateDebut.value && dateDebut.value < new Date().toISOString().split('T')[0])
    erreurs.dateDebut = 'La date de début ne peut pas être dans le passé'
  if (!dateFin.value) erreurs.dateFin = 'Veuillez entrez une date de fin'
  if (dateFin.value && dateFin.value <= dateDebut.value)
        erreurs.dateFin = 'La date de fin doit être après la date de début'

  if (Object.keys(erreurs).length > 0) return

  try {
    const formData = new FormData()
    formData.append('prix', prix.value)
    formData.append('choixPaiement', choixPaiement.value)
    formData.append('adresse', adresse.value)
    formData.append('vendeurId', auth.userId)
    formData.append('dateDebut', dateDebut.value)
    formData.append('dateFin', dateFin.value)

    const reponse = await fetch(`/api/modifierLocation/${idVente}`, {
      method: 'POST',
      body: formData,
    })

    const data = await reponse.json()

    if (reponse.ok) {
      notif.setNotif('Location modifiée avec succès')
      router.push('/mesLocations')
    } else {
      Object.assign(erreurs, data.erreurs)
    }
  } catch (e) {
    erreurs.serveur = 'Impossible de contacter le serveur'
  }
}
</script>
