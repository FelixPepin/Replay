// ============================================================
// FICHIER DE DONNÉES DES QUIZ
// ============================================================
// Pour ajouter un nouveau jeu, copiez le bloc ci-dessous et
// modifiez les valeurs. Chaque quiz doit avoir exactement
// 10 questions. L'index "reponse" correspond à la position
// du bon choix dans le tableau "choix" (0 = premier choix).
// ============================================================

export const quizzes = [
  {
    id: 1,
    nom: 'Minecraft',
    emoji: '⛏️',
    description: 'Testez vos connaissances sur le célèbre jeu de survie et de construction.',
    questions: [
      {
        question: 'Quel mob est connu pour exploser près du joueur ?',
        choix: ['Zombie', 'Squelette', 'Creeper', 'Enderman'],
        reponse: 2
      },
      {
        question: 'Quel bloc est utilisé pour construire le cadre d\'un portail du Nether ?',
        choix: ['Granite', 'Obsidienne', 'Pierre du Nether', 'Basalte'],
        reponse: 1
      },
      {
        question: 'Quelle pioche est le minimum requis pour miner du minerai de diamant ?',
        choix: ['Pioche en bois', 'Pioche en or', 'Pioche en fer', 'Pioche en pierre'],
        reponse: 2
      },
      {
        question: 'Quel est le nom du boss final de Minecraft ?',
        choix: ['Le Wither', 'Le Gardien Ancien', 'L\'Ender Dragon', 'Le Golem de Fer'],
        reponse: 2
      },
      {
        question: 'Quel animal faut-il tondre pour obtenir de la laine ?',
        choix: ['La vache', 'Le mouton', 'Le cochon', 'Le lapin'],
        reponse: 1
      },
      {
        question: 'Combien de slots contient un coffre simple ?',
        choix: ['18', '27', '36', '54'],
        reponse: 1
      },
      {
        question: 'Quel mob laisse tomber une Ender Pearl en mourant ?',
        choix: ['L\'Endermite', 'Le Shulker', 'Le Blaze', 'L\'Enderman'],
        reponse: 3
      },
      {
        question: 'Dans quel biome peut-on trouver des igloos ?',
        choix: ['Toundra enneigée', 'Désert', 'Jungle', 'Savane'],
        reponse: 0
      },
      {
        question: 'Quel bloc est complètement indestructible en mode Survie ?',
        choix: ['L\'obsidienne', 'La pierre noire (Deepslate)', 'La roche de base (Bedrock)', 'La pierre du Nether'],
        reponse: 2
      },
      {
        question: 'Quelle potion permet de respirer indéfiniment sous l\'eau ?',
        choix: ['Potion de Vision Nocturne', 'Potion de Respiration Aquatique', 'Potion d\'Invisibilité', 'Potion de Force'],
        reponse: 1
      }
    ]
  },

  {
    id: 2,
    nom: 'Pokémon',
    emoji: '🔴',
    description: 'Devenez le meilleur dresseur en testant vos connaissances sur l\'univers Pokémon.',
    questions: [
      {
        question: 'Quel Pokémon de départ est de type Feu dans Pokémon Rouge/Bleu ?',
        choix: ['Salamèche', 'Bulbizarre', 'Carapuce', 'Pikachu'],
        reponse: 0
      },
      {
        question: 'Quel est le numéro de Pikachu dans le Pokédex national ?',
        choix: ['#001', '#025', '#050', '#100'],
        reponse: 1
      },
      {
        question: 'Quel type est super efficace contre le type Eau ?',
        choix: ['Glace', 'Électrik', 'Feu', 'Normal'],
        reponse: 1
      },
      {
        question: 'Quel Pokémon légendaire est sur la pochette de Pokémon Or ?',
        choix: ['Entei', 'Suicune', 'Lugia', 'Ho-Oh'],
        reponse: 3
      },
      {
        question: 'Combien de Pokémon composent la première génération (Pokédex de Kanto) ?',
        choix: ['152', '150', '151', '100'],
        reponse: 2
      },
      {
        question: 'Quelle capacité permet d\'endormir un Pokémon adverse ?',
        choix: ['Rugissement', 'Mimi-Queue', 'Lilliput', 'Berceuse'],
        reponse: 3
      },
      {
        question: 'Quel objet fait évoluer Pikachu en Raichu ?',
        choix: ['Pierre Feu', 'Pierre Tonnerre', 'Pierre Eau', 'Pierre Lune'],
        reponse: 1
      },
      {
        question: 'Quels sont les types du Pokémon Fantominus (Gastly) ?',
        choix: ['Spectre/Poison', 'Ténèbres/Poison', 'Spectre/Normal', 'Psychique/Poison'],
        reponse: 0
      },
      {
        question: 'Quel est le nom du professeur Pokémon de la région de Kanto ?',
        choix: ['Professeur Sorbier', 'Professeur Chen', 'Professeur Orme', 'Professeur Bouleau'],
        reponse: 1
      },
      {
        question: 'Quel est le stade final d\'évolution de Salamèche ?',
        choix: ['Reptincel', 'Dracolosse', 'Mega-Dracaufeu X', 'Dracaufeu'],
        reponse: 3
      }
    ]
  },

  {
    id: 3,
    nom: 'God of War',
    emoji: '⚔️',
    description: 'Suivez Kratos et Atreus dans les royaumes nordiques. Prouvez que vous connaissez la saga God of War.',
    questions: [
      {
        question: 'Quel est le nom du fils de Kratos dans God of War (2018) ?',
        choix: ['Zeus', 'Atreus', 'Baldur', 'Freyr'],
        reponse: 1
      },
      {
        question: 'Quelle mythologie est au cœur de God of War (2018) ?',
        choix: ['Grecque', 'Égyptienne', 'Nordique', 'Romaine'],
        reponse: 2
      },
      {
        question: 'Quel est le nom de l\'arme principale de Kratos dans God of War (2018) ?',
        choix: ['La Hache du Léviathan', 'Les Lames du Chaos', 'L\'Épée de l\'Olympe', 'Le Glaive de Tyr'],
        reponse: 0
      },
      {
        question: 'Quel dieu est le principal antagoniste de God of War (2018) ?',
        choix: ['Thor', 'Odin', 'Tyr', 'Baldur'],
        reponse: 3
      },
      {
        question: 'Quel est le vrai nom d\'Atreus révélé à la fin de God of War (2018) ?',
        choix: ['Thor', 'Tyr', 'Loki', 'Odin'],
        reponse: 2
      },
      {
        question: 'Dans quelle mythologie se déroulent les God of War originaux (avant 2018) ?',
        choix: ['Nordique', 'Égyptienne', 'Mésopotamienne', 'Grecque'],
        reponse: 3
      },
      {
        question: 'Quel est le prénom de la mère d\'Atreus, la femme de Kratos ?',
        choix: ['Freya', 'Faye', 'Sif', 'Skadi'],
        reponse: 1
      },
      {
        question: 'Quel est le nom du royaume des humains dans la mythologie nordique de God of War ?',
        choix: ['Midgard', 'Asgard', 'Vanaheim', 'Niflheim'],
        reponse: 0
      },
      {
        question: 'Quelle est l\'arme de prédilection d\'Atreus au combat dans God of War (2018) ?',
        choix: ['Un bouclier enchanté', 'Une épée divine', 'Un arc et des flèches magiques', 'Un marteau de foudre'],
        reponse: 2
      },
      {
        question: 'Quel opus de la série God of War est sorti en 2022 ?',
        choix: ['God of War: Ascension', 'God of War: Ragnarök', 'God of War: Valhalla', 'God of War: Midgard'],
        reponse: 1
      }
    ]
  },

  {
    id: 4,
    nom: 'GTA V',
    emoji: '🚗',
    description: 'Bienvenue à Los Santos ! Prouvez que vous connaissez Grand Theft Auto V sur le bout des doigts.',
    questions: [
      {
        question: 'Dans quelle ville fictive se déroule principalement GTA V ?',
        choix: ['Vice City', 'Los Santos', 'Liberty City', 'San Fierro'],
        reponse: 1
      },
      {
        question: 'Combien de personnages jouables y a-t-il dans la campagne de GTA V ?',
        choix: ['1', '2', '3', '4'],
        reponse: 2
      },
      {
        question: 'Quel personnage est un ancien braqueur reconverti en homme de famille ?',
        choix: ['Trevor', 'Franklin', 'Lamar', 'Michael'],
        reponse: 3
      },
      {
        question: 'Quel est le nom de la plus haute montagne de GTA V ?',
        choix: ['Mount Chilliad', 'Mount Gordo', 'Mount Davis', 'Vinewood Peak'],
        reponse: 0
      },
      {
        question: 'Quel personnage est un ancien pilote militaire de formation ?',
        choix: ['Michael', 'Franklin', 'Lester', 'Trevor'],
        reponse: 3
      },
      {
        question: 'Comment s\'appelle l\'agence gouvernementale fictive équivalente du FBI dans GTA V ?',
        choix: ['NOOSE', 'IAA', 'FIB', 'LSPD'],
        reponse: 2
      },
      {
        question: 'Dans quel État fictif se situe Los Santos ?',
        choix: ['Vice State', 'Alderney', 'Liberty State', 'San Andreas'],
        reponse: 3
      },
      {
        question: 'Comment s\'appelle le quartier huppé de Los Santos (parodie de Beverly Hills) ?',
        choix: ['Vinewood Hills', 'Rockford Hills', 'Strawberry', 'Davis'],
        reponse: 1
      },
      {
        question: 'Quel est le nom de l\'aéroport principal de Los Santos ?',
        choix: ['Los Santos International Airport', 'Sandy Shores Airfield', 'Trevor\'s Airfield', 'McKenzie Airfield'],
        reponse: 0
      },
      {
        question: 'Comment s\'appelle la prison principale de GTA V ?',
        choix: ['San Andreas State Prison', 'Bolingbroke Penitentiary', 'Los Santos County Jail', 'Alamo Prison'],
        reponse: 1
      }
    ]
  },

  {
    id: 5,
    nom: 'Fortnite',
    emoji: '🎯',
    description: 'Constructeur ou frageur ? Montrez que vous maîtrisez l\'univers de Fortnite Battle Royale.',
    questions: [
      {
        question: 'Combien de joueurs participent à une partie de Fortnite Battle Royale standard ?',
        choix: ['100', '50', '75', '150'],
        reponse: 0
      },
      {
        question: 'Quel matériau ne peut PAS être récolté pour construire dans Fortnite ?',
        choix: ['Bois', 'Pierre', 'Verre', 'Métal'],
        reponse: 2
      },
      {
        question: 'Comment s\'appelle le bus qui transporte les joueurs au début de chaque partie ?',
        choix: ['War Bus', 'Drop Ship', 'Storm Bus', 'Battle Bus'],
        reponse: 3
      },
      {
        question: 'Quelle zone rétrécit progressivement et force les joueurs à se rapprocher ?',
        choix: ['La Tempête', 'La Zone Morte', 'Le Cercle Rouge', 'La Zone Finale'],
        reponse: 0
      },
      {
        question: 'Quel est le nom de la monnaie utilisée pour acheter des skins dans Fortnite ?',
        choix: ['G-Bucks', 'Storm Coins', 'Battle Coins', 'V-Bucks'],
        reponse: 3
      },
      {
        question: 'Quel est le nom du skin masculin par défaut, considéré comme la mascotte de Fortnite ?',
        choix: ['Peely', 'Jonesy', 'Fishstick', 'Brite Bomber'],
        reponse: 1
      },
      {
        question: 'Quelle est la rareté d\'arme la plus élevée dans Fortnite (hors évènements spéciaux) ?',
        choix: ['Légendaire', 'Épique', 'Mythique', 'Rare'],
        reponse: 2
      },
      {
        question: 'Quel objet restaure exactement 50 points de bouclier dans Fortnite ?',
        choix: ['Slurp Juice', 'Grande potion de bouclier', 'Mini bouclier', 'Chug Jug'],
        reponse: 1
      },
      {
        question: 'Comment s\'appelle le message de victoire affiché quand on gagne une partie ?',
        choix: ['Last Man Standing', 'Battle Won', 'Final Ring', 'Victory Royale'],
        reponse: 3
      },
      {
        question: 'Quel est le total maximum de points de vie + bouclier qu\'un joueur peut avoir dans Fortnite ?',
        choix: ['150', '300', '200', '250'],
        reponse: 2
      }
    ]
  },

  // ---- TEMPLATE POUR AJOUTER UN JEU ----
  // {
  //   id: 6,                       // identifiant unique (numérique, incrémenter)
  //   nom: 'Nom du Jeu',         // nom affiché
  //   emoji: '🎮',               // emoji représentatif
  //   description: 'Description courte du quiz.',
  //   questions: [
  //     {
  //       question: 'Votre question ici ?',
  //       choix: ['Choix A', 'Choix B', 'Choix C', 'Choix D'],
  //       reponse: 0  // index du bon choix (0, 1, 2 ou 3)
  //     },
  //     // ... (10 questions au total)
  //   ]
  // }
]
