import pandas as pd
import unicodedata
import re

# Función que limpia y normaliza texto
def limpiar_texto(texto):
    texto = texto.upper()  # O reemplázalo por .lower() si quieres minúsculas
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = re.sub(r"[^\w\s]", "", texto)  # Quita caracteres especiales
    texto = texto.strip()
    return texto

# FUNCION PRINCIPAL CORRECTA
def normalizar_ciudades(contenido_txt):
    lineas = contenido_txt.strip().split("\n")
    ciudades = []

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue  # Salta líneas vacías

        # Caso con numeración (e.g. "1. Santiago")
        if re.match(r"^\d+\.\s", linea):
            partes = linea.split(".", 1)
            ciudad = limpiar_texto(partes[1])
        else:
            # Caso sin numeración
            ciudad = limpiar_texto(linea)

        ciudades.append(ciudad)

    # Crear DataFrame
    df = pd.DataFrame(ciudades, columns=["CIUDAD"])
    df = df.drop_duplicates().reset_index(drop=True)
    df["ID"] = df.index + 1
    df = df[["ID", "CIUDAD"]]
    return df
