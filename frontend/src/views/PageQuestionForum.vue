<template>
    <main class="container">

        <div class="page-header">
            <h1>Forum d'aide</h1>
            <p class="subtitle">Pose tes questions sur tes jeux préférés</p>
        </div>

        <p v-if="erreurs" class="erreur">{{ erreurs }}</p>

        <!-- Liste des jeux -->
        <div v-if="!jeuSelectionne" class="jeux-grid">
            <div v-for="jeu in jeux" :key="jeu.id" class="jeu-card" @click="selectionnerJeu(jeu)">
                <img :src="jeu.image" :alt="jeu.nom" class="jeu-image" />
                <div class="jeu-info">
                    <h3>{{ jeu.nom }}</h3>
                    <span class="question-count">{{ jeu.questions }} question(s)</span>
                </div>
            </div>
        </div>

        <div v-else>
            <button class="btn-back" @click="jeuSelectionne = null">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 12H5" />
                    <path d="m12 19-7-7 7-7" />
                </svg>
                Retour aux jeux
            </button>

            <div class="section-header">
                <h2>{{ jeuSelectionne.nom }}</h2>
                <button class="btn-ask" @click="ouvrirModal">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="12" y1="5" x2="12" y2="19" />
                        <line x1="5" y1="12" x2="19" y2="12" />
                    </svg>
                    Poser une question
                </button>
            </div>

            <div class="table-wrapper">
                <div class="questions-list">
                    <div v-for="question in questions" :key="question.id" class="question-row"
                        @click="voirQuestion(question)">
                        <div class="question-main">
                            <div class="question-status">
                                <div class="status-indicator"></div>
                            </div>
                            <div class="question-content">
                                <h3 class="question-title">{{ question.titre }}</h3>
                                <div class="question-meta">
                                    <span class="meta-item author">Par {{ question.auteur }}</span>
                                    <span class="meta-divider">•</span>
                                    <span class="meta-item date">{{ formatDate(question.dateCreation) }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="question-stats">
                            <div class="stat-box">
                                <span class="stat-value">0</span>
                                <span class="stat-label">Réponses</span>
                            </div>
                        </div>

                        <div class="question-actions" @click.stop>
                            <button v-if="auth.userId === question.idUtilisateur || auth.role === 'admin'"
                                class="btn-icon-delete" @click="supprimerQuestion(question)" title="Supprimer">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path
                                        d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div v-if="questions.length === 0" class="empty-state">
                        <p>Aucune question pour ce jeu. Sois le premier à en poser une !</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal fade" id="questionModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header border-bottom-0">
                        <h5 class="modal-title text-dark fw-bold">Poser une question — {{ jeuSelectionne?.nom }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label class="form-label fw-semibold text-dark">Titre</label>
                            <input v-model="form.titre" type="text"
                                class="form-control text-dark border-secondary-subtle"
                                placeholder="Ex: Comment débloquer le niveau 5 ?" />
                        </div>
                        <div class="form-group mt-3">
                            <label class="form-label fw-semibold text-dark">Description</label>
                            <textarea v-model="form.description" class="form-control text-dark border-secondary-subtle"
                                rows="4" placeholder="Décris ton problème en détail..."></textarea>
                        </div>
                        <p v-if="erreurModal" class="erreur mt-2 mb-0">{{ erreurModal }}</p>
                    </div>
                    <div class="modal-footer border-top-0">
                        <button type="button" class="btn btn-light border" data-bs-dismiss="modal">Annuler</button>
                        <button type="button" class="btn btn-primary px-4" @click="soumettreQuestion"
                            :disabled="chargement">
                            {{ chargement ? 'Envoi...' : 'Envoyer' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
import { Modal } from 'bootstrap'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const notif = useNotifStore()
const router = useRouter()

const erreurs = ref('')
const erreurModal = ref('')
const chargement = ref(false)

const jeux = ref([])
const jeuSelectionne = ref(null)
const questions = ref([])

const form = ref({ titre: '', description: '' })
let modalInstance = null
const toutesLesQuestions = ref([])

onUnmounted(() => notif.clear())

onMounted(async () => {
    modalInstance = new Modal(document.getElementById('questionModal'))

    try {
        const res = await fetch('/api/jeux')
        const data = await res.json()
        if (res.ok) {
            jeux.value = data
        } else {
            erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement des jeux'
        }
    } catch (e) {
        erreurs.value = 'Erreur lors du chargement des jeux'
    }
})

async function selectionnerJeu(jeu) {
    jeuSelectionne.value = jeu
    questions.value = []
    erreurs.value = ''

    try {
        const res = await fetch(`/api/jeux/${jeu.id}/questions`)
        const data = await res.json()
        if (res.ok) {
            questions.value = data
        } else {
            erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement des questions'
        }
    } catch (e) {
        erreurs.value = 'Erreur lors du chargement des questions'
    }
}

function ouvrirModal() {
    form.value = { titre: '', description: '' }
    erreurModal.value = ''
    modalInstance.show()
}

function voirQuestion(question) {
    router.push(`/questions/${question.id}`)
}

async function soumettreQuestion() {
    if (!form.value.titre.trim()) {
        erreurModal.value = 'Le titre est obligatoire.'
        return
    }
    if (!form.value.description.trim()) {
        erreurModal.value = 'La description est obligatoire.'
        return
    }



    chargement.value = true
    erreurModal.value = ''

    try {
        const res = await fetch(`/api/jeux/${jeuSelectionne.value.id}/questions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                titre: form.value.titre,
                description: form.value.description,
                idUtilisateur: auth.userId
            })
        })

        const data = await res.json()

        if (res.ok) {
            questions.value.unshift(data)
            modalInstance.hide()
            // Reset du formulaire
            form.value = { titre: '', description: '' }
        } else {
            // Affiche l'erreur précise renvoyée par Flask
            erreurModal.value = data?.erreurs?.serveur ?? 'Erreur lors de l\'envoi'
        }
    } catch (e) {
        erreurModal.value = 'Erreur lors de l\'envoi'
    } finally {
        chargement.value = false
    }
}

async function supprimerQuestion(question) {
    if (!confirm(`Supprimer la question "${question.titre}" ?`)) return

    try {
        const res = await fetch(`/api/questions/${question.id}`, { method: 'DELETE' })
        if (res.ok) {
            questions.value = questions.value.filter(q => q.id !== question.id)
        } else {
            const data = await res.json()
            erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors de la suppression'
        }
    } catch (e) {
        erreurs.value = 'Erreur lors de la suppression'
    }
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('fr-CA', {
        year: 'numeric', month: 'short', day: 'numeric'
    })
}
</script>

<style scoped>
.questions-list {
    display: flex;
    flex-direction: column;
    gap: 1px;
    background: #e8eaf0;
    border-radius: 14px;
    overflow: hidden;
    border: 1.5px solid #e8eaf0;
}

.question-row {
    display: grid;
    grid-template-columns: 1fr auto auto;
    align-items: center;
    padding: 16px 24px;
    background: #ffffff;
    cursor: pointer;
    transition: background 0.2s;
}

.question-row:hover {
    background: #f8f9ff;
}

.question-status {
    padding-right: 15px;
}

.status-indicator {
    width: 10px;
    height: 10px;
    background: #10b981;
    border-radius: 50%;
}

.question-main {
    display: flex;
    align-items: center;
}

.question-title {
    font-size: 16px;
    font-weight: 600;
    color: #1a1d23;
    margin: 0 0 4px 0;
}

.question-meta {
    font-size: 13px;
    color: #6b7280;
    display: flex;
    gap: 8px;
}

.question-stats {
    display: flex;
    gap: 20px;
    padding: 0 30px;
    border-right: 1px solid #f0f2f6;
    border-left: 1px solid #f0f2f6;
}

.stat-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 60px;
}

.stat-value {
    font-weight: 700;
    color: #1a1d23;
}

.stat-label {
    font-size: 11px;
    text-transform: uppercase;
    color: #9ba3b0;
    letter-spacing: 0.05em;
}

.btn-icon-delete {
    background: transparent;
    border: none;
    color: #9ba3b0;
    padding: 10px;
    cursor: pointer;
    border-radius: 50%;
    transition: all 0.2s;
}

.btn-icon-delete:hover {
    background: #fee2e2;
    color: #ef4444;
}

.btn-icon-delete svg {
    width: 18px;
    height: 18px;
}

.empty-state {
    background: white;
    padding: 40px;
    text-align: center;
    color: #9ba3b0;
}

:deep(.modal-content) {
    background-color: #ffffff !important;
    color: #1a1d23 !important;
}

:deep(.modal-title) {
    color: #1a1d23 !important;
}

:deep(.form-label) {
    color: #1a1d23 !important;
}

:deep(.form-control) {
    background-color: #ffffff !important;
    color: #1a1d23 !important;
    border: 1px solid #dee2e6 !important;
}

:deep(.form-control:focus) {
    color: #1a1d23 !important;
    background-color: #fff !important;
}

:deep(.form-control::placeholder) {
    color: #9ba3b0 !important;
    opacity: 1;
}

:deep(.btn-close) {
    filter: none;
}

.btn-light.border {
    color: #374151 !important;
    background-color: #f9fafb !important;
}

.container {
    padding: 24px;
    font-family: sans-serif;
}

.page-header {
    margin-bottom: 28px;
}

.page-header h1 {
    font-size: 24px;
    font-weight: 700;
    color: #1a1d23;
    margin-bottom: 4px;
}

.subtitle {
    color: #6b7280;
    font-size: 14px;
}

.erreur {
    color: #ef4444;
    margin-bottom: 12px;
    font-size: 14px;
}

.jeux-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
}

.jeu-card {
    background: #fff;
    border: 1.5px solid #e8eaf0;
    border-radius: 14px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.jeu-card:hover {
    border-color: #6366f1;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.12);
    transform: translateY(-2px);
}

.jeu-image {
    width: 100%;
    height: 120px;
    object-fit: cover;
    background: #f0f2f6;
}

.jeu-info {
    padding: 12px 14px;
}

.jeu-info h3 {
    font-size: 14px;
    font-weight: 600;
    color: #1a1d23;
    margin-bottom: 4px;
}

.question-count {
    font-size: 12px;
    color: #9ba3b0;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.section-header h2 {
    font-size: 20px;
    font-weight: 700;
    color: #1a1d23;
}

.btn-back {
    display: flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    border: none;
    color: #6366f1;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    padding: 0;
    margin-bottom: 20px;
    font-family: inherit;
}

.btn-back svg {
    width: 16px;
    height: 16px;
}

.btn-back:hover {
    text-decoration: underline;
}

.btn-ask {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #1a1d23;
    border: none;
    color: #fff;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    padding: 8px 16px;
    border-radius: 50px;
    font-family: inherit;
    transition: background 0.2s;
}

.btn-ask svg {
    width: 14px;
    height: 14px;
}

.btn-ask:hover {
    background: #6366f1;
}

.table-wrapper {
    background: #fff;
    border-radius: 14px;
    border: 1.5px solid #e8eaf0;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.user-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

.user-table thead tr {
    background: #1a1d23;
}

.user-table thead th {
    color: #c9cdd6;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 13px 16px;
    text-align: left;
}

.user-table tbody tr {
    border-bottom: 1px solid #f0f2f6;
}

.user-table tbody tr:last-child {
    border-bottom: none;
}

.user-table tbody tr:hover {
    background: #f8f9ff;
}

.user-table tbody td {
    padding: 12px 16px;
    color: #2c3040;
    vertical-align: middle;
}

.muted {
    color: #6b7280;
}

.actions {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

.btn-voir,
.btn-delete {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 5px 10px;
    border-radius: 7px;
    border: 1.5px solid transparent;
    background: transparent;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    font-family: inherit;
}

.btn-voir svg,
.btn-delete svg {
    width: 13px;
    height: 13px;
    flex-shrink: 0;
}

.btn-voir {
    color: #0ea5e9;
}

.btn-voir:hover {
    background: #e0f2fe;
    border-color: #7dd3fc;
}

.btn-delete {
    color: #ef4444;
}

.btn-delete:hover {
    background: #fee2e2;
    border-color: #fca5a5;
}

.empty {
    text-align: center;
    padding: 40px;
    color: #9ba3b0;
    font-size: 14px;
}

:deep(.modal-content) {
    background-color: #fff;
}
</style>