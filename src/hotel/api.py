from flask import Blueprint, request, jsonify
from .database import db
from .models import Client, Chambre, Reservation
from datetime import datetime


def isReserve(date_depart, date_arrivee, chambre, reservations):
    for reservation in reservations:
        chambre_id = chambre.id
        res_chambre_id = reservation.id_chambre
        if chambre_id != res_chambre_id:
            continue
        res_date_arrivee = datetime.strptime(reservation.date_arrivee, '%Y-%m-%d').date()
        res_date_depart = datetime.strptime(reservation.date_depart, '%Y-%m-%d').date()
        date_depart = datetime.strptime(date_depart, '%Y-%m-%d').date()
        date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d').date()
        if date_arrivee >= res_date_arrivee and date_arrivee <= res_date_depart:
            return True
        if date_depart >= res_date_arrivee and date_depart <= res_date_depart:
            return True
    return False




api = Blueprint('api', __name__)

@api.route("/new_client", methods=['POST'])
def add_client():
    nom = request.json['nom']
    email = request.json['email']


    new_client = Client(
        nom = nom,
        email = email
        )

    db.session.add(new_client)
    db.session.commit()
    client = Client.query.get(new_client.id)

    return jsonify(
        id = client.id,
        nom = client.nom,
        email = client.email
        )

@api.route('/api/chambres', methods=['POST'])
def add_chambre():
    numero = request.json['numero']
    type = request.json['type']
    prix = request.json['prix']

    new_chambre = Chambre(
        numero = numero,
        type = type,
        prix = prix
    )
    db.session.add(new_chambre)
    db.session.commit()

    return jsonify(
        success =  True, 
	    message = "Chambre ajoutée avec succès."
    )

@api.route('/api/chambres/<int:id>', methods=['PUT'])
def change_chambre(id):

    json = request.get_json()

    chambre = Chambre.query.get_or_404(id)
    
    if 'numero' in json:
        chambre.numero = json["numero"]
    if 'type' in json:
        chambre.type = json["type"]
    if 'prix' in json:
        chambre.prix = json["prix"]
    
    db.session.commit()
    return jsonify(
        success =  True, 
	    message = "Chambre Modifier avec succès."
    )

@api.route('/api/chambres/<int:id>', methods=['DELETE'])
def delete_chambre(id):

    chambre = Chambre.query.get_or_404(id)

    db.session.delete(chambre)
    db.session.commit()

    return jsonify(
        success =  True, 
	    message = "Chambre suprimer avec succès."
    )

@api.route('/api/reservations', methods=['POST'])
def new_reservation():
    id_client = request.json['id_client']
    id_chambre = request.json['id_chambre']
    date_arrivee = request.json['date_arrivee']
    date_depart = request.json['date_depart']

    chambre = Chambre.query.get_or_404(id_chambre)
    client = Client.query.get_or_404(id_client)
    arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d').date()
    depart = datetime.strptime(date_depart, '%Y-%m-%d').date()
    if arrivee >= depart: 
        return jsonify(
        success =  False, 
	    message = "La date d'arrivée superieur ou egal a la date de départ !!!!"
    )


    new_reservation = Reservation(
        client = client,
        chambre = chambre,
        date_arrivee = date_arrivee,
        date_depart = date_depart
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify(
        success =  True, 
	    message = "Réservation créée avec succès."
    )

@api.route('/api/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)

    db.session.delete(reservation)

    db.session.commit()

    return jsonify(
        success =  True, 
	    message = "Réservation annulée avec succès."
    )

@api.route('/api/chambres/disponibles', methods=['GET'])
def chambre_disponibles():
    results = []
    date_arrivee = request.json['date_arrivee']
    date_depart = request.json['date_depart']

    chambres = Chambre.query.all()
    reservations = Reservation.query.all()

    for chambre in chambres:
        if isReserve(date_depart,date_arrivee,chambre,reservations):
            continue
        results.append(chambre)
    return jsonify(results)

