import streamlit as st
import pandas as pd
from io import BytesIO
from normalizadores import norm_ciudades, norm_fechas, norm_lugares

# ----------- CONFIGURACIÓN DE LA APP -----------
st.set_page_config(page_title="Normalizador de Datos", layout="centered")
st.title("🧹 Normalizador de Datos")
st.markdown("""
Esta aplicación te permite normalizar tres tipos de datos:
- **Ciudades**
- **Fechas de nacimiento**
- **Lugares con direcciones**

Sube tu archivo `.txt` o `.xlsx` (solo para fechas), selecciona el tipo de datos y descarga los resultados normalizados.
""")

# ----------- SUBIDA DE ARCHIVO -----------
archivo = st.file_uploader(
    "📂 Sube tu archivo (.txt o .xlsx)",
    type=["txt", "xlsx"]
)

tipo = st.selectbox(
    "¿Qué tipo de datos quieres normalizar?",
    [
        "Seleccionar...",
        "Ciudades",
        "Fechas de nacimiento",
        "Lugares con direcciones"
    ]
)

# ----------- PROCESAMIENTO -----------
if archivo and tipo != "Seleccionar...":
    df = None

    # Procesar según el tipo de archivo y tipo de datos
    if tipo == "Fechas de nacimiento" and archivo.name.endswith(".xlsx"):
        # Lectura directa de Excel
        df = norm_fechas.normalizar_fechas(archivo_excel=archivo)
    else:
        # Leer contenido binario (.txt)
        contenido_binario = archivo.read()
        try:
            contenido = contenido_binario.decode("utf-8")
        except UnicodeDecodeError:
            contenido = contenido_binario.decode("latin1")

        if tipo == "Ciudades":
            df = norm_ciudades.normalizar_ciudades(contenido)
        elif tipo == "Fechas de nacimiento":
            df = norm_fechas.normalizar_fechas(contenido_txt=contenido)
        elif tipo == "Lugares con direcciones":
            df = norm_lugares.normalizar_lugares(contenido)
        else:
            st.error("Tipo de dato no válido")
            st.stop()

    if df is not None and not df.empty:
        # Mostrar vista previa
        st.success(f"✅ Datos normalizados correctamente. Total registros: {len(df)}")
        st.dataframe(df, use_container_width=True)

        # Convertir a CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Descargar como CSV",
            data=csv,
            file_name="datos_normalizados.csv",
            mime="text/csv"
        )

        # Convertir a Excel
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Normalizado")

        st.download_button(
            "📥 Descargar como Excel",
            data=buffer.getvalue(),
            file_name="datos_normalizados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ No se encontraron datos para normalizar.")

elif tipo != "Seleccionar...":
    st.warning("⚠️ Debes subir un archivo para continuar.")
