from flask import Flask, render_template
#import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/negocio")
def negocio():
    return render_template("negocio.html")

# siempre al final del archivo
if __name__ == '__main__':
    app.run(debug=True)