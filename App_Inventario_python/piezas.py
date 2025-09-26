import streamlit as st
import pandas as pd
from db import init_db
from barcode.scanner import leer_codigo_barras
from barcode_camera import escanear_codigo_camara

def registrar_pieza_streamlit():
    st.header("Registrar nueva pieza")
    codigo = ""
    st.subheader("Escanear código de barras")
    if st.button("Usar cámara para escanear"):
        st.session_state['show_camera'] = True
    if st.session_state.get('show_camera', False):
        codigo_detectado = escanear_codigo_camara()
        if codigo_detectado:
            codigo = codigo_detectado
            st.session_state['show_camera'] = False
    st.subheader("O subir imagen de código de barras")
    imagen = st.file_uploader("Leer código desde imagen", type=["png", "jpg", "jpeg", "bmp"])
    if imagen is not None:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(imagen.read())
            codigos = leer_codigo_barras(tmp.name)
        if codigos:
            st.success(f"Código leído: {codigos[0]}")
            codigo = codigos[0]
    with st.form("form_registro_pieza"):
        col1, col2 = st.columns(2)
        with col1:
            codigo_input = st.text_input("Código", value=codigo)
            descripcion = st.text_input("Descripción")
        with col2:
            ubicacion = st.text_input("Ubicación")
            stock = st.text_input("Stock")
        submitted = st.form_submit_button("Registrar")
        if submitted:
            if not (codigo_input and descripcion and ubicacion and stock):
                st.error("Todos los campos son obligatorios")
            else:
                try:
                    stock_int = int(stock)
                except ValueError:
                    st.error("Stock debe ser un número")
                    return
                exito, error = init_db.registrar_pieza(codigo_input, descripcion, ubicacion, stock_int)
                if exito:
                    st.success("Pieza registrada exitosamente")
                else:
                    st.error(f"Error: {error}")

def consultar_piezas_streamlit():
    st.header("Consulta de piezas")
    piezas = init_db.obtener_piezas()
    df = pd.DataFrame(piezas, columns=["ID", "Código", "Descripción", "Ubicación", "Stock"])
    filtro = st.text_input("Buscar por código, descripción o ubicación")
    if filtro:
        filtro_lower = filtro.lower()
        df = df[df.apply(lambda row: filtro_lower in str(row["Código"]).lower() or filtro_lower in str(row["Descripción"]).lower() or filtro_lower in str(row["Ubicación"]).lower(), axis=1)]
    st.dataframe(df)
