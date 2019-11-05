from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def prva_stran():
    return render_template("prva_stran.html")


@app.route("/kontakt")
def kontakt():
    emaili = ["ime@example.com", "ime@gmail.com", "tretji@email.si"]
    return render_template("kontakt.html", emaili=emaili)


if __name__ == '__main__':
    app.run()
