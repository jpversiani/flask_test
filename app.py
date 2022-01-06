import math
import time
from datetime import datetime
import os
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resource={r"/*":{"origins":"*"}})

@app.route("/", methods = ["GET","POST"])
def index():
    variavel = "Digite o número de dígitos de PI a serem cálculados:"
    if request.method == "GET":
        return render_template("index.html",variavel=variavel)
    else:
        start = time.time()
        i = int(request.form.get("name"))
        pi = pi_chudnovsky_bs(i)
        end = time.time()
        tr = end - start    
        return "<!DOCTYPE html>\n <html lang='en'>\n <head>\n <meta charset='UTF8'>\n <meta name='viewport' content='width=device-width', initial-scale=1.0'>\n <title>Document</title>\n </head>\n <body>\n <p>O valor de PI calculado é: </p>\n <p>"+str(pi)+"</p>\n <p>e o tempo de execucao do calculo é de: "+str(tr)+" segundos</p>"

@app.route("/sobre")
def sobre():
    return "<h1>Sobre</h1>"

def sqrt(n, one):
    """
    Return the square root of n as a fixed point number with the one
    passed in.  It uses a second order Newton-Raphson convgence.  This
    doubles the number of significant figures on each iteration.
    """
    # Use floating point arithmetic to make an initial guess
    floating_point_precision = 10**16
    n_float = float((n * floating_point_precision) // one) / floating_point_precision
    x = (int(floating_point_precision * math.sqrt(n_float)) * one) // floating_point_precision
    n_one = n * one
    while 1:
        x_old = x
        x = (x + n_one // x) // 2
        if x == x_old:
            break
    return x

"""
Python3 program to calculate Pi using python long integers, binary
splitting and the Chudnovsky algorithm

See: http://www.craig-wood.com/nick/articles/pi-chudnovsky/ for more
info

Nick Craig-Wood <nick@craig-wood.com>
"""

def pi_chudnovsky_bs(digits):
    """
    Compute int(pi * 10**digits)

    This is done using Chudnovsky's series with binary splitting
    """
    C = 640320
    C3_OVER_24 = C**3 // 24
    def bs(a, b):
        """
        Computes the terms for binary splitting the Chudnovsky infinite series

        a(a) = +/- (13591409 + 545140134*a)
        p(a) = (6*a-5)*(2*a-1)*(6*a-1)
        b(a) = 1
        q(a) = a*a*a*C3_OVER_24

        returns P(a,b), Q(a,b) and T(a,b)
        """
        if b - a == 1:
            # Directly compute P(a,a+1), Q(a,a+1) and T(a,a+1)
            if a == 0:
                Pab = Qab = 1
            else:
                Pab = (6*a-5)*(2*a-1)*(6*a-1)
                Qab = a*a*a*C3_OVER_24
            Tab = Pab * (13591409 + 545140134*a) # a(a) * p(a)
            if a & 1:
                Tab = -Tab
        else:
            # Recursively compute P(a,b), Q(a,b) and T(a,b)
            # m is the midpoint of a and b
            m = (a + b) // 2
            # Recursively calculate P(a,m), Q(a,m) and T(a,m)
            Pam, Qam, Tam = bs(a, m)
            # Recursively calculate P(m,b), Q(m,b) and T(m,b)
            Pmb, Qmb, Tmb = bs(m, b)
            # Now combine
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
        return Pab, Qab, Tab
    # how many terms to compute
    DIGITS_PER_TERM = math.log10(C3_OVER_24/6/2/6)
    N = int(digits/DIGITS_PER_TERM + 1)
    # Calclate P(0,N) and Q(0,N)
    P, Q, T = bs(0, N)
    one = 10**digits
    sqrtC = sqrt(10005*one, one)
    return (Q*426880*sqrtC) // T

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()