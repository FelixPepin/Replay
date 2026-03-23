<template>
    <main class="container mt-5">
        <div class="card p-4 shadow-sm" style="background-color: #fde8e8; border-radius: 20px;">
            <div class="row">

                <div class="col-md-6">
                    <h2 class="fw-bolder mb-3 text-black">{{ nomJeu }}</h2>

                    <p class="text-uppercase fw-bolder mb-2 text-black ">Détails du jeu :</p>
                    <p class="mb-1 text-black">Prix : {{ prix }} $</p>
                    <!-- <p class="mb-1 text-black">Vendeur : {{ nom }}</p> -->
                    <p class="mb-1 text-black">Livraison : {{ choixLivraison }}</p>
                    <p class="mb-1 text-black">Paiement : {{ choixPaiement }}</p>
                    <p class="mb-1 text-black">Console : {{ typeConsole }}</p>
                </div>

                <div class="col-md-6 d-flex align-items-center justify-content-center">
                    <img :src="`/static/images/ajouts/${photo}`" :alt="nomJeu" class="img-fluid rounded"
                        style="max-height: 250px; object-fit: cover;" />
                </div>

            </div>

            <div class="d-flex justify-content-end gap-3 mt-4">
                <button @click="() => {notif.clear;router.back()}" class="btn btn-danger rounded-pill px-4">
                    <i class="fi fi-br-arrow-left me-1"></i> Retour
                </button>
                <button @click="acheter" class="btn btn-success rounded-pill px-4">
                    <i class="fi fi-br-shopping-cart me-1"></i> Acheter
                </button>
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
const typeConsole = ref ('')
const estVendu = ref('')

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
            typeConsole.value = data.TypeConsole
            estVendu.value = data.estVendu
        }
    } catch (e) {
        console.error('Erreur chargement:', e)
    }
})

async function acheter() {
    try {
        const res = await fetch(`/api/vente/${idVente}/acheter`, { method: 'POST' })
        if (res.ok) {
            notif.setNotif("Jeu acheté avec succès !")
            router.push('/achat')
        }
    } catch (e) {
        console.error('Erreur achat:', e)
    }
}
</script>