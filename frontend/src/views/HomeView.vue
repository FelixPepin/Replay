<script setup>
import { ref } from 'vue'

const carouselItems = ref([
  { id: 1, img: 'jeux1.jpg', alt: 'Jeux action' },
  { id: 2, img: 'jeux2.jpg', alt: 'Jeux aventure' },
  { id: 3, img: 'jeux3.jpg', alt: 'Jeux rétro' }
])

const getImageUrl = (name) => {
  return new URL(`../assets/images/${name}`, import.meta.url).href
}
</script>

<template>
  <main>
    <section class="hero-section d-flex align-items-center">
      <div class="container">
        <div class="row align-items-center">

          <div class="col-lg-6 text-white py-5">
            <h1 class="display-3 fw-bold mb-3">
              Rejoue mieux avec <span class="text-warning">RePlay</span>.
            </h1>
            <p class="lead mb-4">
              Donnez une seconde vie aux jeux usagés. La plateforme hybride pour
              <strong>acheter, vendre et louer</strong> vos titres préférés,
              même avec un petit budget.
            </p>

            <div class="d-flex flex-wrap gap-3">
              <RouterLink to="/achat"
                class="btn btn-warning btn-lg px-4 fw-bold shadow text-decoration-none d-flex align-items-center">
                🛒 Acheter
              </RouterLink>
              <RouterLink to="/vendre"
                class="btn btn-outline-light btn-lg px-4 text-decoration-none d-flex align-items-center">
                💰 Vendre
              </RouterLink>
            </div>

            <div class="mt-4 d-flex align-items-center opacity-75">
              <span class="badge bg-success me-2">Sécurisé</span>
              <span>Intermédiaire de confiance pour toutes vos transactions</span>
            </div>
          </div>

          <div class="col-lg-6 d-none d-lg-block">
            <div id="heroCarousel" class="carousel slide shadow-lg rounded-4 overflow-hidden" data-bs-ride="carousel">
              <div class="carousel-inner">
                <div v-for="(item, index) in carouselItems" :key="item.id"
                  :class="['carousel-item', { active: index === 0 }]">
                  <img :src="getImageUrl(item.img)" class="d-block w-100 hero-img" :alt="item.alt">
                </div>
              </div>
              <button class="carousel-control-prev" type="button" data-bs-target="#heroCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#heroCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
              </button>
            </div>
          </div>

        </div>
      </div>
    </section>

    <section class="py-5 bg-white border-bottom">
      <div class="container">
        <div class="row text-center g-4">
          <div class="col-md-4">
            <div class="p-3 card h-100 border-0 bg-transparent">
              <div class="fs-1 mb-2">🤝</div>
              <h5 class="fw-bold text-dark">Marché Sécurisé</h5>
              <p class="text-dark opacity-75 small">
                RePlay sert d'intermédiaire pour garantir des transactions sans risque.
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="p-3 card h-100 border-0 bg-transparent">
              <div class="fs-1 mb-2">🔄</div>
              <h5 class="fw-bold text-dark">Location Hybride</h5>
              <p class="text-dark opacity-75 small">
                Rentabilisez votre collection ou jouez à petit prix grâce à notre système de location.
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="p-3 card h-100 border-0 bg-transparent">
              <div class="fs-1 mb-2">⭐</div>
              <h5 class="fw-bold text-dark">Communauté de Confiance</h5>
              <p class="text-dark opacity-75 small">
                Système d'évaluations rigoureux pour chaque utilisateur de la plateforme.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
    <footer class="footer mt-auto py-5 text-white">
      <div class="container">
        <div class="row g-4">
          <div class="col-lg-4 col-md-6">
            <h4 class="fw-bold text-warning mb-3">RePlay</h4>
            <p class="opacity-75">
              « Rejoue mieux en donnant une seconde vie aux jeux. »
            </p>
            <p class="small opacity-50">
              La première plateforme hybride dédiée à la durabilité dans l'univers du gaming.
            </p>
          </div>

          <div class="col-lg-2 col-md-6">
            <h5 class="fw-bold mb-3">Explorer</h5>
            <ul class="list-unstyled opacity-75">
              <li class="mb-2">
                <RouterLink to="/achat" class="text-white text-decoration-none hover-warning">Acheter</RouterLink>
              </li>
              <li class="mb-2">
                <RouterLink to="/vendre" class="text-white text-decoration-none hover-warning">Vendre</RouterLink>
              </li>
              <li class="mb-2">
                <RouterLink to="/location" class="text-white text-decoration-none hover-warning">Louer</RouterLink>
              </li>
            </ul>
          </div>

          <div class="col-lg-2 col-md-6">
            <h5 class="fw-bold mb-3">Support</h5>
            <ul class="list-unstyled opacity-75">
              <li class="mb-2"><a href="#" class="text-white text-decoration-none">FAQ</a></li>
              <li class="mb-2"><a href="#" class="text-white text-decoration-none">Système d'évaluations</a></li>
              <li class="mb-2"><a href="#" class="text-white text-decoration-none">Protection Acheteur</a></li>
            </ul>
          </div>

          <div class="col-lg-4 col-md-6">
            <h5 class="fw-bold mb-3">Restez au courant</h5>
            <p class="small opacity-75">Recevez les meilleures offres de jeux usagés avant tout le monde.</p>
            <div class="input-group mb-3 shadow-sm">
              <input type="text" class="form-control border-0" placeholder="Ton courriel" aria-label="Email">
              <button class="btn btn-warning fw-bold" type="button">OK</button>
            </div>
          </div>
        </div>

        <hr class="my-5 opacity-25">

        <div class="d-flex flex-column flex-sm-row justify-content-between align-items-center opacity-50 small">
          <p>&copy; 2024 RePlay Inc. Tous droits réservés.</p>
          <ul class="list-inline mb-0">
            <li class="list-inline-item me-4">Confidentialité</li>
            <li class="list-inline-item">Conditions d'utilisation</li>
          </ul>
        </div>
      </div>
    </footer>
  </main>
</template>

<style scoped>
.hero-section {
  min-height: 85vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  position: relative;
  overflow: hidden;
}

.hero-img {
  height: 450px;
  object-fit: cover;
  border: 4px solid rgba(255, 255, 255, 0.1);
}

.btn-warning {
  background-color: #ffca28;
  border: none;
  color: #0f172a;
}

.btn-warning:hover {
  background-color: #ffb300;
  transform: translateY(-2px);
  transition: all 0.2s;
}

.carousel-item img {
  filter: brightness(0.9);
}

.carousel-control-prev,
.carousel-control-next {
  width: 10%;
}
</style>