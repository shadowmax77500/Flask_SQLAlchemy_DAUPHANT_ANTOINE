from .database import db

class Client(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nom = db.Column(db.String(100), nullable = False)
  email = db.Column(db.String(100), nullable = False, unique = True)
  reservations = db.relationship('Reservation', backref='client', lazy='dynamic')

class Chambre(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  numero = db.Column(db.Integer, nullable = False, unique = True)
  type = db.Column(db.String(100), nullable = False)
  prix = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  reservations = db.relationship('Reservation', backref='chambre', lazy='dynamic')

class Reservation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  id_client = db.Column(db.Integer, db.ForeignKey('client.id'))
  id_chambre = db.Column(db.Integer, db.ForeignKey('chambre.id'))
  date_arrivee = db.Column(db.Date, nullable=False)
  date_depart = db.Column(db.Date, nullable=False)
  statut = db.Column(db.String(100), default='En cours')


