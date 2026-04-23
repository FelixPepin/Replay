from flask import request, Blueprint, abort, jsonify, current_app
import mysql.connector
import bd
import os
import datetime

bp_location = Blueprint('location',__name__)

# Permet de mettre en location un jeu vidéo
@bp_location.route("/location", methods=['POST'])
def location():
    nomJeu = (request.form.get("nomJeu", "")).strip()
    prix_brut = request.form.get("prix", "")
    typeConsole = request.form.get("typeConsole", "")
    choixPaiement = request.form.get("choixPaiement", "")
    adresse = (request.form.get("adresse", "")).strip()
    dateDebut = request.form.get("dateDebut", "")
    dateFin = request.form.get("dateFin", "")
    locateurId = request.form.get("locateurId", "")
    photo = request.files.get("photo")

    CONSOLES_VALIDES = ['PS5', 'PS4', 'PS3', 'Xbox Series X', 'Xbox One', 'Xbox 360',
                        'Nintendo Switch 2', 'Nintendo Switch', 'Wii U', 'Wii']
    PAIEMENTS_VALIDES = ['En ligne', 'En main propre']
    EXTENSIONS_PERMISES = {'JPG', 'JPEG', 'PNG', 'WEBP'}

    erreurs = {}
    prix_float = None

    if not nomJeu:
        erreurs['nomJeu'] = 'Le nom du jeu est requis'
    elif len(nomJeu) < 3 or len(nomJeu) > 20:
        erreurs['nomJeu'] = 'Le nom du jeu doit être entre 3 et 20 caractères'

    try:
        prix_float = round(float(prix_brut), 2)
        if prix_float <= 0:
            erreurs['prix'] = 'Le prix doit être supérieur à 0$'
        elif prix_float > 60:
            erreurs['prix'] = 'Un jeu en location ne peut pas valoir plus de 60$'
    except (ValueError, TypeError):
        erreurs['prix'] = 'Le prix du jeu est requis'

    if not photo or not photo.filename:
        erreurs['photo'] = 'La photo du jeu est requise'
    else:
        extension = photo.filename.rsplit('.', 1)[-1].upper()
        if extension not in EXTENSIONS_PERMISES:
            erreurs['photo'] = 'Seuls les fichiers JPG, JPEG, PNG et WEBP sont acceptés'

    if not typeConsole:
        erreurs['typeConsole'] = 'Veuillez choisir le type de console'
    elif typeConsole not in CONSOLES_VALIDES:
        erreurs['typeConsole'] = 'Type de console invalide'

    if not choixPaiement:
        erreurs['choixPaiement'] = 'Veuillez choisir la méthode de paiement désirée'
    elif choixPaiement not in PAIEMENTS_VALIDES:
        erreurs['choixPaiement'] = 'Méthode de paiement invalide'

    if not adresse:
        erreurs['adresse'] = "L'adresse est requise."
    elif len(adresse) < 5:
        erreurs['adresse'] = "L'adresse doit contenir au moins 5 caractères"

    aujourd_hui = datetime.date.today().isoformat()
    if not dateDebut:
        erreurs['dateDebut'] = 'Veuillez entrer une date de début'
    elif dateDebut < aujourd_hui:
        erreurs['dateDebut'] = 'La date de début ne peut pas être dans le passé'

    if not dateFin:
        erreurs['dateFin'] = 'Veuillez entrer une date de fin'
    elif dateDebut and dateFin <= dateDebut:
        erreurs['dateFin'] = 'La date de fin doit être après la date de début'

    if erreurs:
        return jsonify({"erreurs": erreurs}), 400

    nomFichier = photo.filename
    chemin_complet = os.path.join(current_app.config['CHEMIN_VERS_AJOUTS'], nomFichier)
    photo.save(chemin_complet)

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'INSERT INTO locations (NomJeu, Prix, Photo, TypeConsole, TypePaiement, Adresse, DateDebut, DateFin, LocateurId) VALUES (%(NomJeu)s, %(Prix)s,'
                    ' %(Photo)s, %(TypeConsole)s, %(Paiement)s, %(Adresse)s, %(DateDebut)s, %(DateFin)s, %(LocateurId)s)',
                    {
                        'NomJeu' : nomJeu,
                        'Prix' : prix_float,
                        'Photo' : nomFichier,
                        'TypeConsole' : typeConsole,
                        'Paiement' : choixPaiement,
                        'Adresse' : adresse,
                        'DateDebut' : dateDebut,
                        'DateFin' : dateFin,
                        'LocateurId': locateurId
                    }
                )
        return jsonify({"succes": True}), 201

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500

@bp_location.route("/locations", methods=['GET'])
def get_locations():
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('SELECT * FROM locations')
                locations = curseur.fetchall()
        return jsonify(locations), 200

    except mysql.connector.Error as error:
        current_app.logger.exception(error)

# Permet d'afficher les locations d'un vendeur
@bp_location.route("/mesLocations/<int:id_utilisateur>", methods=['GET'])
def mesLocations(id_utilisateur):
    locations = []

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("SELECT l.Id as Id, l.NomJeu, l.Prix, l.Photo, l.TypePaiement, l.Adresse, u.NomUtilisateur," \
                " l.DateDebut, l.DateFin FROM locations l JOIN utilisateurs u ON l.LocateurId = u.Id WHERE u.Id = %(idUtilisateur)s",
                {
                    'idUtilisateur' : id_utilisateur
                })
                locations = curseur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        abort(500)
    return jsonify(locations)

# Permet de sélectionner une vente précise
@bp_location.route("/location/<int:id_location>", methods=['GET'])
def vente(id_location):
    location = None

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("SELECT l.NomJeu, l.Prix, l.Photo, l.TypePaiement, l.Adresse, l.LocateurId," \
                " l.DateDebut, l.DateFin, l.EstLoue, l.TypeConsole, u.NomUtilisateur, l.estDisponible" \
                " FROM locations l JOIN utilisateurs u ON l.LocateurId = u.Id" \
                " WHERE l.Id = %(idLocation)s",
                {
                    'idLocation' : id_location
                })
                location = curseur.fetchone()
    except mysql.connector.Error as err:
        print(err)
        abort(500)
    return jsonify(location)

@bp_location.route("/supprimerLocation/<int:id_location>", methods=['POST'])
def supprimer(id_location):
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('DELETE FROM locations WHERE Id = %(idLocation)s', {'idLocation' : id_location})
        return jsonify({"succes": True}), 200
    except mysql.connector.Error as err:
        current_app.logger.exception(err)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500
    
@bp_location.route("/modifierLocation/<int:id_location>", methods=['POST'])
def modifier(id_location):
    prix_brut = request.form.get("prix", "")
    choixPaiement = request.form.get("choixPaiement", "")
    adresse = (request.form.get("adresse", "")).strip()
    dateDebut = request.form.get("dateDebut", "")
    dateFin = request.form.get("dateFin", "")

    PAIEMENTS_VALIDES = ['En ligne', 'En main propre']

    erreurs = {}
    prix_float = None

    try:
        prix_float = round(float(prix_brut), 2)
        if prix_float <= 0:
            erreurs['prix'] = 'Le prix doit être supérieur à 0$'
        elif prix_float > 60:
            erreurs['prix'] = 'Un jeu en location ne peut pas valoir plus de 60$'
    except (ValueError, TypeError):
        erreurs['prix'] = 'Le prix du jeu est requis'

    if not choixPaiement:
        erreurs['choixPaiement'] = 'Veuillez choisir la méthode de paiement désirée'
    elif choixPaiement not in PAIEMENTS_VALIDES:
        erreurs['choixPaiement'] = 'Méthode de paiement invalide'

    if not adresse:
        erreurs['adresse'] = "L'adresse est requise."
    elif len(adresse) < 5:
        erreurs['adresse'] = "L'adresse doit contenir au moins 5 caractères"

    aujourd_hui = datetime.date.today().isoformat()
    if not dateDebut:
        erreurs['dateDebut'] = 'Veuillez entrer une date de début'
    elif dateDebut < aujourd_hui:
        erreurs['dateDebut'] = 'La date de début ne peut pas être dans le passé'

    if not dateFin:
        erreurs['dateFin'] = 'Veuillez entrer une date de fin'
    elif dateDebut and dateFin <= dateDebut:
        erreurs['dateFin'] = 'La date de fin doit être après la date de début'

    if erreurs:
        return jsonify({"erreurs": erreurs}), 400

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("UPDATE locations SET Prix = %(prix)s, TypePaiement = %(choixPaiement)s" \
                ", Adresse = %(adresse)s, DateDebut = %(dateDebut)s, DateFin = %(dateFin)s WHERE Id = %(idLocation)s",
                {
                    'prix': prix_float,
                    'choixPaiement': choixPaiement,
                    'adresse': adresse,
                    'dateDebut': dateDebut,
                    'dateFin': dateFin,
                    'idLocation': id_location
                })
        return jsonify({"succes": True}), 200

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500
    
