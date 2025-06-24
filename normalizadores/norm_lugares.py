import pandas as pd
import re
import unicodedata

# Extrae número de calle si existe en la dirección
def extraer_numero(texto):
    match = re.search(r'\b\d+\w?\b', texto)
    return match.group(0) if match else ""

# Normaliza texto (mayúsculas, sin tildes ni caracteres especiales)
def limpiar_texto(texto):
    texto = texto.upper()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = texto.strip()
    return texto

# Parsea la dirección completa en componentes
def parse_direccion(direccion):
    partes = [p.strip() for p in direccion.split(',')]
    if len(partes) < 2:
        return pd.Series([direccion, "", "", ""])
    elif len(partes) == 2:
        nombre_calle = partes[0]
        numero_calle = extraer_numero(nombre_calle)
        ciudad_estado_provincia = ""
        pais = partes[1]
    else:
        nombre_calle = partes[0]
        numero_calle = extraer_numero(nombre_calle)
        ciudad_estado_provincia = ", ".join(partes[1:-1])
        pais = partes[-1]
    return pd.Series([nombre_calle, numero_calle, ciudad_estado_provincia, pais])

# Función principal que normaliza lugares con dirección y coordenadas
def normalizar_lugares(contenido_txt):
    from io import StringIO
    df = pd.read_csv(StringIO(contenido_txt), sep=';', encoding='latin1')

    # Limpiar y renombrar columnas
    df['Nombre del lugar'] = df['Nombre del lugar'].apply(limpiar_texto)
    df['Dirección Completa'] = df['Dirección Completa'].apply(limpiar_texto)
    df['Georeferencia'] = df['Georeferencia'].apply(limpiar_texto)

    df.rename(columns={
        'Nombre del lugar': 'NOMBRE',
        'Dirección Completa': 'DIRECCION_COMPLETA',
        'Georeferencia': 'COORDENADAS'
    }, inplace=True)

    # Separar coordenadas en LATITUD y LONGITUD
    df[['LATITUD', 'LONGITUD']] = df['COORDENADAS'].str.split(',', expand=True)
    df['LATITUD'] = df['LATITUD'].str.strip()
    df['LONGITUD'] = df['LONGITUD'].str.strip()

    # Eliminar duplicados por nombre y coordenadas
    df = df.drop_duplicates(subset=['NOMBRE', 'LATITUD', 'LONGITUD']).reset_index(drop=True)

    # Parsear dirección
    df[['NOMBRE_CALLE', 'NUMERO_CALLE', 'CIUDAD_ESTADO_PROVINCIA', 'PAIS']] = df['DIRECCION_COMPLETA'].apply(parse_direccion)

    # Asignar ID
    df['ID'] = df.index + 1

    # Ordenar columnas finales
    df_final = df[['ID', 'NOMBRE', 'NOMBRE_CALLE', 'NUMERO_CALLE', 'CIUDAD_ESTADO_PROVINCIA', 'PAIS', 'LATITUD', 'LONGITUD']]
    return df_final
