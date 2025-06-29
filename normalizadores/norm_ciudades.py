import pandas as pd
import unicodedata
import re

# Esta función limpia y normaliza una línea de texto (ciudad)
def limpiar_texto(texto):
    texto = texto.upper()  # Convertir a mayúsculas
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')  # Eliminar tildes y eñes
    texto = re.sub(r"[^\w\s]", "", texto)  # Eliminar caracteres especiales como puntos y comas
    texto = re.sub(r"\s+", " ", texto)  # Reemplazar tabs, múltiples espacios por uno solo
    texto = texto.strip()  # Quitar espacios al inicio y final
    return texto

# Función principal que toma el contenido del archivo y devuelve un DataFrame normalizado
def normalizar_ciudades(contenido_txt):
    lineas = contenido_txt.strip().split("\n")
    ciudades = []

    for linea in lineas:
        linea = linea.strip()
        if not linea:  # Ignorar líneas vacías después de limpiar tabs y espacios
            continue

        # Caso con numeración (ej. "1. Santiago")
        if re.match(r"^\d+\.\s", linea):
            partes = linea.split(".", 1)
            ciudad = limpiar_texto(partes[1])
        else:
            # Caso sin numeración
            ciudad = limpiar_texto(linea)

        if ciudad:  # Solo agregar si hay contenido real
            ciudades.append(ciudad)

    # Crear DataFrame, eliminar duplicados y asignar ID
    df = pd.DataFrame(ciudades, columns=["CIUDAD"])
    df = df.drop_duplicates().reset_index(drop=True)
    df["ID"] = df.index + 1
    df = df[["ID", "CIUDAD"]]
    return df
