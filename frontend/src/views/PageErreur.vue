<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const erreurs = {
  '400': {
    titre: 'Requête invalide',
    message: "Ta manette envoie des commandes que le serveur ne reconnaît pas. Vérifie ta requête et réessaie.",
    icon: 'fi-br-joystick',
    couleur: '#f5c33b',
    hint: 'Bad Request',
  },
  '401': {
    titre: 'Non authentifié',
    message: "Il faut s'identifier avant d'entrer dans cette zone. Connecte-toi pour continuer l'aventure.",
    icon: 'fi-br-lock',
    couleur: '#7e9eff',
    hint: 'Unauthorized',
    boutonLogin: true,
  },
  '403': {
    titre: 'Accès interdit',
    message: "Tu n'as pas les permissions nécessaires. Cette zone est réservée aux joueurs de haut niveau.",
    icon: 'fi-br-shield-check',
    couleur: '#fb923c',
    hint: 'Forbidden',
  },
  '404': {
    titre: 'Page introuvable',
    message: "Cette page s'est volatilisée comme un loot rare. Elle n'existe plus — ou n'a jamais existé.",
    icon: 'fi-br-search',
    couleur: '#f5c33b',
    hint: 'Not Found',
  },
  '405': {
    titre: 'Méthode non autorisée',
    message: "Cette touche de ta manette est désactivée. L'action que tu tentes n'est pas permise ici.",
    icon: 'fi-br-cross-circle',
    couleur: '#9aa0af',
    hint: 'Method Not Allowed',
  },
  '500': {
    titre: 'Erreur serveur',
    message: "Game Over côté serveur. Une erreur critique vient de survenir. Nos ingénieurs sont sur le coup.",
    icon: 'fi-br-bug',
    couleur: '#e07070',
    hint: 'Internal Server Error',
  },
}

const code = computed(() => String(route.params.code || '404'))
const erreur = computed(() => erreurs[code.value] || erreurs['404'])
const codeAffiche = computed(() => (erreurs[code.value] ? code.value : '404'))
</script>

<template>
  <main class="erreur-page d-flex align-items-center justify-content-center">
    <div class="dot-grid"></div>

    <div class="erreur-content text-center">
      <div class="erreur-hint" :style="{ color: erreur.couleur }">{{ erreur.hint }}</div>

      <div class="erreur-code" :style="{ color: erreur.couleur }">
        {{ codeAffiche }}
      </div>

      <i :class="['fi', erreur.icon, 'erreur-icon']" :style="{ color: erreur.couleur }"></i>

      <h1 class="erreur-titre">{{ erreur.titre }}</h1>
      <p class="erreur-message">{{ erreur.message }}</p>

      <div class="d-flex gap-3 justify-content-center flex-wrap mt-4">
        <button @click="router.push('/')" class="btn-erreur-retour">
          <i class="fi fi-br-home"></i>
          Retour à l'accueil
        </button>
        <button
          v-if="erreur.boutonLogin"
          @click="router.push('/login')"
          class="btn-erreur-login"
        >
          <i class="fi fi-br-user"></i>
          Se connecter
        </button>
      </div>

      <p class="erreur-footer">RePlay · © 2026</p>
    </div>
  </main>
</template>

<style scoped>
.erreur-page {
  min-height: 85vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  position: relative;
  overflow: hidden;
  padding: 40px 20px;
}

.dot-grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
  z-index: 0;
}

.erreur-content {
  position: relative;
  z-index: 1;
  max-width: 560px;
}

.erreur-hint {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  opacity: 0.65;
  margin-bottom: 4px;
}

.erreur-code {
  font-size: clamp(96px, 20vw, 160px);
  font-weight: 800;
  line-height: 1;
  letter-spacing: -4px;
  animation: glitch 6s infinite;
}

@keyframes glitch {
  0%,
  86%,
  100% {
    text-shadow: none;
    transform: none;
  }
  87% {
    text-shadow: 4px 0 #7e9eff, -4px 0 #e07070;
    transform: translateX(3px);
  }
  89% {
    text-shadow: -4px 0 #7e9eff, 4px 0 #e07070;
    transform: translateX(-3px);
  }
  91% {
    text-shadow: 2px 0 #f5c33b, -2px 0 #7e9eff;
    transform: translateX(2px);
  }
  93% {
    text-shadow: none;
    transform: none;
  }
}

.erreur-icon {
  font-size: 2.2rem;
  display: block;
  margin: 10px auto 22px;
}

.erreur-titre {
  font-size: 1.55rem;
  font-weight: 700;
  color: #e0e4ed;
  margin-bottom: 12px;
}

.erreur-message {
  font-size: 15px;
  color: #9aa0af;
  line-height: 1.7;
  max-width: 440px;
  margin: 0 auto;
}

.btn-erreur-retour {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border-radius: 999px;
  border: none;
  background: #f5c33b;
  color: #1a1f2e;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, transform 0.15s;
}

.btn-erreur-retour:hover {
  background: #e6b635;
  transform: translateY(-2px);
}

.btn-erreur-login {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border-radius: 999px;
  border: 0.5px solid rgba(93, 130, 255, 0.45);
  background: rgba(93, 130, 255, 0.08);
  color: #7e9eff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, transform 0.15s;
}

.btn-erreur-login:hover {
  background: rgba(93, 130, 255, 0.18);
  transform: translateY(-2px);
}

.erreur-footer {
  margin-top: 52px;
  font-size: 11px;
  color: #4e5568;
}
</style>
