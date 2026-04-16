<script setup>
import { ref, computed } from 'vue'
import { quizzes } from '@/data/quizzes.js'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const phase = ref('selection') // 'selection' | 'quiz' | 'resultats'
const quizActif = ref(null)
const questionIndex = ref(0)
const score = ref(0)
const reponseChoisie = ref(null)
const enAttente = ref(false)

const questionActuelle = computed(() =>
  quizActif.value?.questions[questionIndex.value]
)

const progression = computed(() =>
  quizActif.value
    ? Math.round((questionIndex.value / quizActif.value.questions.length) * 100)
    : 0
)

function commencer(quiz) {
  quizActif.value = quiz
  questionIndex.value = 0
  score.value = 0
  reponseChoisie.value = null
  enAttente.value = false
  phase.value = 'quiz'
}

function repondre(index) {
  if (enAttente.value || reponseChoisie.value !== null) return
  reponseChoisie.value = index
  enAttente.value = true
  if (index === questionActuelle.value.reponse) score.value++

  setTimeout(async () => {
    reponseChoisie.value = null
    enAttente.value = false
    if (questionIndex.value + 1 < quizActif.value.questions.length) {
      questionIndex.value++
    } else {
      phase.value = 'resultats'
      if (auth.estConnecte && score.value > 9) {
        try {
          const res = await fetch(`/api/users/${auth.userId}/promouvoir-coach`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ jeuCoachId: quizActif.value.id })
          })
          if (res.ok) {
            const data = await res.json()
            auth.connecter(data.token)
          }
        } catch {
          // Échec silencieux, le rôle sera mis à jour à la prochaine connexion
        }
      }
    }
  }, 1100)
}

function classBouton(index) {
  if (reponseChoisie.value === null) return 'btn-outline-secondary'
  if (index === questionActuelle.value.reponse) return 'btn-success'
  if (index === reponseChoisie.value) return 'btn-danger'
  return 'btn-outline-secondary'
}

function messageResultat() {
  const n = quizActif.value.questions.length
  const r = score.value / n
  if (r === 1) return 'Score parfait ! Vous êtes un vrai expert !'
  if (r >= 0.8) return 'Excellent ! Vous connaissez très bien ce jeu !'
  if (r >= 0.6) return 'Pas mal ! Continuez comme ça !'
  if (r >= 0.4) return 'Quelques révisions s\'imposent...'
  return 'Retournez jouer un peu avant de refaire ce quiz !'
}

function emojiResultat() {
  const n = quizActif.value.questions.length
  const r = score.value / n
  if (r === 1) return '🏆'
  if (r >= 0.6) return '⭐'
  return '📚'
}

function rejouer() {
  commencer(quizActif.value)
}

function revenirSelection() {
  phase.value = 'selection'
}

const lettres = ['A', 'B', 'C', 'D']
</script>

<template>
  <div class="container py-5">
    <Transition name="phase" mode="out-in">

      <!-- ==================== SÉLECTION ==================== -->
      <div v-if="phase === 'selection'" key="selection">
        <div class="text-center mb-5">
          <h1 class="fw-bold display-5">Quiz Jeux Vidéo</h1>
          <p class="text-muted fs-5">Choisissez un quiz et testez vos connaissances !</p>
        </div>
        <div class="row justify-content-center g-4">
          <div
            v-for="quiz in quizzes"
            :key="quiz.id"
            class="col-lg-4 col-md-5 col-sm-8"
          >
            <div class="card bg-dark text-white h-100 border-0 shadow quiz-card">
              <div class="card-body d-flex flex-column p-4 text-center">
                <div class="quiz-emoji mb-3">{{ quiz.emoji }}</div>
                <h3 class="card-title fw-bold mb-2">{{ quiz.nom }}</h3>
                <p class="card-text text-secondary flex-grow-1 mb-3">{{ quiz.description }}</p>
                <span class="badge bg-warning text-dark mb-4 align-self-center px-3 py-2">
                  {{ quiz.questions.length }} questions
                </span>
                <button @click="commencer(quiz)" class="btn btn-warning fw-bold text-uppercase">
                  Commencer
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ==================== QUIZ ==================== -->
      <div v-else-if="phase === 'quiz'" key="quiz" class="quiz-container mx-auto">
        <!-- En-tête -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h5 class="fw-bold mb-0">
            {{ quizActif.emoji }} {{ quizActif.nom }}
          </h5>
          <button @click="revenirSelection" class="btn btn-outline-secondary btn-sm">
            Abandonner
          </button>
        </div>

        <!-- Progression -->
        <div class="d-flex justify-content-between text-muted small mb-1">
          <span>Question {{ questionIndex + 1 }} / {{ quizActif.questions.length }}</span>
          <span>{{ score }} bonne(s) réponse(s)</span>
        </div>
        <div class="progress mb-4" style="height: 8px;">
          <div
            class="progress-bar bg-warning"
            role="progressbar"
            :style="{ width: progression + '%' }"
          ></div>
        </div>

        <!-- Question avec transition -->
        <Transition name="question" mode="out-in">
          <div :key="questionIndex" class="card bg-dark text-white border-0 shadow">
            <div class="card-body p-4 p-md-5">
              <p class="fs-5 fw-bold mb-4 text-center lh-base">
                {{ questionActuelle.question }}
              </p>
              <div class="d-grid gap-3">
                <button
                  v-for="(choix, i) in questionActuelle.choix"
                  :key="i"
                  @click="repondre(i)"
                  :class="['btn', 'text-start', 'py-3', 'px-4', 'reponse-btn', classBouton(i)]"
                  :disabled="enAttente"
                >
                  <span class="badge bg-secondary me-2 lettre-badge">{{ lettres[i] }}</span>
                  {{ choix }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- ==================== RÉSULTATS ==================== -->
      <div v-else key="resultats" class="quiz-container mx-auto">
        <div class="card bg-dark text-white border-0 shadow text-center">
          <div class="card-body p-5">
            <div class="resultat-emoji mb-3">{{ emojiResultat() }}</div>
            <h2 class="fw-bold mb-1">{{ quizActif.nom }}</h2>
            <p class="text-muted mb-4">Quiz terminé !</p>
            <div class="score-display mb-2">
              <span class="text-warning fw-bold">{{ score }}</span>
              <span class="text-muted"> / {{ quizActif.questions.length }}</span>
            </div>
            <p class="fs-5 mb-5">{{ messageResultat() }}</p>
            <div class="d-flex flex-wrap gap-3 justify-content-center">
              <button @click="rejouer" class="btn btn-warning fw-bold px-5">
                Rejouer
              </button>
              <button @click="revenirSelection" class="btn btn-outline-light px-5">
                Choisir un autre quiz
              </button>
            </div>
          </div>
        </div>
      </div>

    </Transition>
  </div>
</template>

<style scoped>
/* ---- Conteneur quiz (questions + résultats) ---- */
.quiz-container {
  max-width: 660px;
}

/* ---- Carte sélection ---- */
.quiz-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.quiz-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45) !important;
}
.quiz-emoji {
  font-size: 3.5rem;
  line-height: 1;
}

/* ---- Boutons de réponse ---- */
.reponse-btn {
  transition: background-color 0.25s, border-color 0.25s, color 0.25s;
  font-size: 1rem;
}
.reponse-btn.btn-outline-secondary {
  color: #ced4da;
  border-color: #495057;
}
.reponse-btn.btn-outline-secondary:hover:not(:disabled) {
  background-color: #495057;
  color: #fff;
  border-color: #6c757d;
}
.reponse-btn.btn-success {
  background-color: #198754 !important;
  border-color: #198754 !important;
  color: #fff !important;
}
.reponse-btn.btn-danger {
  background-color: #dc3545 !important;
  border-color: #dc3545 !important;
  color: #fff !important;
}
.reponse-btn:disabled {
  opacity: 0.8;
  cursor: not-allowed;
}
.lettre-badge {
  min-width: 1.5rem;
  text-align: center;
}

/* ---- Score résultats ---- */
.resultat-emoji {
  font-size: 4rem;
  line-height: 1;
}
.score-display {
  font-size: 3.5rem;
  line-height: 1;
}

/* ---- Transitions de phase (sélection <-> quiz <-> résultats) ---- */
.phase-enter-active,
.phase-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.phase-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.phase-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* ---- Transitions de question ---- */
.question-enter-active,
.question-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.question-enter-from {
  opacity: 0;
  transform: translateX(28px);
}
.question-leave-to {
  opacity: 0;
  transform: translateX(-28px);
}
</style>
