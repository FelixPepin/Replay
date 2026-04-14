from flask import request, Blueprint, abort, jsonify, current_app
import mysql.connector
import bd
import os
from datetime import date, timedelta

bp_reservation = Blueprint('reservation',__name__)


@bp_reservation.route("/reservation/<int:id_location>", methods=['GET'])
def getReservations(id_location):
    reservations = []

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute("SELECT DateDebutReservation, DateFinReservation FROM reservations_locations WHERE " \
                "LocationId = %(id_location)s",
                {
                    'id_location' : id_location
                })
                reservations = curseur.fetchall()
    except mysql.connector.Error as err:
        print(err)
        abort(500)
    return jsonify(reservations)

@bp_reservation.route("/reservation/<int:id_location>", methods=['POST'])
def creerReservation(id_location):
    dateDebut = request.form.get("dateDebut", "")
    dateFin = request.form.get("dateFin", "")
    utilisateurId = request.form.get("locataireId", "")

    if not dateDebut or not dateFin or not utilisateurId:
        return jsonify({"erreurs": {"champs": "Champs manquants"}}), 400

    try:
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    "INSERT INTO reservations_locations (LocationId, UtilisateurId, DateDebutReservation, DateFinReservation) "
                    "VALUES (%(locationId)s, %(utilisateurId)s, %(dateDebut)s, %(dateFin)s)",
                    {
                        'locationId': id_location,
                        'utilisateurId': utilisateurId,
                        'dateDebut': dateDebut,
                        'dateFin': dateFin,
                    }
                )

                # Récupérer la plage de la location
                curseur.execute(
                    "SELECT DateDebut, DateFin FROM locations WHERE Id = %(locationId)s",
                    {'locationId': id_location}
                )
                location = curseur.fetchone()

                # Récupérer toutes les réservations existantes
                curseur.execute(
                    "SELECT DateDebutReservation, DateFinReservation FROM reservations_locations WHERE LocationId = %(locationId)s",
                    {'locationId': id_location}
                )
                reservations = curseur.fetchall()

                # Construire l'ensemble des dates réservées
                dates_reservees = set()
                for r in reservations:
                    d = r['DateDebutReservation']
                    fin_r = r['DateFinReservation']
                    while d <= fin_r:
                        dates_reservees.add(d)
                        d += timedelta(days=1)

                # Vérifier si toutes les dates de la location sont couvertes
                toutes_prises = True
                d = location['DateDebut']
                while d <= location['DateFin']:
                    if d not in dates_reservees:
                        toutes_prises = False
                        break
                    d += timedelta(days=1)

                # EstLoue = 1 dès qu'il existe au moins une réservation
                curseur.execute(
                    "UPDATE locations SET EstLoue = 1 WHERE Id = %(locationId)s",
                    {'locationId': id_location}
                )

                # EstDisponible = 0 seulement si toutes les dates sont prises
                if toutes_prises:
                    curseur.execute(
                        "UPDATE locations SET EstDisponible = 0 WHERE Id = %(locationId)s",
                        {'locationId': id_location}
                    )

        return jsonify({"succes": True}), 201
    except mysql.connector.Error as err:
        print(err)
        abort(500)