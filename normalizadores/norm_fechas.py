import pandas as pd
import re
from datetime import datetime
from dateutil import parser

# Intenta convertir una fecha a formato DD-MM-YYYY
def parse_fecha(fecha_raw):
    if pd.isnull(fecha_raw):
        return None
    if isinstance(fecha_raw, datetime):
        return fecha_raw.strftime("%d-%m-%Y")

    # Ignorar registros sin fecha útil
    fecha_str = str(fecha_raw).lower()
    if "a.c" in fecha_str or "alrededor" in fecha_str:
        return None

    fecha_raw = re.sub(r"[\\/\\.]", "-", str(fecha_raw).strip())
    try:
        fecha = parser.parse(fecha_raw, dayfirst=True)
        return fecha.strftime("%d-%m-%Y")
    except:
        return None

# Calcula edad actual a partir de la fecha
def calcular_edad(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%d-%m-%Y")
        hoy = datetime.today()
        return hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
    except:
        return None

# Devuelve 1 si cumple años hoy, 0 si no
def es_cumple_hoy(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%d-%m-%Y")
        hoy = datetime.today()
        return int(fecha.day == hoy.day and fecha.month == hoy.month)
    except:
        return 0

# -------- FUNCIÓN PRINCIPAL --------
def normalizar_fechas(contenido_txt=None, archivo_excel=None):
    datos = []

    # CASO TXT
    if contenido_txt:
        lineas = contenido_txt.strip().split("\n")
        for linea in lineas:
            if not linea.strip():
                continue
            match = re.match(r"\d+\.\s*(.*?)\s*-\s*(.+)", linea.strip())
            if match:
                nombre = match.group(1).strip().upper()
                fecha_raw = match.group(2).strip()
                fecha = parse_fecha(fecha_raw)
                datos.append((nombre, fecha))
            else:
                nombre = linea.strip().upper()
                if nombre:
                    datos.append((nombre, None))

    # CASO EXCEL
    elif archivo_excel:
        df_excel = pd.read_excel(archivo_excel)
        columnas = df_excel.columns

        # Buscar columnas similares a "Nombre" y "Fecha Nacimiento"
        nombre_col = next((col for col in columnas if "NOMBRE" in col.upper()), None)
        fecha_col = next((col for col in columnas if "FECHA" in col.upper() and "NACIMIENTO" in col.upper()), None)

        if nombre_col:
            for _, row in df_excel.iterrows():
                nombre = str(row[nombre_col]).strip().upper()
                fecha = parse_fecha(row[fecha_col]) if fecha_col else None
                datos.append((nombre, fecha))

    # Armar DataFrame
    df = pd.DataFrame(datos, columns=["NOMBRE", "FECHA_NACIMIENTO"])

    # Eliminar duplicados por nombre
    df = df.drop_duplicates(subset="NOMBRE", keep="first")

    # Calcular edad y cumpleaños si hay fechas
    df["EDAD"] = df["FECHA_NACIMIENTO"].apply(lambda x: calcular_edad(x) if pd.notnull(x) else None)
    df["CUMPLE_HOY"] = df["FECHA_NACIMIENTO"].apply(lambda x: es_cumple_hoy(x) if pd.notnull(x) else 0)

    return df
