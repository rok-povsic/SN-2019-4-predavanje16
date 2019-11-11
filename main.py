from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)


@app.route("/")
def prva_stran():
    ime = request.cookies.get("ime")

    return render_template("prva_stran.html", ime=ime)


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

    odgovor = make_response(redirect("/"))
    odgovor.set_cookie("ime", ime)
    return odgovor


@app.route("/komentar", methods=["POST"])
def poslji_komentar():
    vsebina_komentarja = request.form.get("vsebina")

    # Tukaj se bo komentar shranil v podatkovno bazo

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)



