import pandas as pd
import numpy as np

def cargar_datos(path):
    return pd.read_excel(path)

def limpiar_datos(df):
    # 1. Eliminar columnas irrelevantes
    columnas_a_eliminar = [
        "Año", "Casa Justicia", "Fecha  y Hora Solicitud CRI",
        "Nro Solicitud", "Nro Remisión"
    ]
    df = df.drop(columns=[col for col in columnas_a_eliminar if col in df.columns])

    # 2. Rellenar nulos y formatear
    df['Grupo Etario'] = df['Grupo Etario'].fillna('').astype(str)
    df['Sexo'] = df['Sexo'].fillna('').astype(str)
    df['Estrato'] = df['Estrato'].fillna('').astype(str)
    df['Nacionalidad'] = df['Nacionalidad'].fillna('').astype(str)
    df['Entidad'] = df['Entidad'].fillna('').astype(str)
    df['Motivo'] = df['Motivo'].fillna('').astype(str)

    # 3. Clasificación basada en motivo
    motivos_violencia = [
        "05 Orientación a víctimas", "09 Informe pericial sobre lesiones",
        "26 Abandono de adulto mayor", "26 Asistencia psicológica", "26 Asistencia social",
        "26 Recepción de denuncias por delitos contra NNA", "26 Relaciones conflictivas familiares",
        "26 Violencia física", "26 Violencia física y patrimonial", "26 Violencia física y psicológica",
        "26 Violencia física, psicológica y sexual", "26 Violencia patrimonial", "26 Violencia psicológica"
    ]
    motivos_conflicto = ["05 Recepción declaración desplazados"]

    df['victima_violencia'] = df['Motivo'].isin(motivos_violencia)
    df['victima_conflicto'] = df['Motivo'].isin(motivos_conflicto)

    # 4. Simulación de abandono (puede ser mejorado)
    np.random.seed(42)
    df['abandono'] = np.random.choice([True, False], size=len(df), p=[0.05, 0.95])

    return df

def calcular_riesgo(df):
    def score(row):
        score = 0.0
        if any(x in row['Grupo Etario'] for x in ["0 y 5", "12 y 17", "56 y 63", "64"]): score += 0.2
        if row['Sexo'].lower() == 'mujer': score += 0.1
        if row.get('victima_violencia'): score += 0.2
        if row.get('victima_conflicto'): score += 0.2
        if any(e in row['Entidad'] for e in ['ICBF', 'Policía', 'Defensoría']): score += 0.1
        if '1' in row['Estrato'] or 'sin estrato' in row['Estrato'].lower(): score += 0.1
        if row['Nacionalidad'].lower() != 'colombiano': score += 0.1
        return round(score, 2)

    df['riesgo_score'] = df.apply(score, axis=1)
    return df
def resaltar_riesgo(df):
    """
    Aplica bordes y colores directamente con HTML embebido.
    """
    def estilo_riesgo(val):
        if val >= 0.6:
            return 'background-color: red; color: white;'
        elif val >= 0.4:
            return 'background-color: yellow;'
        return ''

    styled = df.style.applymap(estilo_riesgo, subset=['riesgo_score']) \
                     .set_table_attributes('class="styled-risk-table"')
    return styled