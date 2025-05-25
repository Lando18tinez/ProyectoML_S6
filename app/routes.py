from flask import Blueprint, render_template, send_file
from app.utils import cargar_datos, limpiar_datos, calcular_riesgo, resaltar_riesgo
from io import BytesIO
import pandas as pd
import os
from app.model import entrenar_modelo



bp = Blueprint('main', __name__)

@bp.route('/ver_datos')
def ver_datos():
    df_original = cargar_datos("data/original.xlsx")
    df_limpio = limpiar_datos(df_original.copy())
    df_procesado = calcular_riesgo(df_limpio)

    tabla_original = df_original.head(50).to_html(classes="table table-bordered", index=False)
    tabla_procesado = resaltar_riesgo(df_procesado.head(50)).to_html(index=False)
  
    return render_template("show_data.html", tabla_original=tabla_original, tabla_procesado=tabla_procesado)

@bp.route('/ingDatos')
def ingenieria_datos():
    df_original = cargar_datos('data/original.xlsx')
    df_procesado = calcular_riesgo(limpiar_datos(df_original.copy()))

    tabla_original = df_original.head(50).to_html(classes='table table-bordered', index=True)
    tabla_procesado = resaltar_riesgo(df_procesado.head(50)).to_html(index=True)


    return render_template('ingDatos.html',
                           tabla_original=tabla_original,
                           tabla_procesado=tabla_procesado)
@bp.route('/descargar-excel')
def descargar_excel():
    # Ruta absoluta al archivo dentro de /data
    ruta_absoluta = os.path.join(os.path.dirname(__file__), "..", "data", "original.xlsx")

    # Cargar, limpiar y procesar
    df = cargar_datos(ruta_absoluta)
    df_limpio = limpiar_datos(df)
    df_procesado = calcular_riesgo(df_limpio)

    # Convertir a Excel en memoria
    output = BytesIO()
    df_procesado.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="datos_procesados.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@bp.route('/entrenar-modelo')
def ruta_entrenar_modelo():
    reporte = entrenar_modelo()
    return render_template("modelo_entrenado.html", reporte=reporte)

@bp.route('/ingModelo')
def ingenieria_modelo():
    reporte = entrenar_modelo()
    return render_template('ingModelo.html', reporte=reporte)
