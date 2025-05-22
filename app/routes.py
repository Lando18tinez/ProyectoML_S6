from flask import Blueprint, render_template
from app.utils import cargar_datos, limpiar_datos, calcular_riesgo, resaltar_riesgo


bp = Blueprint('main', __name__)

@bp.route('/ver_datos')
def ver_datos():
    df_original = cargar_datos("data/original.xlsx")
    df_limpio = limpiar_datos(df_original.copy())
    df_procesado = calcular_riesgo(df_limpio)

    tabla_original = df_original.head(50).to_html(classes="table table-bordered", index=False)
    tabla_procesado = resaltar_riesgo(df_procesado.head(50)).to_html(index=False)

    return render_template("show_data.html", tabla_original=tabla_original, tabla_procesado=tabla_procesado)