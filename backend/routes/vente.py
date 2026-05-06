from flask import Flask, render_template, request, redirect, make_response, url_for, Blueprint, session, flash, abort, jsonify, current_app
import mysql.connector
import bd
import os
import re
from flask.logging import create_logger
import datetime

bp_vente = Blueprint('vente',__name__)

# Permet de mettre en vente un jeu vidéo
@bp_vente.route("/vendre", methods=['POST'])
def vendre():
    nomJeu = (request.form.get("nomJeu", "")).strip()
    prix_brut = request.form.get("prix", "")
    typeConsole = request.form.get("typeConsole", "")
    choixPaiement = request.form.get("choixPaiement", "")
    choixLivraison = request.form.get("choixLivraison", "")
    adresse = (request.form.get("adresse", "")).strip()
    vendeurId = request.form.get("vendeurId", "")
    photo = request.files.get("photo")

    CONSOLES_VALIDES = ['PS5', 'PS4', 'PS3', 'Xbox Series X', 'Xbox One', 'Xbox 360',
                        'Nintendo Switch 2', 'Nintendo Switch', 'Wii U', 'Wii']
    PAIEMENTS_VALIDES = ['En ligne', 'En main propre']
    LIVRAISONS_VALIDES = ['Par la poste', 'En main propre']
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
            erreurs['prix'] = 'Un jeu en revente ne peut pas valoir plus de 60$'
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

    if not choixLivraison:
        erreurs['choixLivraison'] = 'Veuillez choisir la méthode de livraison désirée'
    elif choixLivraison not in LIVRAISONS_VALIDES:
        erreurs['choixLivraison'] = 'Méthode de livraison invalide'
    elif choixLivraison == 'En main propre' and not adresse:
        erreurs['adresse'] = "L'adresse est requise lorsque la méthode de livraison est en main propre."

    if erreurs:
        return jsonify({"erreurs": erreurs}), 400

    nomFichier = photo.filename
    chemin_complet = os.path.join(current_app.config['CHEMIN_VERS_AJOUTS'], nomFichier)
    photo.save(chemin_complet)

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'INSERT INTO ventes (NomJeu, Prix, Photo, TypeConsole, TypePaiement, TypeLivraison, Adresse, VendeurId) VALUES (%(NomJeu)s, %(Prix)s,'
                    ' %(Photo)s, %(TypeConsole)s, %(Paiement)s, %(Livraison)s, %(Adresse)s, %(VendeurId)s)',
                    {
                        'NomJeu': nomJeu,
                        'Prix': prix_float,
                        'Photo': nomFichier,
                        'TypeConsole': typeConsole,
                        'Paiement': choixPaiement,
                        'Livraison': choixLivraison,
                        'Adresse': adresse,
                        'VendeurId': vendeurId
                    }
                )
        return jsonify({"succes": True}), 201

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500

# Permet de récuperer tous les ventens d'un utilisateur
@bp_vente.route("/mesVentes/<int:id_utilisateur>", methods=['GET'])
def mesVentes(id_utilisateur):
    ventes = []

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("SELECT v.Id as Id, v.NomJeu, v.Prix, v.Photo, v.TypePaiement, v.TypeLivraison, v.Adresse, u.NomUtilisateur" \
                " FROM ventes v JOIN utilisateurs u ON v.VendeurId = u.Id WHERE u.Id = %(idUtilisateur)s",
                {
                    'idUtilisateur' : id_utilisateur
                })
                ventes = curseur.fetchall()
    except mysql.connector.Error as err:
        current_app.logger.exception(err)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500
    return jsonify(ventes)
# Permet de sélectionner une vente précise
@bp_vente.route("/vente/<int:id_vente>", methods=['GET'])
def vente(id_vente):
    vente = None

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("SELECT NomJeu, Prix, Photo, TypePaiement, TypeLivraison, Adresse, VendeurId,TypeConsole, estVendu FROM ventes" \
                " WHERE Id = %(idVente)s",
                {
                    'idVente' : id_vente
                })
                vente = curseur.fetchone()
    except mysql.connector.Error as err:
        current_app.logger.exception(err)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500
    return jsonify(vente)

@bp_vente.route("/modifier/<int:idVente>", methods=['POST'])
def modifier(idVente):
    prix_brut = request.form.get("prix", "")
    choixPaiement = request.form.get("choixPaiement", "")
    choixLivraison = request.form.get("choixLivraison", "")
    adresse = (request.form.get("adresse", "")).strip()

    PAIEMENTS_VALIDES = ['En ligne', 'En main propre']
    LIVRAISONS_VALIDES = ['Par la poste', 'En main propre']

    erreurs = {}
    prix_float = None

    try:
        prix_float = round(float(prix_brut), 2)
        if prix_float <= 0:
            erreurs['prix'] = 'Le prix doit être supérieur à 0$'
        elif prix_float > 60:
            erreurs['prix'] = 'Un jeu en revente ne peut pas valoir plus de 60$'
    except (ValueError, TypeError):
        erreurs['prix'] = 'Le prix du jeu est requis'

    if not choixPaiement:
        erreurs['choixPaiement'] = 'Veuillez choisir la méthode de paiement désirée'
    elif choixPaiement not in PAIEMENTS_VALIDES:
        erreurs['choixPaiement'] = 'Méthode de paiement invalide'

    if not choixLivraison:
        erreurs['choixLivraison'] = 'Veuillez choisir la méthode de livraison désirée'
    elif choixLivraison not in LIVRAISONS_VALIDES:
        erreurs['choixLivraison'] = 'Méthode de livraison invalide'
    elif choixLivraison == 'En main propre' and not adresse:
        erreurs['adresse'] = "L'adresse est requise lorsque la méthode de livraison est en main propre."

    if erreurs:
        return jsonify({"erreurs": erreurs}), 400

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("UPDATE ventes SET Prix = %(prix)s, TypePaiement = %(choixPaiement)s, TypeLivraison = %(choixLivraison)s" \
                ", Adresse = %(adresse)s WHERE Id = %(idVente)s",
                {
                    'prix' : prix_float,
                    'choixPaiement': choixPaiement,
                    'choixLivraison': choixLivraison,
                    'adresse': adresse,
                    'idVente': idVente
                })
            return jsonify({"succes": True}), 200

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500
    
@bp_vente.route("/supprimerVente/<int:idVente>", methods=['POST'])
def supprimer(idVente):
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('DELETE FROM ventes WHERE Id = %(idVente)s', {'idVente' : idVente})
        return jsonify({"succes": True}), 200
    except mysql.connector.Error as err:
        current_app.logger.exception(err)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500

@bp_vente.route("/ventes", methods=['GET'])
def getVentes():
    ventes = []
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('SELECT v.Id, v.NomJeu, v.Prix, v.Photo, v.TypePaiement, v.TypeLivraison, v.Adresse, v.VendeurId, v.TypeConsole,v.estVendu, u.NomUtilisateur FROM ventes v JOIN utilisateurs u ON v.VendeurId = u.Id')
                ventes = curseur.fetchall()                    
        return jsonify(ventes), 200
    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500


@bp_vente.route("/vente/<int:id_vente>/acheter", methods=['POST'])
def acheterVente(id_vente):
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('UPDATE ventes SET estVendu = 1 WHERE Id = %s', (id_vente,))
            conn.commit
        return jsonify({"succes": True}), 200
    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreur": "Erreur serveur"}), 500