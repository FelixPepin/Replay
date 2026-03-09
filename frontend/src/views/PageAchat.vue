<template>
  <main class="container">
    <div class="container mt-5">
      <h1>Liste de jeux en vente</h1>
    </div>

    <div class="row">
      <div v-for="jeu in jeux" :key="jeu.id" class="col-lg-6 mb-3">
        <div class="card h-100">
          <div class="card-body">
            <h2 class="card-title h5">{{ jeu.nom }}</h2>
            <p class="card-text text-primary fw-bold">{{ jeu.prix }} $</p>
            <button class="btn btn-sm btn-success me-2">Ajouter au panier</button>
            <button class="btn btn-sm btn-success">Détails</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>
import { ref } from 'vue'

const jeux = ref([
  { id: 1, nom: 'God of War', prix: 12.5 },
  { id: 2, nom: 'The Legend of Zelda: Breath of the Wild', prix: 45.0 },
  { id: 3, nom: 'Elden Ring', prix: 35.0 },
  { id: 4, nom: 'Mario Kart 8 Deluxe', prix: 40.0 },
  { id: 5, nom: 'Spider-Man: Miles Morales', prix: 20.0 },
  { id: 6, nom: 'Red Dead Redemption 2', prix: 15.75 },
  { id: 7, nom: 'Minecraft', prix: 18.0 },
  { id: 8, nom: 'Hades', prix: 14.5 },
  { id: 9, nom: 'Cyberpunk 2077', prix: 25.0 },
  { id: 10, nom: 'Animal Crossing: New Horizons', prix: 38.0 },
])
</script>
