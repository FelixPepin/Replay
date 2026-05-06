from flask import Blueprint, jsonify, request, current_app
import mysql.connector
import bd
import os
import re
from flask.logging import create_logger
import datetime

bp_evaluation = Blueprint('evaluation',__name__)

# Permet de mettre en vente un jeu vidéo
@bp_evaluation.route("/evaluation", methods=['POST'])
def vendre():
    nomJeu = (request.form.get("nomJeu","")).strip()
    vendeurId = request.form.get("vendeurId","")
    evaluateurId = request.form.get("evaluateurId")


    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'INSERT INTO evaluation (IdVendeur, IdEvaluateur, NomJeu) VALUES (%(IdVendeur)s, %(IdEvaluateur)s,'
                    ' %(NomJeu)s)',
                    {
                        'IdVendeur' : vendeurId,
                        'IdEvaluateur' : evaluateurId,
                        'NomJeu' : nomJeu
                    }
                )
        return jsonify({"succes": True}), 201

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500

# Permet de récuperer tous les évaluations d'un utilisateur
@bp_evaluation.route("/mesEvaluations/<int:id_utilisateur>", methods=['GET'])
def mesEvaluations(id_utilisateur):
    mesEvaluations = []

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("SELECT e.Id as Id, e.NomJeu, e.IdVendeur, u.NomUtilisateur" \
                " FROM evaluation e JOIN utilisateurs u ON e.IdEvaluateur = u.Id WHERE u.Id = %(idUtilisateur)s",
                {
                    'idUtilisateur' : id_utilisateur
                })
                mesEvaluations = curseur.fetchall()
    except mysql.connector.Error as err:
        current_app.logger.exception(err)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500
    return jsonify(mesEvaluations)

# Permet de supprimer une évaluation
@bp_evaluation.route("/evaluation/<int:id_evaluation>", methods=['DELETE'])
def supprimer_evaluation(id_evaluation):
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'DELETE FROM evaluation WHERE Id = %(id)s',
                    {'id': id_evaluation}
                )
        return jsonify({"succes": True}), 200

    except mysql.connector.Error as error:
        current_app.logger.exception(error)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500

# Permet de récupérer les infos d'une évaluation précise
@bp_evaluation.route("/evaluer/<int:id_evaluation>", methods=['GET'])
def get_evaluation(id_evaluation):
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    "SELECT e.Id, e.NomJeu, e.IdVendeur, u.NomUtilisateur"
                    " FROM evaluation e JOIN utilisateurs u ON e.IdVendeur = u.Id"
                    " WHERE e.Id = %(id)s",
                    {'id': id_evaluation}
                )
                evaluation = curseur.fetchone()
    except mysql.connector.Error as err:
        current_app.logger.exception(err)
        return jsonify({"erreurs": {"serveur": "Erreur de base de données"}}), 500
    return jsonify(evaluation)