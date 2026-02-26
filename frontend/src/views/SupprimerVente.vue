<template>
    <main>
        <div class="container mt-2">
            <div class="row">
                <p>auth: {{ auth.userId }} ({{ typeof auth.userId }})</p>
<p>vendeur: {{ vendeurId }} ({{ typeof vendeurId }})</p>
                <div v-if="auth.userId === vendeurId" class="col-mb-3">
                    <h1 class="mb-4">Mettre un jeu en vente</h1>
                    <div class="card mb-4 shadow-sm">
                        <img class="card-img-top w-100" :src="`http://localhost:5000/static/images/ajouts/${photo}`" />
                        <div class="card-body">
                            <h2 class="card-title">Nom du jeu : {{ nomJeu }}</h2>
                            <p class="card-text">Prix : {{ prix }}$</p>
                            <p class="card-text">Livraison : {{ choixLivraison }}</p>
                            <p class="card-text">Paiement : {{ choixPaiement }}</p>
                            <p v-if="adresse" !="" class="card-text">Adresse : {{ adresse }}</p>
                            <RouterLink :to="`/modifier/${vente.Id}`" class="btn btn-warning p-2 text-black ms-5">
                                Modifier</RouterLink>
                            <RouterLink :to="`/supprimer/${vente.Id}`" class="btn btn-danger p-2 text-black ms-5">
                                Supprimer</RouterLink>
                        </div>
                    </div>
                    <form @submit.prevent="supprimerVente" method="post" enctype="multipart/form-data" novalidate>
                        <button type="submit" class="btn btn-primary w-100">Supprimer le jeu</button>
                    </form>
                </div>
                <div v-else>
                    <p class="alert alert-warning">Vous devez être le vendeur pour supprimer ce jeu.</p>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const idVente = route.params.id

const prix = ref('')
const choixPaiement = ref('')
const choixLivraison = ref('')
const adresse = ref('')
const vendeurId = ref('')
const photo = ref('')

onMounted(async () => {
    try {
        const res = await fetch(`http://localhost:5000/vente/${idVente}`)
        const data = await res.json()
        if (res.ok) {
            prix.value = data.Prix
            choixLivraison.value = data.TypeLivraison
            choixPaiement.value = data.TypePaiement
            adresse.value = data.Adresse ?? ''
            vendeurId.value = data.VendeurId
            photo.value = data.Photo
        } else {
            erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
        }
    } catch (e) {
        erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
        return
    }
})

async function supprimerVente() {
    try {
        const reponse = await fetch(`http://localhost:5000/supprimer/${idVente}`, {
            method: 'POST',
        })

        const data = await reponse.json()

        if (reponse.ok) {
            router.push({
                path: '/',
                state: { success: 'Vente supprimer avec succès' },
            })
        } else {
            Object.assign(erreurs, data.erreurs)
        }
    } catch (e) {
        erreurs.serveur = 'Impossible de contacter le serveur'
    }
}
</script>
