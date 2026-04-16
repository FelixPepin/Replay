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
            <div class="section-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                    class="icon-title">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
                <h3>Réponses des coachs</h3>
            </div>

            <div v-if="reponses.length > 0" class="responses-list">
                <div v-for="rep in reponses" :key="rep.id" class="response-card">
                    <div class="response-header">
                        <span class="coach-name">Coach {{ rep.auteur_nom }}</span> |
                        <span class="date">{{ formatDate(rep.dateCreation) }}</span>
                    </div>
                    <div class="response-body">
                        {{ rep.contenu }}
                    </div>
                </div>
            </div>
            <div v-else class="empty-state">
                <p>Aucun coach n'a encore répondu à cette question.</p>
            </div>

            <div v-if="peutRepondre" class="reply-container">
                <h4>Apporter une réponse d'expert</h4>
                <textarea v-model="nouvelleReponse" placeholder="Écrivez votre solution ici..."
                    :disabled="chargement"></textarea>
                <div class="reply-actions">
                    <button @click="envoyerReponse" class="btn-send" :disabled="chargement || !nouvelleReponse.trim()">
                        <span v-if="!chargement">Publier la réponse</span>
                        <span v-else>Publication en cours...</span>
                    </button>
                </div>
            </div>

            <div v-else class="coach-only-notice">
                <p>🔒 Seuls les coachs assignés à ce jeu peuvent répondre pour garantir la fiabilité des informations.
                </p>
            </div>
        </section>
    </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()

const question = ref(null)
const reponses = ref([])
const nouvelleReponse = ref('')
const chargement = ref(false)

const peutRepondre = computed(() => {
    if (!auth.estConnecte || auth.role !== 'coach') return false
    const idJeuQuestion = question.value?.idJeu
    return auth.utilisateur?.mes_jeux_ids?.includes(idJeuQuestion)
})
onMounted(async () => {
    await chargerDonnees()
})

async function chargerDonnees() {
    try {
        const resQ = await fetch(`/api/questions/${route.params.id}`)
        if (resQ.ok) question.value = await resQ.json()

        const resR = await fetch(`/api/questions/${route.params.id}/reponses`)
        if (resR.ok) reponses.value = await resR.json()
    } catch (e) {
        console.error("Erreur chargement", e)
    }
}

async function envoyerReponse() {
    if (!nouvelleReponse.value.trim()) return
    chargement.value = true

    try {
        const res = await fetch(`/api/questions/${route.params.id}/reponses`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contenu: nouvelleReponse.value,
                idUtilisateur: auth.userId
            })
        })

        if (res.ok) {
            nouvelleReponse.value = ''
            await chargerDonnees()
        }
    } finally {
        chargement.value = false
    }
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('fr-CA', {
        year: 'numeric', month: 'long', day: 'numeric'
    })
}
</script>

<style scoped>
.responses-section {
    margin-top: 48px;
    border-top: 1px solid #334155;
    padding-top: 32px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}

.icon-title {
    color: #6366f1;
}

.response-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    border-left: 4px solid #10b981;
}

.coach-name {
    color: #10b981;
    font-weight: 700;
    font-size: 0.9rem;
}

.response-body {
    color: #f8fafc;
    margin-top: 10px;
    line-height: 1.6;
}

.reply-container {
    background: #f8fafc;
    border-radius: 12px;
    padding: 24px;
    margin-top: 40px;
}

.reply-container h4 {
    color: #1e293b;
    margin-bottom: 16px;
}

.reply-container textarea {
    width: 100%;
    min-height: 120px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 12px;
    background: white;
    color: #1e293b;
}

.btn-send {
    background: #6366f1;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 12px;
    transition: background 0.2s;
}

.btn-send:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.coach-only-notice {
    margin-top: 32px;
    text-align: center;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    color: #94a3b8;
    font-size: 0.9rem;
}

.container {
    padding: 24px;
    min-height: 100vh;
}

.btn-back {
    display: flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    border: none;
    color: #6366f1;
    font-weight: 600;
    cursor: pointer;
    margin-bottom: 20px;
    padding: 0;
}

.question-header h1 {
    color: #f8fafc;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.meta {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-bottom: 24px;
}

.content-card {
    background-color: #ffffff !important;
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.content-card p {
    color: #1e293b !important;
    font-size: 1.1rem;
    line-height: 1.7;
    margin: 0;
    white-space: pre-wrap;
}

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