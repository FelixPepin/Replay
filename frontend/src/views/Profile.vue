<template>
    <main class="container">

        <div class="page-header">
            <h1 class="page-title">Mon profil</h1>
        </div>

        <div v-if="erreurs.general" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ erreurs.general }}
            <button type="button" class="btn-close" @click="erreurs.general = ''"></button>
        </div>

        <div v-if="succes" class="alert alert-success alert-dismissible fade show" role="alert">
            {{ succes }}
            <button type="button" class="btn-close" @click="succes = ''"></button>
        </div>

        <div class="table-wrapper">
            <div class="profil-section">

                <div class="profil-info">
                    <div class="avatar-cercle">{{ auth.initiales }}</div>
                    <div>
                        <div class="profil-nom">{{ auth.nom }}</div>
                        <div class="profil-role">{{ auth.role }}</div>
                    </div>
                </div>

                <hr class="divider" />

                <div class="form-bloc">
                    <h2 class="form-titre">Nom d'utilisateur</h2>
                    <div class="form-group">
                        <label>Nouveau nom d'utilisateur</label>
                        <input v-model="formNom.nomUtilisateur" type="text" class="form-control"
                            placeholder="Nouveau nom d'utilisateur" />
                        <p v-if="erreurs.nomUtilisateur" class="erreur-champ">{{ erreurs.nomUtilisateur }}</p>
                    </div>
                    <button class="btn-save" @click="modifierNom" :disabled="chargementNom">
                        {{ chargementNom ? 'Sauvegarde...' : 'Modifier le nom' }}
                    </button>
                </div>

                <hr class="divider" />

                <div class="form-bloc">
                    <h2 class="form-titre">Mot de passe</h2>
                    <div class="form-group">
                        <label>Mot de passe actuel</label>
                        <input v-model="formMdp.actuel" type="password" class="form-control" placeholder="••••••••" />
                        <p v-if="erreurs.actuel" class="erreur-champ">{{ erreurs.actuel }}</p>
                    </div>
                    <div class="form-group">
                        <label>Nouveau mot de passe</label>
                        <input v-model="formMdp.nouveau" type="password" class="form-control" placeholder="••••••••" />
                        <p v-if="erreurs.nouveau" class="erreur-champ">{{ erreurs.nouveau }}</p>
                    </div>
                    <div class="form-group">
                        <label>Confirmer le nouveau mot de passe</label>
                        <input v-model="formMdp.confirmation" type="password" class="form-control"
                            placeholder="••••••••" />
                        <p v-if="erreurs.confirmation" class="erreur-champ">{{ erreurs.confirmation }}</p>
                    </div>
                    <button class="btn-save" @click="modifierMdp" :disabled="chargementMdp">
                        {{ chargementMdp ? 'Sauvegarde...' : 'Modifier le mot de passe' }}
                    </button>
                </div>

                <hr class="divider" />

                <div class="form-bloc danger-zone">
                    <h2 class="form-titre danger-titre">Supprimer mon compte</h2>
                    <p class="danger-desc">Cette action est irréversible. Toutes tes données seront supprimées.</p>
                    <button class="btn-danger" @click="ouvrirModalSuppression">
                        Supprimer mon compte
                    </button>
                </div>

            </div>
        </div>

        <div class="modal fade" id="suppressionModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Confirmer la suppression</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Entrez votre mot de passe pour confirmer la suppression de votre compte.</p>
                        <input v-model="motDePasseConfirmation" type="password" class="form-control"
                            placeholder="••••••••" />
                        <p v-if="erreurs.suppression" class="erreur-champ mt-2">{{ erreurs.suppression }}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                        <button type="button" class="btn btn-danger" @click="supprimerCompte"
                            :disabled="chargementSuppression">
                            {{ chargementSuppression ? 'Suppression...' : 'Confirmer la suppression' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

    </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotifStore } from '@/stores/notif'
import { useRouter } from 'vue-router'
import { Modal } from 'bootstrap'

const auth = useAuthStore()
const notif = useNotifStore()
const router = useRouter()

const erreurs = ref({})
const succes = ref('')
const chargementNom = ref(false)
const chargementMdp = ref(false)
const chargementSuppression = ref(false)
const motDePasseConfirmation = ref('')
let modalInstance = null

const formNom = ref({ nomUtilisateur: '' })
const formMdp = ref({ actuel: '', nouveau: '', confirmation: '' })

onUnmounted(() => notif.clear())

onMounted(() => {
    modalInstance = new Modal(document.getElementById('suppressionModal'))
})

watch(() => auth.nom, (nouvelleValeur) => {
    if (nouvelleValeur) {
        formNom.value.nomUtilisateur = nouvelleValeur
    }
}, { immediate: true })

async function modifierNom() {
    erreurs.value = {}
    succes.value = ''

    if (!formNom.value.nomUtilisateur.trim()) {
        erreurs.value.nomUtilisateur = 'Le nom d\'utilisateur est obligatoire.'
        return
    }
    if (formNom.value.nomUtilisateur === auth.nom) {
        erreurs.value.nomUtilisateur = 'Le nom est identique à l\'actuel.'
        return
    }

    chargementNom.value = true
    try {
        const res = await fetch('/api/profil/nom', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${auth.token}` },
            body: JSON.stringify({ nomUtilisateur: formNom.value.nomUtilisateur })
        })
        const data = await res.json()
        if (res.ok) {
            auth.connecter(data.token)
            succes.value = 'Nom d\'utilisateur modifié avec succès.'
        } else {
            erreurs.value = data?.erreurs ?? { general: 'Erreur lors de la modification' }
        }
    } catch (e) {
        erreurs.value.general = 'Erreur lors de la modification'
    } finally {
        chargementNom.value = false
    }
}

async function modifierMdp() {
    erreurs.value = {}
    succes.value = ''

    if (!formMdp.value.actuel) {
        erreurs.value.actuel = 'Le mot de passe actuel est obligatoire.'
        return
    }
    if (!formMdp.value.nouveau) {
        erreurs.value.nouveau = 'Le nouveau mot de passe est obligatoire.'
        return
    }
    if (formMdp.value.nouveau !== formMdp.value.confirmation) {
        erreurs.value.confirmation = 'Les mots de passe ne correspondent pas.'
        return
    }

    chargementMdp.value = true
    try {
        const res = await fetch('/api/profil/motdepasse', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${auth.token}` },
            body: JSON.stringify({
                actuel: formMdp.value.actuel,
                nouveau: formMdp.value.nouveau
            })
        })
        const data = await res.json()
        if (res.ok) {
            formMdp.value = { actuel: '', nouveau: '', confirmation: '' }
            succes.value = 'Mot de passe modifié avec succès.'
        } else {
            erreurs.value = data?.erreurs ?? { general: 'Erreur lors de la modification' }
        }
    } catch (e) {
        erreurs.value.general = 'Erreur lors de la modification'
    } finally {
        chargementMdp.value = false
    }
}

function ouvrirModalSuppression() {
    motDePasseConfirmation.value = ''
    erreurs.value = {}
    modalInstance.show()
}

async function supprimerCompte() {
    erreurs.value = {}

    if (!motDePasseConfirmation.value) {
        erreurs.value.suppression = 'Le mot de passe est obligatoire.'
        return
    }

    chargementSuppression.value = true
    try {
        const res = await fetch('/api/profil', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${auth.token}` },
            body: JSON.stringify({ motDePasse: motDePasseConfirmation.value })
        })
        const data = await res.json()
        if (res.ok) {
            modalInstance.hide()
            auth.deconnecter()
            notif.setNotif('Votre compte a été supprimé.', 'info')
            router.push('/')
        } else {
            erreurs.value.suppression = data?.erreurs?.motDePasse ?? 'Mot de passe incorrect.'
        }
    } catch (e) {
        erreurs.value.suppression = 'Erreur lors de la suppression'
    } finally {
        chargementSuppression.value = false
    }
}
</script>

<style scoped>
.container {
    padding: 24px;
    font-family: sans-serif;
    max-width: 640px;
}

.page-header {
    margin-bottom: 24px;
}

.page-title {
    font-size: 22px;
    font-weight: 700;
    color: #1a1d23;
}

.erreur-champ {
    color: #ef4444;
    font-size: 12px;
    margin-top: 4px;
    margin-bottom: 0;
}

.table-wrapper {
    background: #fff;
    border-radius: 14px;
    border: 1.5px solid #e8eaf0;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.profil-section {
    padding: 24px;
}

.profil-info {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
}

.avatar-cercle {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: #6366f1;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 700;
    flex-shrink: 0;
}

.profil-nom {
    font-weight: 600;
    font-size: 16px;
    color: #1a1d23;
}

.profil-role {
    font-size: 13px;
    color: #9ba3b0;
    text-transform: capitalize;
}

.divider {
    border: none;
    border-top: 1px solid #f0f2f6;
    margin: 20px 0;
}

.form-bloc {
    margin-bottom: 4px;
}

.form-titre {
    font-size: 15px;
    font-weight: 600;
    color: #1a1d23;
    margin-bottom: 14px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-bottom: 12px;
}

.form-group label {
    font-size: 13px;
    font-weight: 500;
    color: #4b5263;
}

.form-group input {
    border: 1.5px solid #e2e6ed;
    border-radius: 10px;
    padding: 9px 13px;
    font-family: inherit;
    font-size: 14px;
    color: #1a1d23;
    outline: none;
    transition: border-color 0.2s;
}

.form-group input:focus {
    border-color: #6366f1;
}

.btn-save {
    display: inline-flex;
    align-items: center;
    padding: 9px 20px;
    border-radius: 50px;
    border: none;
    background: #1a1d23;
    font-family: inherit;
    font-size: 14px;
    font-weight: 600;
    color: #fff;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-save:hover {
    background: #6366f1;
}

.btn-save:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.danger-zone {}

.danger-titre {
    color: #ef4444;
}

.danger-desc {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 14px;
}

.btn-danger {
    display: inline-flex;
    align-items: center;
    padding: 9px 20px;
    border-radius: 50px;
    border: 1.5px solid #ef4444;
    background: transparent;
    font-family: inherit;
    font-size: 14px;
    font-weight: 600;
    color: #ef4444;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-danger:hover {
    background: #fee2e2;
}

:deep(.modal-content) {
    background-color: #fff;
    color: #1a1d23;
}

:deep(.modal-header) {
    border-bottom: 1px solid #f0f2f6;
}

:deep(.modal-footer) {
    border-top: 1px solid #f0f2f6;
}

:deep(.modal-title) {
    color: #1a1d23;
    font-weight: 600;
}

:deep(.modal-body p) {
    color: #4b5263;
    font-size: 14px;
}

:deep(.modal-body .form-control) {
    background-color: #fff;
    color: #1a1d23;
    border: 1.5px solid #e2e6ed;
    border-radius: 10px;
    padding: 9px 13px;
}

:deep(.modal-body .form-control:focus) {
    border-color: #6366f1;
    box-shadow: none;
}
</style>