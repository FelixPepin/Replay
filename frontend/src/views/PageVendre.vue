<template>
    <main>
        <div class="container mt-2">
            <div class="row">
                <div class="col-mb-3">
                    <h1 class="mb-4">Mettre un jeu en vente</h1>

                    <div v-if="Object.keys(erreurs).length" class="alert alert-danger">
                        <ul class="mb-0">
                            <li v-for="(msg, champ) in erreurs" :key="champ">{{ msg }}</li>
                        </ul>
                    </div>

                    <form @submit.prevent="mettreEnVente" method="post" enctype="multipart/form-data" novalidate>
                        <div class="mb-3">
                            <label for="nomJeu" class="form-label fw-bold">Nom du jeu</label>
                            <input v-model="nomJeu" type="text" id="nomJeu" name="nomJeu" class="form-control" />
                        </div>
                        <div class="mb-3">
                            <label for="prix" class="form-label fw-bold">Prix</label>
                            <input v-model="prix" type="number" id="prix" name="prix" class="form-control" />
                        </div>

                        <div class="mb-3">
                            <label for="photo" class="form-label fw-bold">Photo du jeu</label>
                            <input v-model="photo" type="file" name="photo" id="photo" class="form-control" />
                        </div>
                        <div class="mb-3">
                            <fieldset>
                                <legend class="col-form-label pt-0 fw-bold">Mode de paiement</legend>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="choixPaiement" id="choixPaiementEnLigne"
                                    v-model="choixPaiement" value="enLigne">
                                    <label class="form-check-label" for="choixPaiementEnLigne">Paiement en ligne</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="choixPaiement" id="choixPaiementEnMainPropre"
                                    v-model="choixPaiement" value="mainPropre">
                                    <label class="form-check-label" for="choixPaiementEnMainPropre">Paiement en main propre</label>
                                </div>
                            </fieldset>
                        </div>
                        <div class="mb-3">
                            <fieldset>
                                <legend class="col-form-label pt-0 fw-bold">Type de livraison</legend>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="choixLivraison" id="choixLivraisonPoste"
                                    value="parPoste" v-model="choixLivraison">
                                    <label class="form-check-label" for="choixLivraisonPoste">Livraison par la poste</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="choixLivraison" id="choixLivraisonEnMainPropre"
                                    value="mainPropre" v-model="choixLivraison">
                                    <label class="form-check-label" for="choixLivraisonEnMainPropre">Venir chercher en main propre</label>
                                </div>
                            </fieldset>
                        </div>
                        <div class="mb-3" v-if="choixLivraison === 'mainPropre'">
                            <label for="adresse" class="form-label fw-bold">Adresse</label>
                            <input v-model="adresse" type="text" id="adresse" name="adresse" class="form-control"/>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Vendre le jeu</button>
                    </form>
                </div>
            </div>
        </div>
    </main>
</template>

<script>
import { ref, reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
const router = useRouter()

const nomJeu = ref('')
const prix = ref('')
const photo = ref('')
const choixPaiement = ref('')
const choixLivraison = ref('')
const adresse = ref('')
const erreurs = reactive({})

async function mettreEnVente() {
    console.log("AppelleMettreEnVente")
    Object.keys(erreurs).forEach(k => delete erreurs[k])

    if (!nomJeu.value.trim()) erreurs.nomJeu = "Le nom du jeu est requis"
    if (!prix.value) erreurs.prix = "Le prix du jeu est requis"
    if (prix.value > 60) erreurs.prix = "Un jeu en revente ne peut pas valoir plus de 60$"
    if (!photo.value.trim()) erreurs.photo = "La photo du jeu est requis"
    if (!choixPaiement.value) erreurs.choixPaiement = "Veuillez choisir la méthode de paiement désirée"
    if (!choixLivraison.value) erreurs.choixLivraison = "Veuillez choisir la méthode de livraison désirée"
    if (!adresse.value && choixLivraison.value==="mainPropre") erreurs.adresse = "L'adresse est requise lorsque la méthode de livraison est en main propre."


    if (Object.keys(erreurs).length > 0) return

    try {
        const reponse = await fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username.value,
                email: email.value,
                password: password.value,
                confirm: confirm.value
            })
        })

        const data = await reponse.json()

        if (reponse.ok) {
            router.push('/')
        } else {
            Object.assign(erreurs, data.erreurs)
        }
    } catch (e) {
        erreurs.serveur = "Impossible de contacter le serveur"
    }
}

</script>
