<template>
  <main>
    <div class="container mt-2">
      <div class="row">
        <div v-if="auth.role === 'vendeur'" class="col-mb-3">
          <h1 class="mb-4">Mettre un jeu en vente</h1>
          <div v-if="Object.keys(erreurs).length" class="alert alert-danger">
            <ul class="mb-0">
              <li v-for="(msg, champ) in erreurs" :key="champ">{{ msg }}</li>
            </ul>
          </div>

          <form
            @submit.prevent="mettreEnVente"
            method="post"
            enctype="multipart/form-data"
            novalidate
            action="/api/vendre"
          >
            <div class="mb-3">
              <label for="nomJeu" class="form-label fw-bold">Nom du jeu</label>
              <input v-model="nomJeu" type="text" id="nomJeu" name="nomJeu" class="form-control" />
            </div>
            <div class="mb-3">
              <label for="prix" class="form-label fw-bold">Prix</label>
              <input v-model="prix" type="number" id="prix" name="prix" class="form-control" />
            </div>
            <div class="mb-3">
              <label for="typeConsole" class="form-label fw-bold">Type de console</label>
              <select v-model="typeConsole" id="typeConsole" name="typeConsole" class="form-select">
                <option value="">-- Sélectionner --</option>
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

            <div class="mb-3">
              <label for="photo" class="form-label fw-bold">Photo du jeu</label>
              <input
                type="file"
                name="photo"
                id="photo"
                class="form-control"
                @change="changementPhoto"
              />
              <div v-if="vuePhoto" class="mt-3">
                <img :src="vuePhoto" style="max-width: 200px" class="img-thumbnail" />
              </div>
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
            <button type="submit" class="btn btn-primary w-100">Vendre le jeu</button>
          </form>
        </div>
        <div v-else>
          <p class="alert alert-warning">
            Vous devez être vendeur pour vendre un jeu.
            <router-link to="/login">Se connecter</router-link>
          </p>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
export default {
  setup() {
    const auth = useAuthStore()
    const notif = useNotifStore()
    const router = useRouter()

    const vuePhoto = ref(null)
    const nomJeu = ref('')
    const prix = ref('')
    const photo = ref(null)
    const typeConsole = ref('')
    const choixPaiement = ref('')
    const choixLivraison = ref('')
    const adresse = ref('')
    const erreurs = reactive({})

    async function mettreEnVente() {
      console.log('AppelleMettreEnVente')
      Object.keys(erreurs).forEach((k) => delete erreurs[k])

      if (nomJeu.value.trim().length < 3 || nomJeu.value.trim().length > 20)
        erreurs.nomJeu = 'Le nom du jeu doit être entre 3 et 20 caractères'
      if (!nomJeu.value.trim()) erreurs.nomJeu = 'Le nom du jeu est requis'
      if (!prix.value) erreurs.prix = 'Le prix du jeu est requis'
      if (prix.value > 60) erreurs.prix = 'Un jeu en revente ne peut pas valoir plus de 60$'
      if (!photo.value) {
        erreurs.photo = 'La photo du jeu est requis'
      } else {
        const nomFichier = photo.value.name
        const extension = nomFichier.split('.').pop().toUpperCase()
        const extensionPermis = ['JPG', 'JPEG', 'PNG', 'WEBP']
        if (!extensionPermis.includes(extension))
          erreurs.photo = 'Seuls les fichier JPG, JPEG, PNG et WEBP sont acceptés'
      }
      if (!typeConsole.value) erreurs.typeConsole = 'Veuillez choisir le type de console'
      if (!choixPaiement.value)
        erreurs.choixPaiement = 'Veuillez choisir la méthode de paiement désirée'
      if (!choixLivraison.value)
        erreurs.choixLivraison = 'Veuillez choisir la méthode de livraison désirée'
      if (!adresse.value && choixLivraison.value === 'mainPropre')
        erreurs.adresse =
          "L'adresse est requise lorsque la méthode de livraison est en main propre."

      if (Object.keys(erreurs).length > 0) return

      try {
        const formData = new FormData()
        formData.append('nomJeu', nomJeu.value)
        formData.append('prix', prix.value)
        formData.append('photo', photo.value)
        formData.append('typeConsole', typeConsole.value)
        formData.append('choixPaiement', choixPaiement.value)
        formData.append('choixLivraison', choixLivraison.value)
        formData.append('adresse', adresse.value)
        formData.append('vendeurId', auth.userId)

        const reponse = await fetch('/api/vendre', {
          method: 'POST',
          body: formData,
        })

        const data = await reponse.json()

        if (reponse.ok) {
          notif.setNotif('Jeu mis en vente avec succès')
          router.push('/mesVentes')
        } else {
          Object.assign(erreurs, data.erreurs)
        }
      } catch (e) {
        erreurs.serveur = 'Impossible de contacter le serveur'
      }
    }
    function changementPhoto(e) {
      const fichier = e.target.files[0] || null
      photo.value = fichier
      if (fichier) {
        vuePhoto.value = URL.createObjectURL(fichier)
      } else {
        vuePhoto.value = null
      }
    }
    return {
      auth,
      vuePhoto,
      nomJeu,
      prix,
      photo,
      typeConsole,
      choixPaiement,
      choixLivraison,
      adresse,
      erreurs,
      mettreEnVente,
      changementPhoto,
    }
  },
}
</script>
