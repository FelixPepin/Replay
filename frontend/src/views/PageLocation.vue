<template>
    <main class="container">
        <div class="container mt-5">
            <h1>Liste de jeux disponible en location</h1>
        </div>

        <div class="row">
            <div v-for="jeu in jeux" :key="jeu.id" class="col-lg-6 mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h2 class="card-title h5">{{ jeu.nom }}</h2>
                        <p class="card-text text-primary fw-bold">
                            <span class="text-black">Prix : </span> {{ jeu.prix }} $
                        </p>
                        <p class="card-text text-primary fw-bold">
                            <span class="text-black">Console : </span> {{ jeu.console }}
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
import { ref } from 'vue';

const jeux = ref([
    { id: 1, nom: "Ghost of Tsushima", prix: 2.50, console: "PS5", etat: "Comme neuf" },
    { id: 2, nom: "Super Mario Wonder", prix: 3.00, console: "Switch", etat: "Excellent" },
    { id: 3, nom: "Starfield", prix: 2.00, console: "Xbox Series", etat: "Bon état" },
    { id: 4, nom: "Final Fantasy VII Rebirth", prix: 4.00, console: "PS5", etat: "Neuf" },
    { id: 5, nom: "Metroid Dread", prix: 2.50, console: "Switch", etat: "Excellent" },
    { id: 6, nom: "Forza Horizon 5", prix: 2.00, console: "Xbox Series", etat: "Bon état" },
    { id: 7, nom: "Baldur's Gate 3", prix: 3.50, console: "PC / PS5", etat: "Comme neuf" },
    { id: 8, nom: "Hollow Knight: Silksong", prix: 1.50, console: "Multi", etat: "Neuf" },
    { id: 9, nom: "Resident Evil 4 Remake", prix: 3.00, console: "PS5 / Xbox", etat: "Excellent" },
    { id: 10, nom: "The Last of Us Part I", prix: 2.50, console: "PS5", etat: "Comme neuf" }
]);

</script>
