<template>
    <div class="game-card" :class="{ 'game-card--vendu': jeu.estVendu }">

        <div class="game-img-wrap">
            <img :src="`/static/images/ajouts/${jeu.Photo}`" :alt="jeu.NomJeu" class="game-img" />
            <span class="game-console-badge">{{ jeu.TypeConsole }}</span>
            <span v-if="jeu.estVendu" class="vendu-overlay">Vendu</span>
        </div>

        <div class="game-body">
            <h3 class="game-title">{{ jeu.NomJeu }}</h3>

            <p v-if="afficherVendeur" class="game-seller">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                </svg>
                {{ jeu.NomUtilisateur }}
            </p>

            <!-- Tags livraison/paiement (achat et gestion) -->
            <div v-if="mode !== 'location'" class="game-meta">
                <span class="meta-tag">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                    {{ jeu.TypeLivraison }}
                </span>
                <span class="meta-tag">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="1" y="4" width="22" height="16" rx="2" />
                        <line x1="1" y1="10" x2="23" y2="10" />
                    </svg>
                    {{ jeu.TypePaiement }}
                </span>
            </div>

            <!-- Dates de disponibilité (location) -->
            <div v-if="mode === 'location'" class="game-dates">
                <span class="meta-tag">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" />
                        <line x1="16" y1="2" x2="16" y2="6" />
                        <line x1="8" y1="2" x2="8" y2="6" />
                        <line x1="3" y1="10" x2="21" y2="10" />
                    </svg>
                    Début : {{ formatDate(jeu.DateDebut) }}
                </span>
                <span class="meta-tag">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" />
                        <line x1="16" y1="2" x2="16" y2="6" />
                        <line x1="8" y1="2" x2="8" y2="6" />
                        <line x1="3" y1="10" x2="21" y2="10" />
                    </svg>
                    Fin : {{ formatDate(jeu.DateFin) }}
                </span>
            </div>
        </div>

        <div class="game-footer">
            <span class="game-price">{{ jeu.Prix }} $</span>

            <!-- Mode achat -->
            <RouterLink v-if="mode === 'achat'" :to="`/acheter/${jeu.Id}`" class="btn-acheter">
                Acheter
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
            </RouterLink>

            <!-- Mode location -->
            <RouterLink v-if="mode === 'location'" :to="`/louer/${jeu.Id}`" class="btn-louer">
                Louer
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
            </RouterLink>

            <!-- Mode gestion -->
            <div v-if="mode === 'gestion'" class="game-actions">
                <RouterLink :to="`/modifierVente/${jeu.Id}`" class="btn-modifier" title="Modifier">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                    </svg>
                </RouterLink>
                <RouterLink :to="`/supprimerVente/${jeu.Id}`" class="btn-supprimer" title="Supprimer">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6l-1 14H6L5 6" />
                        <path d="M10 11v6" />
                        <path d="M14 11v6" />
                        <path d="M9 6V4h6v2" />
                    </svg>
                </RouterLink>
            </div>
        </div>

    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    jeu: {
        type: Object,
        required: true
    },
    mode: {
        type: String,
        default: 'achat',
        validator: (v) => ['achat', 'gestion', 'location'].includes(v)
    }
})

const afficherVendeur = computed(() => props.mode === 'achat')

function formatDate(date) {
    const d = new Date(date)
    if (isNaN(d)) return date
    const str = new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate())
        .toLocaleDateString('fr-CA', { day: 'numeric', month: 'long', year: 'numeric' })
    return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

.game-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(8px);
    border-radius: 16px;
    border: 1.5px solid rgba(255, 255, 255, 0.6);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
}

.game-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
    border-color: #6366f1;
}

.game-card--vendu {
    opacity: 0.6;
}

.game-img-wrap {
    position: relative;
    height: 180px;
    background: #f0f2f6;
    overflow: hidden;
}

.game-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s;
}

.game-card:hover .game-img {
    transform: scale(1.04);
}

.game-console-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(26, 29, 35, 0.85);
    color: #fff;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 50px;
    backdrop-filter: blur(4px);
}

.vendu-overlay {
    position: absolute;
    inset: 0;
    background: rgba(26, 29, 35, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #fff;
    letter-spacing: 2px;
    backdrop-filter: blur(2px);
}

.game-body {
    padding: 14px 16px 10px;
    flex: 1;
}

.game-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #1a1d23;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.game-seller {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 12.5px;
    color: #6b7280;
    margin-bottom: 10px;
}

.game-seller svg {
    width: 13px;
    height: 13px;
    flex-shrink: 0;
}

.game-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.game-dates {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-top: 4px;
}

.meta-tag {
    display: flex;
    align-items: center;
    gap: 4px;
    background: #f4f5f7;
    border: 1px solid #e8eaf0;
    border-radius: 50px;
    padding: 3px 10px;
    font-size: 11.5px;
    color: #4b5263;
    font-weight: 500;
}

.meta-tag svg {
    width: 11px;
    height: 11px;
}

.game-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    border-top: 1px solid #f0f2f6;
}

.game-price {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #1a1d23;
}

.btn-acheter {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #1a1d23;
    color: #fff;
    text-decoration: none;
    font-size: 13px;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 50px;
    transition: background 0.2s;
    font-family: inherit;
}

.btn-acheter svg {
    width: 13px;
    height: 13px;
}

.btn-acheter:hover {
    background: #6366f1;
    color: #fff;
}

.btn-louer {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #0ea5e9;
    color: #fff;
    text-decoration: none;
    font-size: 13px;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 50px;
    transition: background 0.2s;
    font-family: inherit;
}

.btn-louer svg {
    width: 13px;
    height: 13px;
}

.btn-louer:hover {
    background: #0284c7;
    color: #fff;
}

.game-actions {
    display: flex;
    gap: 8px;
}

.btn-modifier,
.btn-supprimer {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    border: 1.5px solid transparent;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s;
    text-decoration: none;
}

.btn-modifier svg,
.btn-supprimer svg {
    width: 15px;
    height: 15px;
}

.btn-modifier {
    color: #6366f1;
}

.btn-modifier:hover {
    background: #ede9fe;
    border-color: #c4b5fd;
}

.btn-supprimer {
    color: #ef4444;
}

.btn-supprimer:hover {
    background: #fee2e2;
    border-color: #fca5a5;
}
</style>