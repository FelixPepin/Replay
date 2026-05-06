<template>
    <main class="container">
        <div v-if="auth.role === 'admin'">

            <p v-if="erreurs" class="erreur">{{ erreurs }}</p>

            <div class="table-wrapper">
                <table class="user-table">
                    <thead>
                        <tr>
                            <th>Id</th>
                            <th>Nom Utilisateur</th>
                            <th>Courriel</th>
                            <th>Rôle</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in users" :key="user.id">
                            <td class="muted">{{ user.id }}</td>
                            <td>{{ user.nomUtilisateur }}</td>
                            <td class="muted">{{ user.courriel }}</td>
                            <td>
                                <span class="badge" :class="user.role">{{ user.role }}</span>
                            </td>
                            <td>
                                <div class="actions">
                                    <button class="btn-edit" @click="ouvrirModal(user)">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                                        </svg>
                                    </button>
                                    <button v-if="user.role !== 'admin' && user.id !== auth.id" class="btn-delete"
                                        @click="supprimerUser(user)">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <polyline points="3 6 5 6 21 6" />
                                            <path d="M19 6l-1 14H6L5 6" />
                                            <path d="M10 11v6" />
                                            <path d="M14 11v6" />
                                            <path d="M9 6V4h6v2" />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                        <tr v-if="users.length === 0 && !erreurs">
                            <td colspan="5" class="empty">Aucun utilisateur trouvé.</td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div>
        <div class="modal fade" id="editModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Modifier le rôle — {{ userSelectionne?.nomUtilisateur }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <label class="form-label fw-semibold">Rôle</label>
                        <select v-model="nouveauRole" class="form-select">
                            <option value="admin">Admin</option>
                            <option value="vendeur">Vendeur</option>
                            <option value="client">Client</option>
                        </select>
                        <p v-if="erreurModal" class="erreur mt-2 mb-0">{{ erreurModal }}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                        <button type="button" class="btn btn-primary" @click="sauvegarderRole" :disabled="chargement">
                            {{ chargement ? 'Sauvegarde...' : 'Sauvegarder' }}
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
const users = ref([])
const erreurs = ref('')

const userSelectionne = ref(null)
const nouveauRole = ref('')
const erreurModal = ref('')
const chargement = ref(false)
let modalInstance = null

onMounted(async () => {
    modalInstance = new Modal(document.getElementById('editModal'))

    try {
        const res = await fetch('/api/users')
        const data = await res.json()
        if (res.ok) {
            users.value = data
        } else {
            erreurs.value = data?.erreurs?.serveur ?? 'Erreur lors du chargement'
        }
    } catch (e) {
        erreurs.value = 'Erreur lors du chargement'
    }
})

function ouvrirModal(user) {
    userSelectionne.value = user
    nouveauRole.value = user.role
    erreurModal.value = ''
    modalInstance.show()
}

async function sauvegarderRole() {

    if (userSelectionne.value.id === auth.id) {
        erreurModal.value = "Vous ne pouvez pas changer votre propre rôle"
        return
    }

    if (userSelectionne.value.role === 'admin') {
        erreurModal.value = "Vous ne pouvez pas modifier le rôle d'un admin"
        return
    }
    if (nouveauRole.value === userSelectionne.value.role) {
        modalInstance.hide()
        return
    }

    chargement.value = true
    erreurModal.value = ''

    try {
        const res = await fetch(`/api/users/${userSelectionne.value.id}/role`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role: nouveauRole.value })
        })
        const data = await res.json()

        if (res.ok) {

            userSelectionne.value.role = nouveauRole.value
            modalInstance.hide()
        } else {
            erreurModal.value = data?.erreurs?.serveur ?? 'Erreur lors de la sauvegarde'
        }
    } catch (e) {
        erreurModal.value = 'Erreur lors de la sauvegarde'
    } finally {
        chargement.value = false
    }
}

async function supprimerUser(user) {
    if (user.id === auth.id) return
    if (user.role === 'admin') return
    if (!confirm(`Supprimer l'utilisateur "${user.nomUtilisateur}" ?`)) return

    try {
        const res = await fetch(`/api/users/${user.id}`, { method: 'DELETE' })
        if (res.ok) {
            users.value = users.value.filter(u => u.id !== user.id)
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
.container {
    padding: 24px;
    font-family: sans-serif;
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

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
    text-transform: capitalize;
}

.badge.admin {
    background: #ede9fe;
    color: #6d28d9;
}

.badge.vendeur {
    background: #dcfce7;
    color: #16a34a;
}

.badge.client {
    background: #dbeafe;
    color: #1d4ed8;
}

.actions {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

.btn-edit,
.btn-copy,
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

.btn-edit svg,
.btn-copy svg,
.btn-delete svg {
    width: 13px;
    height: 13px;
    flex-shrink: 0;
}

.btn-edit {
    color: #6366f1;
}

.btn-edit:hover {
    background: #ede9fe;
    border-color: #c4b5fd;
}

.btn-copy {
    color: #0ea5e9;
}

.btn-copy:hover {
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
    background-color: #1a1d23;
}
</style>