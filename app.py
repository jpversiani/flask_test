from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def index():
    variavel = "Game: Adivinhe o game correto"
    if request.method == "GET":
        return render_template("index.html",variavel=variavel)
    else:
        numero = 0
        palpite = int(request.form.get("name"))
        if numero == palpite:
            return "<h1>Resultado: Voce ganhou!</h1>"
        else:
            return "<h1>Resultado: Voce perdeu...</h1>"    

@app.route("/sobre")
def sobre():
    return "<h1>Sobre</h1>"