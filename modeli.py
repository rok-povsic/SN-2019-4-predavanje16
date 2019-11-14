import os
from sqla_wrapper import SQLAlchemy


db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///podatkova-baza.sqlite"))


class Komentar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avtor = db.Column(db.String)
    vsebina = db.Column(db.String)
