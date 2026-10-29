-- ============================================================
-- Replay — schéma de la base de données (MySQL 8, utf8mb4, InnoDB)
-- ============================================================
-- Reconstruit à partir des requêtes SQL de backend/routes/*.py.
-- La casse des noms de colonnes est importante : les routes qui font
-- SELECT * renvoient les clés JSON telles que définies ici
-- (ex. locations.estDisponible, jeux.nom, questions.dateCreation).
--
-- Notes :
--  - Les quiz sont définis côté frontend (frontend/src/data/quizzes.js).
--    L'id de chaque quiz correspond à jeux.id (utilisé par coach_jeux).
--  - Les paiements passent par Stripe : aucune table dédiée, le résultat
--    met à jour ventes.estVendu ou crée une ligne dans reservations_locations.
-- ============================================================

CREATE DATABASE IF NOT EXISTS replay
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE replay;

DROP TABLE IF EXISTS reponses;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS coach_jeux;
DROP TABLE IF EXISTS jeux;
DROP TABLE IF EXISTS evaluation;
DROP TABLE IF EXISTS reservations_locations;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS ventes;
DROP TABLE IF EXISTS utilisateurs;

-- ------------------------------------------------------------
-- Utilisateurs (rôles : admin, vendeur, client, coach)
-- note / nbEvaluation : moyenne des évaluations reçues en tant que vendeur
-- ------------------------------------------------------------
CREATE TABLE utilisateurs (
    Id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    NomUtilisateur  VARCHAR(50)  NOT NULL,
    MotDePasse      VARCHAR(255) NOT NULL,          -- hash bcrypt
    Courriel        VARCHAR(255) NOT NULL,
    Role            ENUM('admin', 'vendeur', 'client', 'coach') NOT NULL DEFAULT 'vendeur',
    note            DECIMAL(2,1) NOT NULL DEFAULT 0.0,
    nbEvaluation    INT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (Id),
    UNIQUE KEY uq_utilisateurs_courriel (Courriel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Annonces de vente
-- ------------------------------------------------------------
CREATE TABLE ventes (
    Id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    NomJeu          VARCHAR(20)  NOT NULL,
    Prix            DECIMAL(5,2) NOT NULL,
    Photo           VARCHAR(255) NOT NULL,          -- fichier dans backend/static/images/ajouts
    TypeConsole     ENUM('PS5', 'PS4', 'PS3', 'Xbox Series X', 'Xbox One', 'Xbox 360',
                         'Nintendo Switch 2', 'Nintendo Switch', 'Wii U', 'Wii') NOT NULL,
    TypePaiement    ENUM('En ligne', 'En main propre') NOT NULL,
    TypeLivraison   ENUM('Par la poste', 'En main propre') NOT NULL,
    Adresse         VARCHAR(255) NOT NULL DEFAULT '',
    VendeurId       INT UNSIGNED NOT NULL,
    estVendu        TINYINT(1)   NOT NULL DEFAULT 0,
    PRIMARY KEY (Id),
    KEY idx_ventes_vendeur (VendeurId),
    CONSTRAINT fk_ventes_vendeur FOREIGN KEY (VendeurId)
        REFERENCES utilisateurs (Id) ON DELETE CASCADE,
    CONSTRAINT chk_ventes_prix CHECK (Prix > 0 AND Prix <= 60)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Annonces de location (période de disponibilité + prix)
-- ------------------------------------------------------------
CREATE TABLE locations (
    Id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    NomJeu          VARCHAR(20)  NOT NULL,
    Prix            DECIMAL(5,2) NOT NULL,
    Photo           VARCHAR(255) NOT NULL,
    TypeConsole     ENUM('PS5', 'PS4', 'PS3', 'Xbox Series X', 'Xbox One', 'Xbox 360',
                         'Nintendo Switch 2', 'Nintendo Switch', 'Wii U', 'Wii') NOT NULL,
    TypePaiement    ENUM('En ligne', 'En main propre') NOT NULL,
    Adresse         VARCHAR(255) NOT NULL,
    DateDebut       DATE         NOT NULL,
    DateFin         DATE         NOT NULL,
    LocateurId      INT UNSIGNED NOT NULL,
    EstLoue         TINYINT(1)   NOT NULL DEFAULT 0,  -- au moins une réservation
    estDisponible   TINYINT(1)   NOT NULL DEFAULT 1,  -- 0 quand toutes les dates sont réservées
    PRIMARY KEY (Id),
    KEY idx_locations_locateur (LocateurId),
    CONSTRAINT fk_locations_locateur FOREIGN KEY (LocateurId)
        REFERENCES utilisateurs (Id) ON DELETE CASCADE,
    CONSTRAINT chk_locations_prix CHECK (Prix > 0 AND Prix <= 60),
    CONSTRAINT chk_locations_dates CHECK (DateFin > DateDebut)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Réservations d'une location
-- ------------------------------------------------------------
CREATE TABLE reservations_locations (
    Id                    INT UNSIGNED NOT NULL AUTO_INCREMENT,
    LocationId            INT UNSIGNED NOT NULL,
    UtilisateurId         INT UNSIGNED NOT NULL,
    DateDebutReservation  DATE NOT NULL,
    DateFinReservation    DATE NOT NULL,
    PRIMARY KEY (Id),
    KEY idx_reservations_location (LocationId),
    KEY idx_reservations_utilisateur (UtilisateurId),
    CONSTRAINT fk_reservations_location FOREIGN KEY (LocationId)
        REFERENCES locations (Id) ON DELETE CASCADE,
    CONSTRAINT fk_reservations_utilisateur FOREIGN KEY (UtilisateurId)
        REFERENCES utilisateurs (Id) ON DELETE CASCADE,
    CONSTRAINT chk_reservations_dates CHECK (DateFinReservation >= DateDebutReservation)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Évaluations en attente : créées après un achat/une location,
-- supprimées une fois que l'acheteur a donné sa note
-- (la note est cumulée dans utilisateurs.note / nbEvaluation).
-- ------------------------------------------------------------
CREATE TABLE evaluation (
    Id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    IdVendeur       INT UNSIGNED NOT NULL,
    IdEvaluateur    INT UNSIGNED NOT NULL,
    NomJeu          VARCHAR(20)  NOT NULL,
    PRIMARY KEY (Id),
    KEY idx_evaluation_vendeur (IdVendeur),
    KEY idx_evaluation_evaluateur (IdEvaluateur),
    CONSTRAINT fk_evaluation_vendeur FOREIGN KEY (IdVendeur)
        REFERENCES utilisateurs (Id) ON DELETE CASCADE,
    CONSTRAINT fk_evaluation_evaluateur FOREIGN KEY (IdEvaluateur)
        REFERENCES utilisateurs (Id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- Forum : jeux, questions et réponses (réservées aux coachs du jeu)
-- ------------------------------------------------------------
CREATE TABLE jeux (
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nom             VARCHAR(100) NOT NULL,
    image           VARCHAR(255) NULL,              -- URL relative, ex. /static/uploads/jeux/x.jpg
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE coach_jeux (
    id_utilisateur  INT UNSIGNED NOT NULL,
    id_jeu          INT UNSIGNED NOT NULL,
    PRIMARY KEY (id_utilisateur, id_jeu),
    KEY idx_coach_jeux_jeu (id_jeu),
    CONSTRAINT fk_coach_jeux_utilisateur FOREIGN KEY (id_utilisateur)
        REFERENCES utilisateurs (Id) ON DELETE CASCADE,
    CONSTRAINT fk_coach_jeux_jeu FOREIGN KEY (id_jeu)
        REFERENCES jeux (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE questions (
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    titre           VARCHAR(255) NOT NULL,
    description     TEXT         NOT NULL,
    idJeu           INT UNSIGNED NOT NULL,
    idUtilisateur   INT UNSIGNED NOT NULL,
    dateCreation    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_questions_jeu (idJeu),
    KEY idx_questions_utilisateur (idUtilisateur),
    CONSTRAINT fk_questions_jeu FOREIGN KEY (idJeu)
        REFERENCES jeux (id) ON DELETE CASCADE,
    CONSTRAINT fk_questions_utilisateur FOREIGN KEY (idUtilisateur)
        REFERENCES utilisateurs (Id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE reponses (
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    contenu         TEXT         NOT NULL,
    idQuestion      INT UNSIGNED NOT NULL,
    idUtilisateur   INT UNSIGNED NOT NULL,
    dateCreation    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_reponses_question (idQuestion),
    KEY idx_reponses_utilisateur (idUtilisateur),
    CONSTRAINT fk_reponses_question FOREIGN KEY (idQuestion)
        REFERENCES questions (id) ON DELETE CASCADE,
    CONSTRAINT fk_reponses_utilisateur FOREIGN KEY (idUtilisateur)
        REFERENCES utilisateurs (Id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
