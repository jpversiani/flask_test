import time
from datetime import datetime
import os
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resource={r"/*":{"origins":"*"}})

@app.route("/", methods = ["GET","POST"])
def index():
    variavel = "Digite o numero de iteracoes para o calculo de PI:"
    if request.method == "GET":
        return render_template("index.html",variavel=variavel)
    else:
        start = time.time()
        i = int(request.form.get("name"))
        k = 1
        s = 0
        for i in range(i): 
            if i % 2 == 0: 
                s += 4/k 
            else: 
                s -= 4/k
            k += 2
        end = time.time()
        tr = end - start    
        return "<h1>O valor de PI calculado é: "+str(s)+"\n e o tempo de execucao do calculo é de: "+str(tr)+" segundos</h1>"
@app.route("/sobre")
def sobre():
    return "<h1>Sobre</h1>"

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()