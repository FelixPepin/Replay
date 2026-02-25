from flask import Flask, render_template, request, redirect, make_response, url_for, Blueprint, session, flash, abort, jsonify, current_app
import mysql.connector
import bd
import os
import re
from flask.logging import create_logger
import datetime

bp_vente = Blueprint('vente',__name__)

@bp_vente.route("/vendre", methods=['POST'])
def register():
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

                current_app.logger.info(f"CRÉATION D'UNE VENTE POUR LE JEU SUIVANT : {curseur.lastrowid} {nomJeu}")

        return jsonify({"succes": True}), 201

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500