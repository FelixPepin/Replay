<template>
    <main>
        <div class="container mt-2">
            <div class="row">
                <div v-if="auth.userId === vendeurId " class="col-mb-3">
                    <h1 class="mb-4">Mettre un jeu en vente</h1>
                    <div v-if="Object.keys(erreurs).length" class="alert alert-danger">
                        <ul class="mb-0">
                            <li v-for="(msg, champ) in erreurs" :key="champ">{{ msg }}</li>
                        </ul>
                    </div>

                    <form @submit.prevent="supprimerVente" method="post" enctype="multipart/form-data" novalidate>
                        <button type="submit" class="btn btn-primary w-100">Vendre le jeu</button>
                    </form>
                </div>
                <div v-else>
                    <p class="alert alert-warning">
                        Vous devez être le vendeur pour modifier ce jeu.
                    </p>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
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
const erreurs = reactive({})
const vendeurId = ref('')


onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:5000/vente/${idVente}`)
    const data = await res.json()
    if (res.ok) {
        prix.value = data.Prix
        choixLivraison.value = data.TypeLivraison
        choixPaiement.value = data.TypePaiement
        adresse.value = data.Adresse ?? ""
        vendeurId.value = data.VendeurId
    } else {
      erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    }
  } catch (e) {
    erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
    return
  }
})


async function supprimerVente() {


    try{

        const reponse = await fetch(`http://localhost:5000/modifier/${idVente}`, {
            method: 'POST',
            body: formData,
        })

        const data = await reponse.json()

        if (reponse.ok) {
            router.push({
                path: '/',
                state: { success: 'Vente modifier avec succès' },
            })
        } else {
            Object.assign(erreurs, data.erreurs)
        }
    } catch (e) {
        erreurs.serveur = 'Impossible de contacter le serveur'
    }
}
</script>
