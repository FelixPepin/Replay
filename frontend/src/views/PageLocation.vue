<template>
    <main class="container">
        <div class="container mt-5">
            <h1>Liste de jeux disponible en location</h1>
        </div>

        <div class="mb-4 col-md-3">
            <select v-model="tri" class="form-select">
                <option value="alpha">Ordre alphabétique</option>
                <option value="prix_asc">Prix croissant</option>
                <option value="prix_desc">Prix décroissant</option>
            </select>
        </div>

        <div class="row">
            <div v-for="jeu in jeuxTriees" :key="jeu.Id" class="col-lg-6 mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h2 class="card-title h5">{{ jeu.NomJeu }}</h2>
                        <p class="card-text text-primary fw-bold">
                            <span class="text-black">Prix : </span> {{ jeu.Prix }} $
                        </p>
                        <p class="card-text text-primary fw-bold">
                            <span class="text-black">Console : </span> {{ jeu.TypeConsole }}
                        </p>
                        <button class="btn btn-sm btn-success me-2">Louer</button>
                        <button class="btn btn-sm btn-success">Détails</button>

                    </div>
                </div>
            </div>
        </div>
    </main>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue';
import axios from 'axios'
const tri = ref('alpha')
const jeux = ref([])

const jeuxTriees = computed(() => {
    const liste = [...jeux.value]
    if (liste.length === 0) return []

    if (tri.value === 'alpha')
        return liste.sort((a, b) => a.NomJeu.localeCompare(b.NomJeu))
    else if (tri.value === 'prix_asc')
        return liste.sort((a, b) => a.Prix - b.Prix)
    else if (tri.value === 'prix_desc')
        return liste.sort((a, b) => b.Prix - a.Prix)

    return liste
})

onMounted(async () => {
    try {
        const response = await axios.get('/api/locations')
        console.log('type:', typeof response.data)
        console.log('données:', response.data)

        jeux.value = Array.isArray(response.data) ? response.data : []
    } catch (err) {
        console.error('Erreur:', err)
    }
})
</script>
