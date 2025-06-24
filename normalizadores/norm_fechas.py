import pandas as pd
import re
from datetime import datetime
from dateutil import parser

# Intenta convertir una fecha a formato DD-MM-YYYY
def parse_fecha(fecha_raw):
    if "a.C" in fecha_raw.lower() or "alrededor" in fecha_raw.lower():
        return None
    fecha_raw = re.sub(r"[\/\.]", "-", fecha_raw.strip())
    try:
        fecha = parser.parse(fecha_raw, dayfirst=True)
        return fecha.strftime("%d-%m-%Y")
    except:
        return None

# Calcula la edad actual a partir de una fecha
def calcular_edad(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%d-%m-%Y")
        hoy = datetime.today()
        return hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
    except:
        return None

# Verifica si la persona cumple años hoy
def es_cumple_hoy(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%d-%m-%Y")
        hoy = datetime.today()
        return int(fecha.day == hoy.day and fecha.month == hoy.month)
    except:
        return 0

# Función principal que normaliza fechas de nacimiento
def normalizar_fechas(contenido_txt):
    lineas = contenido_txt.strip().split("\n")
    datos = []
    for linea in lineas:
        match = re.match(r"\d+\.\s*(.*?)\s*-\s*(.+)", linea.strip())
        if match:
            nombre = match.group(1).strip().upper()
            fecha_raw = match.group(2).strip()
            fecha = parse_fecha(fecha_raw)
            if fecha:
                datos.append((nombre, fecha))

    df = pd.DataFrame(datos, columns=["NOMBRE", "FECHA_NACIMIENTO"])
    df = df.drop_duplicates(subset="NOMBRE", keep="first")
    df["EDAD"] = df["FECHA_NACIMIENTO"].apply(calcular_edad)
    df["CUMPLE_HOY"] = df["FECHA_NACIMIENTO"].apply(es_cumple_hoy)
    return df
