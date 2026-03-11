<template>
  <main>
    <div class="container mt-2">
      <div class="row">
        <div v-if="auth.userId === vendeurId" class="col-mb-3">
          <h1 class="mb-4">Modifier une vente</h1>
          <div v-if="Object.keys(erreurs).length" class="alert alert-danger">
            <ul class="mb-0">
              <li v-for="(msg, champ) in erreurs" :key="champ">{{ msg }}</li>
            </ul>
          </div>

          <form
            @submit.prevent="modifierVente"
            method="post"
            enctype="multipart/form-data"
            novalidate
            action="/api/vendre"
          >
            <div class="mb-3">
              <label for="prix" class="form-label fw-bold">Prix</label>
              <input v-model="prix" type="number" id="prix" name="prix" class="form-control" />
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
              <fieldset>
                <legend class="col-form-label pt-0 fw-bold">Type de livraison</legend>
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="choixLivraison"
                    id="choixLivraisonPoste"
                    value="Par la poste"
                    v-model="choixLivraison"
                  />
                  <label class="form-check-label" for="choixLivraisonPoste"
                    >Livraison par la poste</label
                  >
                </div>
                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="choixLivraison"
                    id="choixLivraisonEnMainPropre"
                    value="En main propre"
                    v-model="choixLivraison"
                  />
                  <label class="form-check-label" for="choixLivraisonEnMainPropre"
                    >Venir chercher en main propre</label
                  >
                </div>
              </fieldset>
            </div>
            <div class="mb-3" v-if="choixLivraison === 'En main propre'">
              <label for="adresse" class="form-label fw-bold">Adresse</label>
              <input
                v-model="adresse"
                type="text"
                id="adresse"
                name="adresse"
                class="form-control"
              />
            </div>
            <button type="submit" class="btn btn-primary w-100">Modifier la vente.</button>
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

const photo = ref('')
const nomJeu = ref('')
const prix = ref('')
const choixPaiement = ref('')
const choixLivraison = ref('')
const adresse = ref('')
const erreurs = reactive({})
const vendeurId = ref('')

onMounted(async () => {
  try {
    const res = await fetch(`/api/vente/${idVente}`)
    const data = await res.json()
    if (res.ok) {
      prix.value = data.Prix
      choixLivraison.value = data.TypeLivraison
      choixPaiement.value = data.TypePaiement
      adresse.value = data.Adresse ?? ''
      photo.value = data.Photo
      nomJeu.value = data.NomJeu
      vendeurId.value = data.VendeurId
    } else {
      erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    }
  } catch (e) {
    erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    return
  }
})

async function modifierVente() {
  console.log('AppelleModifierEnVente')
  Object.keys(erreurs).forEach((k) => delete erreurs[k])

  if (!prix.value) erreurs.prix = 'Le prix du jeu est requis'
  if (prix.value > 60) erreurs.prix = 'Un jeu en revente ne peut pas valoir plus de 60$'
  if (!choixPaiement.value)
    erreurs.choixPaiement = 'Veuillez choisir la méthode de paiement désirée'
  if (!choixLivraison.value)
    erreurs.choixLivraison = 'Veuillez choisir la méthode de livraison désirée'
  if (!adresse.value && choixLivraison.value === 'En main propre')
    erreurs.adresse = "L'adresse est requise lorsque la méthode de livraison est en main propre."

  if (Object.keys(erreurs).length > 0) return

  try {
    const formData = new FormData()
    formData.append('prix', prix.value)
    formData.append('choixPaiement', choixPaiement.value)
    formData.append('choixLivraison', choixLivraison.value)
    formData.append('adresse', adresse.value)
    formData.append('vendeurId', auth.userId)

    const reponse = await fetch(`/api/modifier/${idVente}`, {
      method: 'POST',
      body: formData,
    })

    const data = await reponse.json()

    if (reponse.ok) {
      notif.setNotif('Vente modifiée avec succès')
      router.push('/mesVentes')
    } else {
      Object.assign(erreurs, data.erreurs)
    }
  } catch (e) {
    erreurs.serveur = 'Impossible de contacter le serveur'
  }
}
</script>
