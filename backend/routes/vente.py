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
    nomJeu = (request.form.get("nomJeu","")).strip()
    prix = request.form.get("prix","")
    
    choixPaiement = request.form.get("choixPaiement","")
    choixLivraison = request.form.get("choixLivraison","")
    adresse = request.form.get("adresse","")
    vendeurId = request.form.get("vendeurId","")
    photo = request.files.get("photo","")
    nomFichier = photo.filename

    chemin_complet = os.path.join(current_app.config['CHEMIN_VERS_AJOUTS'], nomFichier)
    photo.save(chemin_complet)

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'INSERT INTO ventes (NomJeu, Prix, Photo, TypePaiement, TypeLivraison, Adresse, VendeurId) VALUES (%(NomJeu)s, %(Prix)s,'
                    ' %(Photo)s, %(Paiement)s, %(Livraison)s, %(Adresse)s, %(VendeurId)s)',
                    {
                        'NomJeu' : nomJeu,
                        'Prix' : prix,
                        'Photo' : nomFichier,
                        'Paiement' : choixPaiement,
                        'Livraison' : choixLivraison,
                        'Adresse' : adresse,
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
        print(err)
        abort(500)
    return jsonify(ventes)
# Permet de sélectionner une vente précise
@bp_vente.route("/vente/<int:id_vente>", methods=['GET'])
def vente(id_vente):
    vente = None

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("SELECT NomJeu, Prix, Photo, TypePaiement, TypeLivraison, Adresse, VendeurId FROM ventes" \
                " WHERE Id = %(idVente)s",
                {
                    'idVente' : id_vente
                })
                vente = curseur.fetchone()
    except mysql.connector.Error as err:
        print(err)
        abort(500)
    return jsonify(vente)

@bp_vente.route("/modifier/<int:idVente>", methods=['POST'])
def modifier(idVente):
    prix = request.form.get("prix","")
    choixPaiement = request.form.get("choixPaiement","")
    choixLivraison = request.form.get("choixLivraison","")
    adresse = request.form.get("adresse","")

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("UPDATE ventes SET Prix = %(prix)s, TypePaiement = %(choixPaiement)s, TypeLivraison = %(choixLivraison)s" \
                ", Adresse = %(adresse)s WHERE Id = %(idVente)s",
                {
                    'prix' : prix,
                    'choixPaiement': choixPaiement,
                    'choixLivraison': choixLivraison,
                    'adresse': adresse,
                    'idVente': idVente
                })
            return jsonify({"succes": True}), 200

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500