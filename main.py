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
    geslo = request.form.get("geslo")

    sejna_vrednost = str(uuid.uuid4())

    # Geslo je potrebno šifrirati!

    uporabnik = db.query(Uporabnik).filter_by(ime=ime).first()
    if not uporabnik:
        uporabnik = Uporabnik(ime=ime, geslo=geslo, sejna_vrednost=sejna_vrednost)
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


if __name__ == '__main__':
    app.run(debug=True)



