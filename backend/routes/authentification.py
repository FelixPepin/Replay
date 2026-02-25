from flask import Flask, render_template, request, redirect, make_response, url_for, Blueprint, session, flash, abort, jsonify, current_app
import mysql.connector
import bd
import re
from flask.logging import create_logger
import bcrypt
import jwt
import datetime

bp_auth = Blueprint('auth',__name__)

@bp_auth.route("/register", methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    confirm = data.get("confirm", "")

    erreurs = {}

    if username == "":
        erreurs["username"] = "Le nom d'utilisateur est requis"
    if email == "":
        erreurs["email"] = "L'adresse courriel est requise"
    if password == "":
        erreurs["password"] = "Le mot de passe est requis"
    if password != confirm:
        erreurs["confirm"] = "Les deux mots de passe doivent correspondre"

    if erreurs:
        return jsonify({"erreurs": erreurs}), 400
    
    with bd.creer_connexion() as conn:
        with conn.get_curseur() as curseur:
            curseur.execute(
                'SELECT Id FROM utilisateurs WHERE Courriel = %(courriel)s',
                {'courriel': email}
            )
            existant = curseur.fetchone()

    if existant:
        return jsonify({"erreurs": {"email": "Cette adresse courriel est déjà utilisée"}}), 400
    

    try:
        salt = bcrypt.gensalt()
        motDePasseHashed = bcrypt.hashpw(password.encode('utf-8'), salt)

        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'INSERT INTO utilisateurs (NomUtilisateur, MotDePasse, Courriel, Role) VALUES (%(nom_utilisateur)s, %(mdp_hache)s, %(courriel)s,%(role)s)',
                    {
                        'nom_utilisateur': username,
                        'mdp_hache': motDePasseHashed,
                        'courriel': email,
                        'role' : 'vendeur'
                    }
                )

                # session['utilisateur_id'] = curseur.lastrowid
                # session['courriel'] = email

                current_app.logger.info(f"CRÉATION D'UN COMPTE : Utilisateur ID : {curseur.lastrowid} {email}")

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
                'role': utilisateur['Role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, current_app.secret_key, algorithm='HS256')
            # current_app.logger.info(f"CONNEXION D'UN COMPTE : Utilisateur ID : {curseur.lastrowid} {email}")
            # return jsonify({"succes": True}), 201
            return jsonify({"token": token}), 200
        return jsonify({"erreurs": {"general": "Courriel ou mot de passe invalide"}}), 401


    
    
    