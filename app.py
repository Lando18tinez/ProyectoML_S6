from flask import Flask, render_template
from app.routes import bp 
import pandas as pd
#import os


app = Flask(__name__)

app.register_blueprint(bp)  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/negocio")
def negocio():
    return render_template("negocio.html")

@app.route("/ver_datos")
def ver_datos():
    df = pd.read_excel("data/original.xlsx")
    tabla_html = df.head(50).to_html(classes="table table-bordered", index=False)
    return render_template("show_data.html", tabla_original=tabla_html)

# siempre al final del archivo
if __name__ == '__main__':
    app.run(debug=True)