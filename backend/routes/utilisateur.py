from flask import Flask, render_template, request, redirect, make_response, url_for, Blueprint, session, flash, abort, jsonify, current_app
import mysql.connector
import bd
import re
from flask.logging import create_logger
import bcrypt
import jwt
import datetime

bp_users = Blueprint('users',__name__)

@bp_users.route("/users",methods=['POST','GET'])
def getUsers():
    """Permet de récupérer tous les utilisateurs"""
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('SELECT id, nomUtilisateur, courriel, role FROM utilisateurs')
                utilisateurs = curseur.fetchall()
        return jsonify(utilisateurs), 200
    except mysql.connector.Error as err:
        abort(500)

    return jsonify({"erreurs": {"general": "Aucun utilisateur(s) a été trouvé"}}), 401

@bp_users.route("/users/<int:id>/role", methods=['PATCH'])
def updateRole(id):
    """Modifier le rôle d'un utilisateur"""
    donnees = request.get_json()
    role = donnees.get('role')

    roles_valides = ['admin', 'vendeur', 'client', 'coach']
    if role not in roles_valides:
        return jsonify({"erreurs": {"serveur": "Rôle invalide"}}), 400

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'UPDATE utilisateurs SET role = %s WHERE id = %s',
                    (role, id)
                )
                if curseur.rowcount == 0:
                    return jsonify({"erreurs": {"serveur": "Utilisateur introuvable"}}), 404
            conn.commit()
        return jsonify({"succes": True}), 200
    except mysql.connector.Error:
        abort(500)

@bp_users.route("/users/<int:id>/promouvoir-coach", methods=['POST'])
def promouvoir_coach(id):
    """Promouvoir un utilisateur au rôle de coach après un score parfait au quiz"""
    donnees = request.get_json() or {}
    jeu_coach_id = donnees.get('jeuCoachId')

    if not jeu_coach_id:
        return jsonify({"erreurs": {"serveur": "jeuCoachId manquant"}}), 400

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'SELECT Id, NomUtilisateur, Courriel, role FROM utilisateurs WHERE Id = %s',
                    (id,)
                )
                user = curseur.fetchone()
                if user is None:
                    return jsonify({"erreurs": {"serveur": "Utilisateur introuvable"}}), 404
                if user['role'] != 'coach':
                    curseur.execute(
                        'UPDATE utilisateurs SET role = %s WHERE id = %s',
                        ('coach', id)
                    )
            conn.commit()

        token = jwt.encode({
            'utilisateur_id': user['Id'],
            'nomUtilisateur': user['NomUtilisateur'],
            'courriel': user['Courriel'],
            'role': 'coach',
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        }, current_app.secret_key, algorithm='HS256')
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'INSERT INTO coach_jeux (id_utilisateur, id_jeu) VALUES (%(id_utilisateur)s, %(id_jeu)s)',
                    {
                        "id_utilisateur" : id,
                        "id_jeu" : jeu_coach_id
                    }
                )
        return jsonify({"token": token}), 200
    except mysql.connector.Error as err:
        current_app.logger.exception(err)
        abort(500)


@bp_users.route("/evaluer/<int:id_vendeur>", methods=['PUT'])
def noter_evaluation(id_vendeur):
    note = request.json.get('note')

    if note is None or not (0 <= int(note) <= 5):
        return jsonify({"erreurs": {"note": "Note invalide"}}), 400
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'SELECT note, nbEvaluation FROM utilisateurs WHERE Id = %(id_vendeur)s',
                    {'id_vendeur': id_vendeur}
                )
                user = curseur.fetchone()

                if user is None:
                    return jsonify({"erreurs": {"serveur": "Vendeur introuvable"}}), 404

                nouveauNbEvaluation = user['nbEvaluation'] + 1
                nouvelleNote = (user['note'] * user['nbEvaluation'] + int(note)) / nouveauNbEvaluation

                nouveauRole = 'client' if nouveauNbEvaluation > 3 and nouvelleNote < 3 else None

                if nouveauRole:
                    curseur.execute(
                        'UPDATE utilisateurs SET note = %(note)s, nbEvaluation = %(nb)s, role = %(role)s WHERE Id = %(id)s',
                        {'note': round(nouvelleNote, 1), 'nb': nouveauNbEvaluation, 'role': nouveauRole, 'id': id_vendeur}
                    )
                else:
                    curseur.execute(
                        'UPDATE utilisateurs SET note = %(note)s, nbEvaluation = %(nb)s WHERE Id = %(id)s',
                        {'note': round(nouvelleNote, 1), 'nb': nouveauNbEvaluation, 'id': id_vendeur}
                    )
        return jsonify({"succes": True}), 200

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500   
    
    
@bp_users.route("/profil/nom", methods=['PATCH'])
def modifierNom():
    utilisateur = get_utilisateur_connecte()
    id_utilisateur = utilisateur['utilisateur_id']

    donnees = request.get_json()
    nom = donnees.get('nomUtilisateur', '').strip()

    if not nom:
        return jsonify({"erreurs": {"nomUtilisateur": "Le nom est obligatoire"}}), 400

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                curseur.execute(
                    'UPDATE utilisateurs SET nomUtilisateur = %s WHERE id = %s',
                    (nom, id_utilisateur)
                )
                curseur.execute(
                    'SELECT id, nomUtilisateur, courriel, role FROM utilisateurs WHERE id = %s',
                    (id_utilisateur,)
                )
                user = curseur.fetchone()
            conn.commit()

        token = jwt.encode({
            'utilisateur_id': user['id'],
            'nomUtilisateur': user['nomUtilisateur'],
            'courriel': user['courriel'],
            'role': user['role'],
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        }, current_app.secret_key, algorithm='HS256')

        return jsonify({"succes": True, "token": token}), 200
    except mysql.connector.Error:
        abort(500)


@bp_users.route("/profil/motdepasse", methods=['PATCH'])
def modifierMotDePasse():
    utilisateur = get_utilisateur_connecte()
    id_utilisateur = utilisateur['utilisateur_id']

    donnees = request.get_json()
    actuel = donnees.get('actuel', '')
    nouveau = donnees.get('nouveau', '')

    if not actuel or not nouveau:
        return jsonify({"erreurs": {"general": "Champs manquants"}}), 400

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                curseur.execute('SELECT motDePasse FROM utilisateurs WHERE id = %s', (id_utilisateur,))
                user = curseur.fetchone()

                if not bcrypt.checkpw(actuel.encode(), user['motDePasse'].encode()):
                    return jsonify({"erreurs": {"actuel": "Mot de passe actuel incorrect"}}), 400

                hash_nouveau = bcrypt.hashpw(nouveau.encode(), bcrypt.gensalt()).decode()
                curseur.execute(
                    'UPDATE utilisateurs SET motDePasse = %s WHERE id = %s',
                    (hash_nouveau, id_utilisateur)
                )
            conn.commit()
        return jsonify({"succes": True}), 200
    except mysql.connector.Error:
        abort(500)


@bp_users.route("/profil", methods=['DELETE'])
def supprimerCompte():
    utilisateur = get_utilisateur_connecte()
    id_utilisateur = utilisateur['utilisateur_id']

    donnees = request.get_json()
    mot_de_passe = donnees.get('motDePasse', '')

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                curseur.execute('SELECT motDePasse FROM utilisateurs WHERE id = %s', (id_utilisateur,))
                user = curseur.fetchone()

                if not bcrypt.checkpw(mot_de_passe.encode(), user['motDePasse'].encode()):
                    return jsonify({"erreurs": {"motDePasse": "Mot de passe incorrect"}}), 400

                curseur.execute('DELETE FROM utilisateurs WHERE id = %s', (id_utilisateur,))
            conn.commit()
        return jsonify({"succes": True}), 200
    except mysql.connector.Error:
        abort(500)
        
def get_utilisateur_connecte():
    """Décode le token JWT et retourne le payload"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        abort(401)
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        abort(401)
    except jwt.InvalidTokenError:
        abort(401)