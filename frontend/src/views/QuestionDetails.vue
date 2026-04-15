<template>
    <main class="container" v-if="question">
        <button class="btn-back" @click="$router.back()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5" />
                <path d="m12 19-7-7 7-7" />
            </svg>
            Retour
        </button>

        <div class="question-header">
            <h1>{{ question.titre }}</h1>
            <div class="meta text-black">
                Par <strong>{{ question.auteur }}</strong> le {{ formatDate(question.dateCreation) }}
            </div>
        </div>

        <div class="content-card">
            <p>{{ question.description }}</p>
        </div>

        <section class="responses-section">
            <h3>Réponses</h3>
            <p class="empty">Aucune réponse pour le moment.</p>
        </section>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const question = ref(null)

onMounted(async () => {
    try {
        // Vous aurez besoin d'une route API : GET /api/questions/<id>
        const res = await fetch(`/api/questions/${route.params.id}`)
        if (res.ok) {
            question.value = await res.json()
        }
    } catch (e) {
        console.error("Erreur chargement question", e)
    }
})

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('fr-CA', {
        year: 'numeric', month: 'long', day: 'numeric'
    })
}
</script>

<style scoped>
/* Conteneur principal */
.container {
    padding: 24px;
    min-height: 100vh;
}

/* Bouton retour */
.btn-back {
    display: flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    border: none;
    color: #6366f1;
    /* Indigo */
    font-weight: 600;
    cursor: pointer;
    margin-bottom: 20px;
    padding: 0;
}

/* Titre de la question (en dehors de la carte) */
.question-header h1 {
    color: #f8fafc;
    /* Blanc cassé pour le titre sur fond sombre */
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.meta {
    color: #94a3b8;
    /* Gris bleuté clair */
    font-size: 0.95rem;
    margin-bottom: 24px;
}

/* LA CARTE DE CONTENU (Le problème est ici) */
.content-card {
    background-color: #ffffff !important;
    /* Fond blanc pur */
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.content-card p {
    color: #1e293b !important;
    /* Gris très foncé (presque noir) pour le contraste */
    font-size: 1.1rem;
    line-height: 1.7;
    margin: 0;
    white-space: pre-wrap;
    /* Garde les retours à la ligne */
}

/* Section Réponses */
.responses-section {
    margin-top: 40px;
}

.responses-section h3 {
    color: #f8fafc;
    margin-bottom: 20px;
    font-weight: 600;
}

.empty {
    text-align: center;
    padding: 40px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: #94a3b8;
}
</style>