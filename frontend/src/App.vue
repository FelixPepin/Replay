<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav class="navbar navbar-expand">
        <RouterLink to="/vendre" class="btn btn-primary p-2 text-black">Vendre un jeu</RouterLink>
        <RouterLink to="/register" class="btn btn-primary p-2 text-black">Inscription</RouterLink>
      </nav>
  </header>

  <RouterView />
</template>

