from flask import Flask, render_template, request, redirect, make_response, url_for, Blueprint, session, flash, abort, jsonify, current_app
import mysql.connector
import bd
import re
from flask.logging import create_logger
import datetime

bp_auth = Blueprint('vente',__name__)

@bp_auth.route("/vente", methods=['POST'])
def register():
    data = request.get_json()

    nomJeu = data.get("nomJeu", "").strip()
    prix = data.get("prix", "").strip()
    photo = data.get("photo", "")
    choixPaiement = data.get("choixPaiement", "")
    choixLivraison = data.get("choixLivraison", "")
    adresse = data.get("adresse", "")

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'INSERT INTO ventes (NomJeu, Prix, Photo, TypePaiement, TypeLivraison, Adresse, VendeurId) VALUES (%(NomJeu)s, %(Prix)s,'
                    ' %(Photo)s, %(Paiement)s, %(Livraison)s, %(adresse)s)',
                    {
                        'NomJeu' : nomJeu,
                        'Prix' : prix,
                        'Photo' : photo,
                        'TypePaiement' : choixPaiement,
                        'TypeLivraison' : choixLivraison,
                        'Adresse' : adresse
                    }
                )

                current_app.logger.info(f"CRÉATION D'UNE VENTE POUR LE JEU SUIVANT : {curseur.lastrowid} {nomJeu}")

        return jsonify({"succes": True}), 201

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500


@bp_auth.route("/login",methods=['POST','GET'])
def login():
    """Permet la connexion d'un compte utilisateur valide"""
    
    data = request.get_json()
    
    email = data.get("email","").strip()
    password = data.get("password", "")
    
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('SELECT Id, NomUtilisateur, MotDePasse, Courriel FROM utilisateurs WHERE courriel = %(courriel)s',
                    {
                            'courriel' : email
                    }
                                    
                )
                utilisateur = curseur.fetchone()
    except mysql.connector.Error as err:
            abort(500)
            
    if (utilisateur):
        userBytes = password.encode('utf-8')
        hash = utilisateur['MotDePasse'].encode('utf-8')
        result  = bcrypt.checkpw(userBytes,hash)
        
        if (result):
            token = jwt.encode({
                'utilisateur_id': utilisateur['Id'],
                'courriel': utilisateur['Courriel'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, current_app.secret_key, algorithm='HS256')
            # current_app.logger.info(f"CONNEXION D'UN COMPTE : Utilisateur ID : {curseur.lastrowid} {email}")
            # return jsonify({"succes": True}), 201
            return jsonify({"token": token}), 200
        return jsonify({"erreurs": {"general": "Courriel ou mot de passe invalide"}}), 401


    
    
    