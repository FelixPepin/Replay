# Replay — Marketplace de jeux vidéo d'occasion

**Replay** est une plateforme web de type marketplace permettant aux joueurs d'acheter, vendre et louer des jeux vidéo d'occasion entre particuliers.

> Projet de cégep (session Hiver 2026). Il n'est plus hébergé en ligne : il se lance **uniquement en local**, en suivant le guide ci-dessous.

---

## Lancer l'application (guide complet)

Ce guide part de zéro : aucune connaissance du projet n'est nécessaire. Comptez environ 10 minutes la première fois.

### Étape 1 — Installer les outils

Installez ces trois logiciels (une seule fois) :

| Outil | Version | Téléchargement |
|---|---|---|
| Docker Desktop | récente | <https://www.docker.com/products/docker-desktop/> |
| Python | 3.10 ou plus | <https://www.python.org/downloads/> (sous Windows, cochez **« Add python.exe to PATH »**) |
| Node.js | 20.19+ ou 22.12+ | <https://nodejs.org/> (version LTS) |

Il faut aussi [Git](https://git-scm.com/downloads) pour récupérer le code (ou téléchargez le ZIP depuis GitHub).

Vérifiez l'installation dans un terminal :

```bash
docker --version
python --version
node --version
```

> Sous macOS/Linux, remplacez `python` par `python3` et `pip` par `pip3` dans toutes les commandes.

### Étape 2 — Récupérer le code

```bash
git clone https://github.com/FelixPepin/Replay.git
cd Replay
```

Toutes les commandes suivantes partent de ce dossier `Replay`.

### Étape 3 — Démarrer la base de données

1. Ouvrez **Docker Desktop** et attendez qu'il indique que le moteur est démarré.
2. Dans le terminal :

   ```bash
   docker compose up -d
   ```

Docker télécharge MySQL 8, crée la base `replay` et la remplit avec des données de test. La première fois, attendez **environ 30 secondes** avant de passer à l'étape suivante (le temps que MySQL s'initialise).

### Étape 4 — Lancer le backend (API Flask)

Dans le même terminal :

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Quand le terminal affiche `Running on http://127.0.0.1:5000`, l'API est prête. **Laissez ce terminal ouvert.**

Aucune configuration n'est nécessaire : le fichier `backend/.env` est déjà fourni avec les bonnes valeurs.

### Étape 5 — Lancer le frontend (Vue.js)

Ouvrez un **deuxième terminal** dans le dossier `Replay`, puis :

```bash
cd frontend
npm install
npm run dev
```

Quand le terminal affiche `Local: http://localhost:5173/`, le site est prêt. **Laissez ce terminal ouvert aussi.**

### Étape 6 — Utiliser le site

Ouvrez <http://localhost:5173> dans votre navigateur et connectez-vous avec un des comptes de test :

| Rôle | Courriel | Mot de passe |
|---|---|---|
| Admin | `admin@replay.test` | `Admin123!` |
| Vendeur | `vendeur@replay.test` | `Vendeur123!` |
| Vendeur | `julie@replay.test` | `Vendeur123!` |
| Client | `client@replay.test` | `Client123!` |
| Coach (Minecraft, GTA V) | `coach@replay.test` | `Coach123!` |

Vous pouvez aussi créer votre propre compte avec le bouton « Inscription » en haut de la page.

### Arrêter et relancer

- **Arrêter :** faites `Ctrl + C` dans les deux terminaux, puis `docker compose stop`.
- **Relancer plus tard :** `docker compose up -d`, puis `python app.py` dans `backend` et `npm run dev` dans `frontend`. Les étapes `pip install` et `npm install` ne sont à refaire que si les dépendances changent.
- **Remettre les données de test à zéro** (efface tout ce qui a été ajouté) :

  ```bash
  docker compose down -v
  docker compose up -d
  ```

### En cas de problème

| Symptôme | Solution |
|---|---|
| `docker` : « cannot connect to the Docker daemon » | Docker Desktop n'est pas démarré. Ouvrez-le et attendez qu'il soit prêt. |
| `docker compose up` : « port 3306 is already allocated » | Un autre MySQL (installé localement, WAMP, etc.) utilise le port 3306. Arrêtez-le, ou remplacez `"3306:3306"` par `"3307:3306"` dans `docker-compose.yml` et `DB_PORT=3306` par `DB_PORT=3307` dans `backend/.env`. |
| Backend : « Can't connect to MySQL server » | La base n'a pas fini de démarrer. Attendez quelques secondes et relancez `python app.py`. Vérifiez avec `docker compose ps` que `replay-db` est démarré. |
| `python` ou `pip` introuvable | Sous Windows, essayez `py` et `py -m pip`. Sinon, réinstallez Python en cochant « Add python.exe to PATH ». |
| Le site affiche des erreurs ou une page vide | Vérifiez que le backend (étape 4) tourne toujours dans son terminal. |
| Paiement « En ligne » en erreur | Normal sans clé Stripe : voir [Paiement en ligne (Stripe)](#paiement-en-ligne-stripe). Les annonces « En main propre » fonctionnent sans configuration. |

---

## À propos du projet

Projet réalisé dans le cadre d'un cours de développement web au cégep, durant la session **Hiver 2026**. Le concept, le design et toute l'architecture technique ont été pensés et construits de A à Z par moi et mon coéquipier.

Le site était hébergé en ligne pendant la session ; il ne l'est plus. Il fonctionne entièrement en local, sans dépendance à un service externe (hormis Stripe, facultatif).

### Ce que fait le site

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

### Stack technique

| Couche | Technologie |
|---|---|
| Frontend | Vue.js + Vite |
| Backend | Python / Flask |
| Base de données | MySQL 8 (locale, via Docker) |
| Paiement en ligne | Stripe (mode test, facultatif) |

---

## Détails techniques

### Base de données

Au premier démarrage, le conteneur `replay-db` exécute automatiquement [`backend/db/schema.sql`](backend/db/schema.sql) (structure des tables) puis [`backend/db/seed.sql`](backend/db/seed.sql) (données de test). MySQL écoute sur `localhost:3306` (utilisateur `replay`, mot de passe `replay`).

Les données de test comprennent les comptes ci-dessus, des annonces de vente et de location (dates relatives au jour de l'initialisation), des réservations, des évaluations en attente et des questions/réponses dans le forum.

Les quiz (Minecraft, Pokémon, God of War, GTA V, Fortnite — 10 questions chacun) sont définis dans [`frontend/src/data/quizzes.js`](frontend/src/data/quizzes.js). Un score parfait promeut l'utilisateur coach du jeu correspondant (l'`id` du quiz correspond à `jeux.id` en base).

<details>
<summary>Utiliser MySQL installé localement (sans Docker)</summary>

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

### Configuration (`backend/.env`)

Le fichier [`backend/.env`](backend/.env) est versionné volontairement : il ne contient que des valeurs locales sans données sensibles, alignées sur `docker-compose.yml`. Le modèle [`backend/.env.example`](backend/.env.example) documente chaque variable :

| Variable | Rôle |
|---|---|
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | Connexion MySQL |
| `DB_SSL` | `false` en local ; `true` pour forcer SSL vers une BD distante |
| `SECRET_KEY` | Signature des jetons JWT |
| `STRIPE_SECRET_KEY` | Clé de test Stripe (`sk_test_...`), facultative |
| `FRONTEND_URL` | URL du frontend (CORS et redirections Stripe) |

### Paiement en ligne (Stripe)

Sans clé Stripe, les annonces dont le paiement est « En main propre » fonctionnent normalement ; le paiement « En ligne » renvoie une erreur. Pour l'activer, créez un compte Stripe gratuit, copiez la clé secrète de test (`sk_test_...`) dans `STRIPE_SECRET_KEY` de `backend/.env`, puis relancez le backend.

### Architecture locale

| Service | Adresse |
|---|---|
| Frontend (Vite) | <http://localhost:5173> |
| API (Flask) | <http://localhost:5000> |
| MySQL (Docker) | `localhost:3306` |

Vite redirige les requêtes `/api` et `/static` du frontend vers le backend Flask.
