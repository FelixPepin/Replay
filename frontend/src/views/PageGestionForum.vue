<template>
    <main class="container">
        <div v-if="auth.role === 'admin'">

            <div class="section-header">
                <h1 class="page-title">Gestion des jeux</h1>
                <button class="btn-ask" @click="ouvrirModal">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="12" y1="5" x2="12" y2="19" />
                        <line x1="5" y1="12" x2="19" y2="12" />
                    </svg>
                    Ajouter un jeu
                </button>
            </div>

            <p v-if="erreurs" class="erreur">{{ erreurs }}</p>

            <div class="table-wrapper">
                <table class="user-table">
                    <thead>
                        <tr>
                            <th>Id</th>
                            <th>Nom</th>
                            <th>Image</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="jeu in jeux" :key="jeu.id">
                            <td class="muted">{{ jeu.id }}</td>
                            <td>{{ jeu.nom }}</td>
                            <td>
                                <img v-if="jeu.image" :src="jeu.image" :alt="jeu.nom" class="jeu-thumb" />
                                <span v-else class="muted">—</span>
                            </td>
                            <td>
                                <div class="actions">
                                    <button class="btn-delete" @click="supprimerJeu(jeu)">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <circle cx="12" cy="12" r="10" />
                                            <line x1="15" y1="9" x2="9" y2="15" />
                                            <line x1="9" y1="9" x2="15" y2="15" />
                                        </svg>
                                        Supprimer
                                    </button>
                                </div>
                            </td>
                        </tr>
                        <tr v-if="jeux.length === 0 && !erreurs">
                            <td colspan="4" class="empty">Aucun jeu ajouté.</td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div>

        <!-- Modal ajout -->
        <div class="modal fade" id="jeuModal" ref="modalElement" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header border-bottom-0">
                        <h5 class="modal-title text-dark fw-bold">Ajouter un jeu</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label class="form-label fw-semibold text-dark">Nom du jeu</label>
                            <input v-model="form.nom" type="text" class="form-control text-dark border-secondary-subtle"
                                placeholder="Ex: Minecraft" />
                        </div>
                        <div class="form-group mt-3">
                            <label class="form-label fw-semibold text-dark">Image du jeu <span
                                    class="text-muted small">(optionnel)</span></label>

                            <input type="file" ref="fileInput" @change="gererFichier"
                                accept="image/png, image/jpeg, image/webp" />

                            <div class="d-flex align-items-center gap-3">
                                <button type="button" class="btn btn-outline-secondary btn-sm"
                                    @click="$refs.fileInput.click()">
                                    Choisir une image...
                                </button>
                                <span v-if="form.image" class="text-muted small text-truncate"
                                    style="max-width: 200px;">
                                    {{ form.image.name }}
                                </span>
                                <span v-else class="text-muted small">Aucun fichier</span>
                            </div>

                            <div v-if="imagePreview" class="mt-3 preview-container border rounded p-2 text-center">
                                <img :src="imagePreview" class="img-thumbnail preview-image" />
                                <button type="button"
                                    class="btn-close btn-close-white position-absolute top-0 end-0 m-2"
                                    @click="annulerImage" aria-label="Supprimer l'image"></button>
                            </div>
                        </div>
                        <p v-if="erreurModal" class="erreur mt-2 mb-0">{{ erreurModal }}</p>
                    </div>
                    <div class="modal-footer border-top-0">
                        <button type="button" class="btn btn-light border" data-bs-dismiss="modal">Annuler</button>
                        <button type="button" class="btn btn-primary px-4" @click="soumettreJeu" :disabled="chargement">
                            {{ chargement ? 'Ajout...' : 'Ajouter' }}
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

const auth = useAuthStore()
const notif = useNotifStore()

const jeux = ref([])
const erreurs = ref('')
const erreurModal = ref('')
const chargement = ref(false)
const form = ref({ nom: '', image: null })
let modalInstance = null
const modalElement = ref(null)
const imagePreview = ref(null)
const fileInput = ref(null)
onUnmounted(() => notif.clear())

onMounted(async () => {
    if (modalElement.value) {
        modalInstance = new Modal(modalElement.value)
    }
    try {
        const res = await fetch('/api/jeux')
        const data = await res.json()
        if (res.ok) {
            jeux.value = data
        } else {
            erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
        }
    } catch (e) {
        erreurs.value = 'Erreur lors du chargement'
    }
})

function ouvrirModal() {
    form.value = { nom: '', image: null }
    imagePreview.value = null
    erreurModal.value = ''
    if (fileInput.value) fileInput.value.value = ''
    modalInstance.show()
}

function gererFichier(event) {
    const fichier = event.target.files[0]
    if (!fichier) return

    if (!fichier.type.startsWith('image/')) {
        erreurModal.value = 'Le fichier doit être une image (PNG, JPG, WebP).'
        annulerImage()
        return
    }

    form.value.image = fichier

    const reader = new FileReader()
    reader.onload = (e) => {
        imagePreview.value = e.target.result
    }
    reader.readAsDataURL(fichier)
}

function annulerImage() {
    form.value.image = null
    imagePreview.value = null
    if (fileInput.value) fileInput.value.value = ''
}

async function soumettreJeu() {
    if (!form.value.nom.trim()) {
        erreurModal.value = 'Le nom est obligatoire.'
        return
    }

    chargement.value = true
    erreurModal.value = ''

    try {
        const formData = new FormData()
        formData.append('nom', form.value.nom)

        if (form.value.image) {
            formData.append('image', form.value.image)
        }

        const res = await fetch('/api/jeux', {
            method: 'POST',
            body: formData
        })

        const data = await res.json()

        if (res.ok) {
            jeux.value.unshift(data)
            modalInstance.hide()
        } else {
            erreurModal.value = data?.erreurs?.serveur ?? 'Erreur lors de l\'ajout'
        }
    } catch (e) {
        erreurModal.value = 'Erreur lors de l\'ajout (problème réseau ou serveur)'
    } finally {
        chargement.value = false
    }
}
async function supprimerJeu(jeu) {
    if (!confirm(`Supprimer "${jeu.nom}" ? Toutes ses questions seront supprimées.`)) return

    try {
        const res = await fetch(`/api/jeux/${jeu.id}`, { method: 'DELETE' })
        if (res.ok) {
            jeux.value = jeux.value.filter(j => j.id !== jeu.id)
        } else {
            const data = await res.json()
            erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors de la suppression'
        }
    } catch (e) {
        erreurs.value = 'Erreur lors de la suppression'
    }
}
</script>

<style scoped>
:deep(.modal-content) {
    background-color: #ffffff !important;
    color: #1a1d23 !important;
}

:deep(.form-control) {
    background-color: #ffffff !important;
    color: #1a1d23 !important;
    border: 1px solid #dee2e6 !important;
}

:deep(.form-control::placeholder) {
    color: #9ba3b0 !important;
    opacity: 1;
}

:deep(.form-label) {
    color: #1a1d23 !important;
}

:deep(.btn-close) {
    filter: none;
}

.container {
    padding: 24px;
    font-family: sans-serif;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}

.page-title {
    font-size: 22px;
    font-weight: 700;
    color: #1a1d23;
}

.erreur {
    color: #ef4444;
    margin-bottom: 12px;
    font-size: 14px;
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

.jeu-thumb {
    width: 48px;
    height: 32px;
    object-fit: cover;
    border-radius: 6px;
}

.actions {
    display: flex;
    gap: 6px;
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
    color: #ef4444;
}

.btn-delete svg {
    width: 13px;
    height: 13px;
    flex-shrink: 0;
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