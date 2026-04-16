import os
import stripe
import bd
import mysql.connector
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, date

bp_paiement = Blueprint('paiement', __name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")


@bp_paiement.route("/paiement/checkout-achat", methods=['POST'])
def checkout_achat():
    data = request.get_json()
    vente_id = data.get("vente_id")
    acheteur_id = data.get("acheteur_id")
    nom_jeu = data.get("nom_jeu")
    prix = data.get("prix")  # en dollars

    if not all([vente_id, acheteur_id, nom_jeu, prix]):
        return jsonify({"erreur": "Données manquantes"}), 400

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "cad",
                        "product_data": {
                            "name": nom_jeu,
                            "description": "Achat de jeu vidéo",
                        },
                        "unit_amount": int(float(prix) * 100),  # Stripe utilise les centimes
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            metadata={
                "type": "achat",
                "vente_id": str(vente_id),
                "acheteur_id": str(acheteur_id),
            },
            success_url=f"{FRONTEND_URL}/paiement/succes?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/acheter/{vente_id}",
        )
        return jsonify({"url": session.url}), 200
    except stripe.error.StripeError as e:
        current_app.logger.exception(e)
        return jsonify({"erreur": "Erreur Stripe"}), 500


@bp_paiement.route("/paiement/checkout-location", methods=['POST'])
def checkout_location():
    data = request.get_json()
    location_id = data.get("location_id")
    locataire_id = data.get("locataire_id")
    nom_jeu = data.get("nom_jeu")
    prix_par_jour = data.get("prix_par_jour")
    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")

    if not all([location_id, locataire_id, nom_jeu, prix_par_jour, date_debut, date_fin]):
        return jsonify({"erreur": "Données manquantes"}), 400

    debut = date.fromisoformat(date_debut)
    fin = date.fromisoformat(date_fin)
    nb_jours = (fin - debut).days + 1
    prix_total = float(prix_par_jour) * nb_jours

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "cad",
                        "product_data": {
                            "name": f"{nom_jeu} — Location {nb_jours} jour(s)",
                            "description": f"Du {date_debut} au {date_fin}",
                        },
                        "unit_amount": int(prix_total * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            metadata={
                "type": "location",
                "location_id": str(location_id),
                "locataire_id": str(locataire_id),
                "date_debut": date_debut,
                "date_fin": date_fin,
            },
            success_url=f"{FRONTEND_URL}/paiement/succes?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/louer/{location_id}",
        )
        return jsonify({"url": session.url}), 200
    except stripe.error.StripeError as e:
        current_app.logger.exception(e)
        return jsonify({"erreur": "Erreur Stripe"}), 500


@bp_paiement.route("/paiement/confirmer", methods=['GET'])
def confirmer_paiement():
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"erreur": "session_id manquant"}), 400

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError as e:
        current_app.logger.exception(e)
        return jsonify({"erreur": "Session Stripe invalide"}), 400

    if session.payment_status != "paid":
        return jsonify({"erreur": "Paiement non complété"}), 402

    meta = session.metadata._data
    type_paiement = meta.get("type")

    try:
        if type_paiement == "achat":
            vente_id = int(meta["vente_id"])
            acheteur_id = int(meta["acheteur_id"])
            with bd.creer_connexion() as conn:
                with conn.get_curseur() as curseur:
                    curseur.execute(
                        "UPDATE ventes SET estVendu = 1 WHERE Id = %s", (vente_id,)
                    )
                with conn.get_curseur() as curseur:
                    curseur.execute(
                        "SELECT NomJeu, VendeurId FROM ventes WHERE Id = %s", (vente_id,)
                    )
                    vente = curseur.fetchone()
            return jsonify({
                "succes": True,
                "type": "achat",
                "nomJeu": vente["NomJeu"],
                "vendeurId": vente["VendeurId"],
                "evaluateurId": acheteur_id,
            }), 200

        elif type_paiement == "location":
            location_id = int(meta["location_id"])
            locataire_id = int(meta["locataire_id"])
            date_debut = meta["date_debut"]
            date_fin = meta["date_fin"]
            with bd.creer_connexion() as conn:
                with conn.get_curseur() as curseur:
                    curseur.execute(
                        "INSERT INTO reservations_locations (LocationId, UtilisateurId, DateDebutReservation, DateFinReservation)"
                        " VALUES (%s, %s, %s, %s)",
                        (location_id, locataire_id, date_debut, date_fin),
                    )
                    curseur.execute(
                        "UPDATE locations SET EstLoue = 1 WHERE Id = %s", (location_id,)
                    )
                with conn.get_curseur() as curseur:
                    curseur.execute(
                        "SELECT NomJeu, LocateurId FROM locations WHERE Id = %s", (location_id,)
                    )
                    location = curseur.fetchone()
            return jsonify({
                "succes": True,
                "type": "location",
                "nomJeu": location["NomJeu"],
                "vendeurId": location["LocateurId"],
                "evaluateurId": locataire_id,
            }), 200

        else:
            return jsonify({"erreur": "Type de paiement inconnu"}), 400

    except mysql.connector.Error as e:
        current_app.logger.exception(e)
        return jsonify({"erreur": "Erreur base de données"}), 500
