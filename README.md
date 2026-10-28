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
| Base de données | MySQL 8 (locale, via Docker) |
| Paiement en ligne | Stripe (mode test, facultatif) |

---

## Statut du projet

Replay est un travail réalisé au cégep durant la session **Hiver 2026**. Il n'est **plus hébergé en ligne** : le projet se lance uniquement en local, sans aucune dépendance à un service externe (hormis Stripe, facultatif).

---

## Lancer le projet en local

### Prérequis

- [Docker](https://www.docker.com/) (Docker Desktop sous Windows/macOS)
- Python 3.10+ et pip
- Node.js 20.19+ ou 22.12+

### 1. Base de données (MySQL)

```bash
docker compose up -d
```

Au premier démarrage, le conteneur `replay-db` crée la base `replay` et exécute automatiquement [`backend/db/schema.sql`](backend/db/schema.sql) puis [`backend/db/seed.sql`](backend/db/seed.sql). MySQL écoute sur `localhost:3306` (utilisateur `replay`, mot de passe `replay`).

Pour **réinitialiser** la base (efface toutes les données et réexécute les scripts) :

```bash
docker compose down -v
docker compose up -d
```

<details>
<summary>Sans Docker (MySQL installé localement)</summary>

Avec un serveur MySQL 8 qui écoute sur le port 3306 et le client `mysql` dans le PATH :

```bash
cd backend
python db/reset_db.py -u root
```

Le script exécute `schema.sql` puis `seed.sql` et crée l'utilisateur de l'application défini dans `backend/.env` (`replay` / `replay`). Si `mysql` n'est pas dans le PATH, passez son chemin avec `--mysql "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"`.

Équivalent manuel :

```bash
mysql -u root -p < backend/db/schema.sql
mysql -u root -p < backend/db/seed.sql
```

</details>

### 2. Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

L'API démarre sur `http://localhost:5000`.

La configuration est lue depuis [`backend/.env`](backend/.env), versionné volontairement : il ne contient que des valeurs locales sans données sensibles, alignées sur `docker-compose.yml`. Le modèle [`backend/.env.example`](backend/.env.example) documente chaque variable :

| Variable | Rôle |
|---|---|
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | Connexion MySQL |
| `DB_SSL` | `false` en local ; `true` pour forcer SSL vers une BD distante |
| `SECRET_KEY` | Signature des jetons JWT |
| `STRIPE_SECRET_KEY` | Clé de test Stripe (`sk_test_...`), facultative |
| `FRONTEND_URL` | URL du frontend (CORS et redirections Stripe) |

> Sans clé Stripe, les annonces dont le paiement est « En main propre » fonctionnent normalement ; le paiement « En ligne » renvoie une erreur.

### 3. Frontend (Vue.js)

```bash
cd frontend
npm install
npm run dev
```

Le frontend démarre sur `http://localhost:5173`. Vite redirige `/api` et `/static` vers le backend `http://localhost:5000`.

---

## Comptes de test

| Rôle | Courriel | Mot de passe |
|---|---|---|
| Admin | `admin@replay.test` | `Admin123!` |
| Vendeur | `vendeur@replay.test` | `Vendeur123!` |
| Vendeur | `julie@replay.test` | `Vendeur123!` |
| Client | `client@replay.test` | `Client123!` |
| Coach (Minecraft, GTA V) | `coach@replay.test` | `Coach123!` |

Les données de test comprennent aussi des annonces de vente et de location (dates relatives au jour de l'initialisation), des réservations, des évaluations en attente et des questions/réponses dans le forum.

Les quiz (Minecraft, Pokémon, God of War, GTA V, Fortnite — 10 questions chacun) sont définis dans [`frontend/src/data/quizzes.js`](frontend/src/data/quizzes.js). Un score parfait promeut l'utilisateur coach du jeu correspondant (l'`id` du quiz correspond à `jeux.id` en base).
