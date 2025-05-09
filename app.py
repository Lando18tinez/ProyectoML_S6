from flask import Flask, render_template
#import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/negocio")
def negocio():
    return render_template("negocio.html")

@app.route("/ingDatos")
def ingDatos():
    return render_template("ingDatos.html")

@app.route("/ingModelo")
def ingModelo():
    return render_template("ingModelo.html")

@app.route("/evaluacionModelo")
def evaluacionModelo():
    return render_template("evaluacionModelo.html") 

# siempre al final del archivo
if __name__ == '__main__':
    app.run(debug=True)