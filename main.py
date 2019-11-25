import hashlib
import random
import uuid
from flask import Flask, render_template, request, redirect, make_response
from modeli import Komentar, db, Uporabnik

app = Flask(__name__)
db.create_all()


@app.route("/")
def prva_stran():
    sejna_vrednost = request.cookies.get("sejna_vrednost")

    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()
    if uporabnik:
        ime = uporabnik.ime
    else:
        ime = None

    # Preberemo vse komentarje
    komentarji = db.query(Komentar).all()

    return render_template("prva_stran.html", ime=ime, komentarji=komentarji)


@app.route("/kontakt")
def kontakt():
    emaili = ["ime@example.com", "ime@gmail.com", "tretji@email.si"]
    return render_template("kontakt.html", emaili=emaili)


@app.route("/poslji-sporocilo", methods=["POST"])
def poslji_sporocilo():
    zadeva = request.form.get("zadeva")
    sporocilo = request.form.get("sporocilo")

    # Tukaj bi shranili te spremenljivki v bazo.

    return render_template("sporocilo_poslano.html", zadeva=zadeva)


@app.route("/prijava", methods=["POST"])
def prijava():
    ime = request.form.get("ime")
    originalno_geslo = request.form.get("geslo")
    geslo = hashlib.sha256(originalno_geslo.encode()).hexdigest()

    sejna_vrednost = str(uuid.uuid4())

    # Geslo je potrebno šifrirati!

    uporabnik = db.query(Uporabnik).filter_by(ime=ime).first()
    if not uporabnik:
        uporabnik = Uporabnik(ime=ime, email="", geslo=geslo, sejna_vrednost=sejna_vrednost)
    else:
        if geslo == uporabnik.geslo:
            uporabnik.sejna_vrednost = sejna_vrednost
        else:
            return "Napačno geslo"

    db.add(uporabnik)
    db.commit()

    odgovor = make_response(redirect("/"))
    odgovor.set_cookie("sejna_vrednost", sejna_vrednost)
    return odgovor


@app.route("/komentar", methods=["POST"])
def poslji_komentar():
    vsebina_komentarja = request.form.get("vsebina")

    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    # Tukaj se bo komentar shranil v podatkovno bazo

    komentar = Komentar(
        avtor=uporabnik.ime,
        vsebina=vsebina_komentarja
    )
    db.add(komentar)

    db.commit()

    return redirect("/")


@app.route("/skrito-stevilo")
def skrito_stevilo():
    odgovor = make_response(render_template("skrito_stevilo.html"))

    if not request.cookies.get("SkritoStevilo"):
        stevilo = str(random.randint(1, 20))
        odgovor.set_cookie("SkritoStevilo", stevilo)

    return odgovor


@app.route("/poslji-skrito-stevilo", methods=["POST"])
def poslji_skrito_stevilo():
    skrito_stevilo = request.cookies.get("SkritoStevilo")
    vpisano_stevilo = request.form.get("stevilo")

    if skrito_stevilo == vpisano_stevilo:
        return "PRAVILNO"
    else:
        return "NI PRAVILNO"


@app.route("/profil")
def moj_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napačna seja"

    return render_template("profil.html", uporabnik=uporabnik)


@app.route("/profil/uredi", methods=["GET", "POST"])
def uredi_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napačna seja"

    if request.method == "GET":
        return render_template("uredi_profil.html", uporabnik=uporabnik)
    elif request.method == "POST":
        uporabnik.ime = request.form.get("ime")
        uporabnik.email = request.form.get("email")

        db.add(uporabnik)
        db.commit()

        return redirect("/profil")


@app.route("/profil/izbrisi", methods=["GET", "POST"])
def izbrisi_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napačna seja"

    if request.method == "GET":
        return render_template("izbrisi_profil.html")
    elif request.method == "POST":
        db.delete(uporabnik)
        db.commit()

        odgovor = make_response(redirect("/"))
        odgovor.set_cookie("sejna_vrednost", expires=0)
        return odgovor


@app.route("/uporabniki")
def uporabniki():
    users = db.query(Uporabnik).all()
    return render_template("uporabniki.html", uporabniki=users)


@app.route("/uporabniki/<uporabnik_id>")
def prikaz_uporabnika(uporabnik_id):
    uporabnik = db.query(Uporabnik).filter_by(id=uporabnik_id).first()
    return render_template("prikaz_uporabnika.html", uporabnik=uporabnik)


if __name__ == '__main__':
    app.run(debug=True)



