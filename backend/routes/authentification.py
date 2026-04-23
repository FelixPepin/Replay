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
    regex_courriel = r'^[\w.\-]+@([\w-]+\.)+[\w-]{2,4}$'
    regex_mdp = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*\-]).{8,}$'

    if email == "":
        erreurs["email"] = "L'adresse courriel est requise"
    elif not re.match(regex_courriel, email):
        erreurs["email"] = "L'adresse courriel doit avoir le format suivant (exemple@exemple.com)"
    if password == "":
        erreurs["password"] = "Le mot de passe est requis"
    elif not re.match(regex_mdp, password):
        erreurs["password"] = "Le mot de passe doit contenir huit caractères, au moins une minuscule, majuscule, un chiffre et un caractère spécial"
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
                current_app.logger.info(f"CRÉATION D'UN COMPTE : Utilisateur ID : {curseur.lastrowid} {email}")
                token = jwt.encode({
                'utilisateur_id': curseur.lastrowid,
                'nomUtilisateur': username,
                'courriel': email,
                'role': 'vendeur',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, current_app.secret_key, algorithm='HS256')
            return jsonify({"token": token}), 200

        return jsonify({"succes": True}), 201

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500


@bp_auth.route("/login", methods=['POST', 'GET'])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                curseur.execute('SELECT Id, NomUtilisateur, MotDePasse, Courriel, Role FROM utilisateurs WHERE courriel = %(courriel)s',
                    {'courriel': email}
                )
                utilisateur = curseur.fetchone()

                if utilisateur:
                    userBytes = password.encode('utf-8')
                    hash_mdp = utilisateur['MotDePasse']
                    if isinstance(hash_mdp, str):
                        hash_mdp = hash_mdp.encode('utf-8')
                        
                    if bcrypt.checkpw(userBytes, hash_mdp):
                        mes_jeux_ids = []
                        if utilisateur['Role'] == 'coach':
                            curseur.execute('SELECT id_jeu FROM coach_jeux WHERE id_utilisateur = %s', (utilisateur['Id'],))
                            mes_jeux_ids = [row['id_jeu'] for row in curseur.fetchall()]

                        token = jwt.encode({
                            'utilisateur_id': utilisateur['Id'],
                            'nomUtilisateur': utilisateur['NomUtilisateur'],
                            'courriel': utilisateur['Courriel'],
                            'role': utilisateur['Role'],
                            'mes_jeux_ids': mes_jeux_ids,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                        }, current_app.secret_key, algorithm='HS256')

                        return jsonify({"token": token}), 200

        return jsonify({"erreurs": {"general": "Courriel ou mot de passe invalide"}}), 401

    except mysql.connector.Error as err:
        current_app.logger.error(f"Erreur DB : {err}")
        abort(500)


    
    
    