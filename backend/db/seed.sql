-- ============================================================
-- Replay — données de test
-- À exécuter après schema.sql.
--
-- Comptes (mots de passe hachés avec bcrypt, comme routes/authentification.py) :
--   admin@replay.local    / Admin123!     (admin)
--   vendeur@replay.local  / Vendeur123!   (vendeur)
--   julie@replay.local    / Vendeur123!   (vendeur)
--   client@replay.local   / Client123!    (client)
--   coach@replay.local    / Coach123!     (coach : Minecraft, GTA V)
--
-- Les dates de location sont relatives à CURDATE() pour que les annonces
-- restent disponibles peu importe le moment où la BD est initialisée.
-- ============================================================

SET NAMES utf8mb4;
USE replay;

-- ------------------------------------------------------------
-- Utilisateurs
-- ------------------------------------------------------------
INSERT INTO utilisateurs (Id, NomUtilisateur, MotDePasse, Courriel, Role, note, nbEvaluation) VALUES
    (1, 'Admin',       '$2b$12$u25eyIlkkXYgJU9GABPreOP/P1xDCGqxosGwuOIwkNIf.u3VKERoe', 'admin@replay.local',   'admin',   0.0, 0),
    (2, 'MarcVend',    '$2b$12$9S.ISN3Pf9GRNQJPEfSxauVgFTOdSowmTdiAclFaMtg1K/nJVkP1u', 'vendeur@replay.local', 'vendeur', 4.5, 2),
    (3, 'SophieClient','$2b$12$0vY0Vbb89RAOBIoi/cyU4ugFemIM187cApsViaqQHLpRRlhc0Rk0C', 'client@replay.local',  'client',  0.0, 0),
    (4, 'CoachLeo',    '$2b$12$VGQ72IoL0SU9YQsSkwAQXOSBkGZuH0bj6lmDpr0aCfjAoTrn8DXj2', 'coach@replay.local',   'coach',   0.0, 0),
    (5, 'JulieGames',  '$2b$12$9S.ISN3Pf9GRNQJPEfSxauVgFTOdSowmTdiAclFaMtg1K/nJVkP1u', 'julie@replay.local',   'vendeur', 4.0, 1);

-- ------------------------------------------------------------
-- Annonces de vente (photos dans backend/static/images/ajouts)
-- ------------------------------------------------------------
INSERT INTO ventes (Id, NomJeu, Prix, Photo, TypeConsole, TypePaiement, TypeLivraison, Adresse, VendeurId, estVendu) VALUES
    (1, 'GTA V',              24.99, 'GTA_V.webp',             'PS4',             'En ligne',       'Par la poste',   '',                              2, 0),
    (2, 'Uncharted 4',        19.99, 'uncharted4.jpg',         'PS4',             'En main propre', 'En main propre', '1020 rue Saint-Jean, Québec',   2, 0),
    (3, 'Pokémon Épée',       39.99, 'pokemonepee.webp',       'Nintendo Switch', 'En ligne',       'Par la poste',   '',                              5, 0),
    (4, 'Super Mario Galaxy', 14.50, 'super mario galaxie.jpg','Wii',             'En main propre', 'En main propre', '2450 boul. Laurier, Québec',    5, 0),
    (5, 'Battlefield 3',       7.99, 'battlefield3.webp',      'Xbox 360',        'En ligne',       'Par la poste',   '',                              2, 1),
    (6, 'Wolfenstein II',     17.00, 'wolfenstein2.webp',      'Xbox One',        'En ligne',       'Par la poste',   '',                              5, 0),
    (7, 'The Simpsons Game',   9.99, 'the simpsons game.jpg',  'PS3',             'En main propre', 'En main propre', '1700 av. Maguire, Québec',      2, 0);

-- ------------------------------------------------------------
-- Annonces de location
-- ------------------------------------------------------------
INSERT INTO locations (Id, NomJeu, Prix, Photo, TypeConsole, TypePaiement, Adresse, DateDebut, DateFin, LocateurId, EstLoue, estDisponible) VALUES
    (1, 'Hollow Knight',       5.00, 'hollow knight.webp',        'Nintendo Switch',   'En ligne',       '1020 rue Saint-Jean, Québec', CURDATE() + INTERVAL 1 DAY, CURDATE() + INTERVAL 60 DAY, 2, 1, 1),
    (2, 'Zelda Skyward Sword', 4.00, 'Zelda-Skyward-Sword-Wii.webp','Wii',             'En main propre', '2450 boul. Laurier, Québec',  CURDATE() + INTERVAL 2 DAY, CURDATE() + INTERVAL 45 DAY, 5, 0, 1),
    (3, 'Call of Duty WWII',   6.50, 'callofdutyWWII.webp',       'PS4',               'En ligne',       '1020 rue Saint-Jean, Québec', CURDATE() + INTERVAL 1 DAY, CURDATE() + INTERVAL 30 DAY, 2, 0, 1),
    (4, 'Yoshi Woolly World',  4.50, 'yoshi wooly world.jpg',     'Wii U',             'En main propre', '2450 boul. Laurier, Québec',  CURDATE() + INTERVAL 3 DAY, CURDATE() + INTERVAL 40 DAY, 5, 1, 1),
    (5, 'Pokopia',             8.00, 'pokopia.jpg',               'Nintendo Switch 2', 'En ligne',       '1700 av. Maguire, Québec',    CURDATE() + INTERVAL 5 DAY, CURDATE() + INTERVAL 90 DAY, 2, 0, 1),
    (6, 'Spyro Reignited',     5.50, 'spyro.webp',                'PS4',               'En main propre', '1700 av. Maguire, Québec',    CURDATE() + INTERVAL 1 DAY, CURDATE() + INTERVAL 21 DAY, 5, 0, 1);

-- ------------------------------------------------------------
-- Réservations
-- ------------------------------------------------------------
INSERT INTO reservations_locations (Id, LocationId, UtilisateurId, DateDebutReservation, DateFinReservation) VALUES
    (1, 1, 3, CURDATE() + INTERVAL 5 DAY,  CURDATE() + INTERVAL 11 DAY),
    (2, 1, 4, CURDATE() + INTERVAL 20 DAY, CURDATE() + INTERVAL 26 DAY),
    (3, 4, 3, CURDATE() + INTERVAL 10 DAY, CURDATE() + INTERVAL 16 DAY);

-- ------------------------------------------------------------
-- Évaluations en attente (l'évaluateur doit encore noter le vendeur)
-- ------------------------------------------------------------
INSERT INTO evaluation (Id, IdVendeur, IdEvaluateur, NomJeu) VALUES
    (1, 2, 3, 'Battlefield 3'),
    (2, 5, 3, 'Yoshi Woolly World'),
    (3, 2, 4, 'Hollow Knight');

-- ------------------------------------------------------------
-- Forum : les jeux 1 à 5 correspondent aux quiz de
-- frontend/src/data/quizzes.js (quiz.id = jeux.id).
-- ------------------------------------------------------------
INSERT INTO jeux (id, nom, image) VALUES
    (1, 'Minecraft',            '/static/uploads/jeux/minecraft.jpg'),
    (2, 'Pokémon',              '/static/uploads/jeux/pokemon.jpg'),
    (3, 'God of War',           '/static/uploads/jeux/gow.jpg'),
    (4, 'GTA V',                '/static/uploads/jeux/Grand_Theft_Auto_V.png'),
    (5, 'Fortnite',             '/static/uploads/jeux/fortnite.jpg'),
    (6, 'Hollow Knight',        '/static/images/ajouts/hollow knight.webp'),
    (7, 'Uncharted 4',          '/static/images/ajouts/uncharted4.jpg'),
    (8, 'Zelda Skyward Sword',  '/static/images/ajouts/Zelda-Skyward-Sword-Wii.webp');

INSERT INTO coach_jeux (id_utilisateur, id_jeu) VALUES
    (4, 1),
    (4, 4);

INSERT INTO questions (id, titre, description, idJeu, idUtilisateur, dateCreation) VALUES
    (1, 'Meilleure façon de trouver des diamants ?',
        'Je creuse depuis des heures sans rien trouver. À quelle couche faut-il miner en 1.20+ ?',
        1, 3, NOW() - INTERVAL 6 DAY),
    (2, 'Comment survivre à la première nuit ?',
        'Je me fais toujours tuer par les zombies la première nuit. Des conseils ?',
        1, 2, NOW() - INTERVAL 4 DAY),
    (3, 'Braquage le plus rentable en solo ?',
        'Quel braquage rapporte le plus quand on joue seul en ligne ?',
        4, 3, NOW() - INTERVAL 3 DAY),
    (4, 'Quel starter choisir dans Pokémon Épée ?',
        'Ouistempo, Flambino ou Larméléon ? Lequel est le plus facile pour un débutant ?',
        2, 5, NOW() - INTERVAL 2 DAY),
    (5, 'Comment battre le Hornet du Vertchemin ?',
        'Je bloque sur le premier combat contre Hornet, elle est trop rapide.',
        6, 3, NOW() - INTERVAL 1 DAY);

INSERT INTO reponses (id, contenu, idQuestion, idUtilisateur, dateCreation) VALUES
    (1, 'Depuis la 1.18, mine autour de la couche Y=-58. Utilise une pioche en fer minimum et cherche près de la lave.',
        1, 4, NOW() - INTERVAL 5 DAY),
    (2, 'Coupe du bois tout de suite, fabrique un lit avec 3 laines ou creuse-toi un abri dans une colline avant le coucher du soleil.',
        2, 4, NOW() - INTERVAL 3 DAY),
    (3, 'Le Cayo Perico reste le plus payant en solo : environ 1 M$ par exécution une fois les préparatifs maîtrisés.',
        3, 4, NOW() - INTERVAL 2 DAY);
