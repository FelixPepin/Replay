# Replay — Marketplace de jeux vidéo d'occasion

**Replay** est une plateforme web de type marketplace permettant aux joueurs d'acheter, vendre et louer des jeux vidéo d'occasion entre particuliers.

> Projet réalisé dans le cadre d'un cours de développement web au cégep. Le concept, le design et toute l'architecture technique ont été pensés et construits de A à Z par moi et mon coéquipier.

---

## Ce que fait le site

- **Vendre** un jeu : publier une annonce avec photo, prix, console, mode de paiement et de livraison
- **Louer** un jeu : mettre un jeu en location avec une période de disponibilité et un prix par semaine
- **Réserver** : réserver un jeu vendu ou en location directement sur la plateforme
- **Paiement** : en ligne ou en main propre selon l'entente entre les utilisateurs
- **Forum** : poser des questions et discuter par jeu vidéo
- **Évaluations** : laisser une note et un commentaire après une transaction
- **Comptes utilisateurs** : inscription, connexion, gestion du profil
- **Quiz** : questionnaires de culture générale par jeu vidéo (10 questions à choix multiples par jeu)
- **Panel admin** : interface de gestion des utilisateurs permettant de consulter tous les comptes et de modifier les rôles (admin, vendeur, client, coach)

Consoles supportées : PS5, PS4, PS3, Xbox Series X, Xbox One, Xbox 360, Nintendo Switch 2, Nintendo Switch, Wii U, Wii

---

## Stack technique

| Couche | Technologie |
|---|---|
| Frontend | Vue.js + Vite |
| Backend | Python / Flask |
| Base de données | MySQL (hébergé sur Aiven) |
| Hébergement | Render |

---

## Site en ligne

Le projet est hébergé sur Render et accessible ici :

**[https://replay-c3nw.onrender.com/](https://replay-c3nw.onrender.com/)**

> Note : l'instance Render est sur un plan gratuit — le premier chargement peut prendre quelques secondes le temps que le serveur se réveille.

---

## Lancer le projet en local

### Prérequis

- Node.js (v18+)
- Python 3.10+
- pip

---

### Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

L'API démarre sur `http://localhost:5000`.

**À propos du fichier `.env` :** En temps normal, ce fichier ne devrait jamais être versionné dans Git car il contient des identifiants sensibles. Il est ici inclus **intentionnellement** pour permettre à quiconque de faire tourner le projet en local sans configuration supplémentaire. Les identifiants donnent accès à une base de données de développement sans données sensibles.

---

### Frontend (Vue.js)

```bash
cd frontend
npm install
npm run dev
```

Le frontend démarre sur `http://localhost:5173` et pointe automatiquement vers le backend local.
