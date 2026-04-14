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

    roles_valides = ['admin', 'vendeur', 'client']
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
    
    
    