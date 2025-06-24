import pandas as pd
import unicodedata
import re

# Esta función limpia y normaliza una línea de texto (ciudad)
def limpiar_texto(texto):
    texto = texto.upper()  # Convertir a mayúsculas
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')  # Eliminar tildes y eñes
    texto = re.sub(r"[^\w\s]", "", texto)  # Eliminar caracteres especiales como puntos y comas
    texto = texto.strip()  # Quitar espacios al inicio y final
    return texto

# Función principal que toma el contenido del archivo y devuelve un DataFrame normalizado
def normalizar_ciudades(contenido_txt):
    lineas = contenido_txt.strip().split("\n")  # Separar el texto en líneas
    ciudades = []
    for linea in lineas:
        partes = linea.strip().split(".", 1)
        if len(partes) == 2:
            ciudad = limpiar_texto(partes[1])
            ciudades.append(ciudad)

    # Crear DataFrame, eliminar duplicados y asignar ID
    df = pd.DataFrame(ciudades, columns=["CIUDAD"])
    df = df.drop_duplicates().reset_index(drop=True)
    df["ID"] = df.index + 1
    df = df[["ID", "CIUDAD"]]  # Ordenar columnas
    return df
