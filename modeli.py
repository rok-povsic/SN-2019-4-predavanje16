import os
from sqla_wrapper import SQLAlchemy


db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///podatkova-baza.sqlite?check_same_thread=False"))


class Komentar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avtor = db.Column(db.String)
    vsebina = db.Column(db.String)


class Uporabnik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String)
    email = db.Column(db.String)
    geslo = db.Column(db.String)
    sejna_vrednost = db.Column(db.String)
    je_blokiran = db.Column(db.Boolean, default=False)
