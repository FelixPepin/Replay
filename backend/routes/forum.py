from flask import Blueprint, jsonify, request, abort
from werkzeug.utils import secure_filename
import mysql.connector
import bd
import os

bp_forum = Blueprint('forum', __name__)
UPLOAD_FOLDER = 'static/uploads/jeux'

@bp_forum.route("/jeux", methods=['GET'])
def getJeux():
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                curseur.execute('SELECT * FROM jeux')
                jeux = curseur.fetchall()
        return jsonify(jeux), 200
    except mysql.connector.Error:
        abort(500)
        
@bp_forum.route("/jeux", methods=['POST'])
def creerJeu():
    nom = request.form.get('nom', '').strip()
    
    if not nom:
        return jsonify({"erreurs": {"nom": "Le nom est obligatoire"}}), 400

    image_url = None

    if 'image' in request.files:
        fichier = request.files['image']
        if fichier and fichier.filename != '':
            nom_fichier = secure_filename(fichier.filename)
            
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            chemin_complet = os.path.join(UPLOAD_FOLDER, nom_fichier)
            fichier.save(chemin_complet)
            
            image_url = f"/{UPLOAD_FOLDER}/{nom_fichier}"

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                curseur.execute(
                    'INSERT INTO jeux (nom, image) VALUES (%s, %s)',
                    (nom, image_url)
                )
                nouveau_id = curseur.lastrowid
                curseur.execute('SELECT * FROM jeux WHERE id = %s', (nouveau_id,))
                jeu = curseur.fetchone()
            conn.commit()
        return jsonify(jeu), 201
    except mysql.connector.Error:
        abort(500)

@bp_forum.route("/jeux/<int:id>", methods=['DELETE'])
def supprimerJeu(id):
    """Admin seulement — supprime un jeu du forum"""
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute('DELETE FROM jeux WHERE id = %s', (id,))
                if curseur.rowcount == 0:
                    return jsonify({"erreurs": {"serveur": "Jeu introuvable"}}), 404
            conn.commit()
        return jsonify({"succes": True}), 200
    except mysql.connector.Error:
        abort(500)
        
@bp_forum.route("/jeux/<int:jeu_id>/questions", methods=['GET'])
def getQuestionsParJeu(jeu_id):
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                query = """
                    SELECT q.*, u.NomUtilisateur as auteur 
                    FROM questions q
                    JOIN utilisateurs u ON q.idUtilisateur = u.Id
                    WHERE q.idJeu = %s
                    ORDER BY q.dateCreation DESC
                """
                curseur.execute(query, (jeu_id,))
                questions = curseur.fetchall()
        return jsonify(questions), 200
    except mysql.connector.Error:
        abort(500)

@bp_forum.route("/jeux/<int:jeu_id>/questions", methods=['POST'])
def creerQuestion(jeu_id):
    donnees = request.get_json()
    titre = donnees.get('titre', '').strip()
    description = donnees.get('description', '').strip()
    id_utilisateur = donnees.get('idUtilisateur') 

    if not titre or not description:
        return jsonify({"erreurs": {"serveur": "Champs obligatoires"}}), 400

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                curseur.execute(
                    'INSERT INTO questions (titre, description, idJeu, idUtilisateur, dateCreation) VALUES (%s, %s, %s, %s, NOW())',
                    (titre, description, jeu_id, id_utilisateur)
                )
                nouveau_id = curseur.lastrowid
                
                query = """
                    SELECT q.*, u.NomUtilisateur as auteur 
                    FROM questions q
                    JOIN utilisateurs u ON q.idUtilisateur = u.Id
                    WHERE q.id = %s
                """
                curseur.execute(query, (nouveau_id,))
                question = curseur.fetchone()
            conn.commit()
        return jsonify(question), 201
    except mysql.connector.Error as e:
        print(f"Erreur SQL précise : {e}")
        return jsonify({"erreurs": {"serveur": "Erreur lors de l'insertion en base"}}), 500
    
@bp_forum.route("/questions/<int:question_id>", methods=['GET'])
def get_detail_question(question_id):
    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur(dictionary=True) as curseur:
                query = """
                    SELECT q.*, u.NomUtilisateur as auteur 
                    FROM questions q
                    JOIN utilisateurs u ON q.idUtilisateur = u.Id
                    WHERE q.id = %s
                """
                curseur.execute(query, (question_id,))
                question = curseur.fetchone()
        
        if not question:
            return jsonify({"erreur": "Question introuvable"}), 404
            
        return jsonify(question), 200
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500 