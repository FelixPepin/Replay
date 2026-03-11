from flask import request, Blueprint, abort, jsonify, current_app
import mysql.connector
import bd
import os

bp_location = Blueprint('location',__name__)

# Permet de mettre en location un jeu vidéo
@bp_location.route("/location", methods=['POST'])
def location():
    nomJeu = (request.form.get("nomJeu","")).strip()
    prix = request.form.get("prix","")
    typeConsole = request.form.get("typeConsole","")
    choixPaiement = request.form.get("choixPaiement","")
    adresse = request.form.get("adresse","")
    dateDebut = request.form.get("dateDebut","")
    dateFin = request.form.get("dateFin","")
    locateurId = request.form.get("locateurId","")
    photo = request.files.get("photo","")
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
                        'Prix' : prix,
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