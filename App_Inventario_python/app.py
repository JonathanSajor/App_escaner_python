from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
# --- Escaneo de código de barras con cámara ---
import numpy as np
from pyzbar.pyzbar import decode as pyzbar_decode
from PIL import Image

class BarcodeScannerTransformer(VideoTransformerBase):
    def __init__(self):
        self.last_code = None
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        pil_img = Image.fromarray(img)
        codes = pyzbar_decode(pil_img)
        if codes:
            self.last_code = codes[0].data.decode('utf-8')
        return img

def escanear_codigo_camara():
    st.info("Haz clic en 'Iniciar cámara' y muestra el código de barras frente a la cámara.")
    ctx = webrtc_streamer(key="barcode", video_transformer_factory=BarcodeScannerTransformer)
    if ctx.video_transformer and ctx.video_transformer.last_code:
        st.success(f"Código detectado: {ctx.video_transformer.last_code}")
        return ctx.video_transformer.last_code
    return None
import streamlit as st
from db import init_db

# Función para validar usuario (puedes mejorarla según tu lógica actual)
def validar_usuario(usuario, contrasena):
    return init_db.validar_usuario(usuario, contrasena)

# Pantalla de inicio de sesión
def pantalla_login():
    st.title("Inicio de Sesión")
    tabs = st.tabs(["Iniciar sesión", "Registrarse"])
    with tabs[0]:
        usuario = st.text_input("Usuario", key="login_usuario")
        contrasena = st.text_input("Contraseña", type="password", key="login_contrasena")
        login_btn = st.button("Iniciar sesión")
        if login_btn:
            if validar_usuario(usuario, contrasena):
                st.session_state['logged_in'] = True
                st.session_state['usuario'] = usuario
                st.success(f"¡Bienvenido, {usuario}!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
    with tabs[1]:
        st.subheader("Registro de nuevo usuario")
        nombre = st.text_input("Nombre", key="reg_nombre")
        numero = st.text_input("Número de empleado", key="reg_numero")
        contrasena_reg = st.text_input("Contraseña", type="password", key="reg_contrasena")
        if st.button("Registrar cuenta"):
            if not (nombre and numero and contrasena_reg):
                st.error("Todos los campos son obligatorios")
            else:
                exito, mensaje = init_db.registrar_usuario(nombre, numero, contrasena_reg)
                if exito:
                    st.success("Usuario registrado correctamente. Ahora puedes iniciar sesión.")
                else:
                    st.error(mensaje or "No se pudo registrar el usuario.")

# Menú principal (placeholder)

def menu_principal():
    st.sidebar.title("Menú")
    opciones = [
        "Registrar salida de pieza",
        "Registrar pieza",
        "Consultar piezas",
        "Historial de salidas",
        "Cerrar sesión"
    ]
    seleccion = st.sidebar.radio("Selecciona una opción", opciones)
    st.write(f"Usuario: {st.session_state.get('usuario', '')}")
    if seleccion == "Registrar pieza":
        registrar_pieza_streamlit()
    elif seleccion == "Registrar salida de pieza":
        registrar_salida_streamlit()
    elif seleccion == "Consultar piezas":
        consultar_piezas_streamlit()
    elif seleccion == "Historial de salidas":
        historial_salidas_streamlit()
    elif seleccion == "Cerrar sesión":
        st.session_state.clear()
        st.rerun()
# --- Formularios e interfaces migradas ---
from datetime import datetime
def registrar_salida_streamlit():
    st.header("Registro de salida de pieza")
    # Estado para autocompletar
    if 'salida_codigo' not in st.session_state:
        st.session_state['salida_codigo'] = ''
    if 'salida_ubicacion' not in st.session_state:
        st.session_state['salida_ubicacion'] = ''
    if 'salida_maquina' not in st.session_state:
        st.session_state['salida_maquina'] = ''

    def actualizar_autocompletado():
        codigo = st.session_state['salida_codigo']
        # Autocompletar máquina
        if len(codigo) >= 2:
            abrev = codigo[:2].upper()
            try:
                nombre = init_db.obtener_proceso_por_abreviatura(abrev)
            except Exception:
                nombre = ''
            st.session_state['salida_maquina'] = nombre
        else:
            st.session_state['salida_maquina'] = ''
        # Autocompletar ubicación
        if len(codigo) > 0:
            try:
                ubicacion = init_db.obtener_ubicacion_por_codigo(codigo)
            except Exception:
                ubicacion = ''
            st.session_state['salida_ubicacion'] = ubicacion
        else:
            st.session_state['salida_ubicacion'] = ''

    # Campo de código fuera del form para permitir autocompletado
    st.text_input("Código de pieza", value=st.session_state['salida_codigo'], key="salida_codigo", on_change=actualizar_autocompletado)

    with st.form("form_registro_salida"):
        ubicacion = st.text_input("Ubicación de pieza", value=st.session_state['salida_ubicacion'], key="salida_ubicacion")
        maquina = st.text_input("Máquina", value=st.session_state['salida_maquina'], key="salida_maquina")
        tipo = st.selectbox("Tipo de salida", ["Correctivo", "Preventivo", "Sistematico"])
        cantidad = st.text_input("Piezas salientes")
        tecnico = st.text_input("Nombre del técnico")
        fecha = st.text_input("Fecha", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        descripcion = st.text_input("Descripción")
        submitted = st.form_submit_button("Registrar salida")
        if submitted:
            codigo = st.session_state['salida_codigo']
            # Validaciones básicas
            if not (codigo and ubicacion and maquina and tipo and cantidad and tecnico and fecha and descripcion):
                st.error("Todos los campos son obligatorios")
                return
            if not (len(codigo) == 9 and codigo.isalnum() and codigo.isupper()):
                st.error("Código: exactamente 9 caracteres, solo mayúsculas y números")
                return
            if not (ubicacion.isalnum() and ubicacion.isupper() and len(ubicacion) <= 7):
                st.error("Ubicación: solo mayúsculas y números, máx 7 caracteres")
                return
            if not (cantidad.isdigit() and cantidad != ""):
                st.error("Cantidad: solo números")
                return
            # Obtener id_usuario
            conn = init_db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM usuarios WHERE numero_empleado = ?', (st.session_state.get('usuario', ''),))
            row = cursor.fetchone()
            conn.close()
            if not row:
                st.error("No se pudo determinar el usuario actual.")
                return
            id_usuario = row[0]
            try:
                exito, error, nuevo_stock = init_db.registrar_salida(
                    id_usuario, codigo, descripcion, ubicacion, cantidad, fecha, tecnico, tipo, maquina
                )
                if exito:
                    st.success(f"Registro guardado. Stock actualizado: {nuevo_stock}")
                    st.rerun()
                    # Limpiar autocompletado
                    st.session_state['salida_codigo'] = ''
                    st.session_state['salida_ubicacion'] = ''
                    st.session_state['salida_maquina'] = ''
                else:
                    st.error(f"Error: {error}")
            except Exception as e:
                st.error(f"Error inesperado: {e}")

# --- Formularios e interfaces migradas ---
import pandas as pd
from db import init_db
from barcode.scanner import leer_codigo_barras

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

def historial_salidas_streamlit():
    st.header("Historial de salidas")
    # Suponiendo que el usuario está logueado y su número está en session_state['usuario']
    conn = init_db.get_connection()
    cursor = conn.cursor()
    # Buscar id_usuario
    cursor.execute('SELECT id, nombre FROM usuarios WHERE numero_empleado = ?', (st.session_state.get('usuario', ''),))
    row = cursor.fetchone()
    if row:
        id_usuario, nombre_usuario = row
        cursor.execute('''SELECT codigo, descripcion, ubicacion, cantidad, fecha, nombre_tecnico, tipo_salida, maquina FROM salidas WHERE id_usuario = ?''', (id_usuario,))
        salidas = cursor.fetchall()
        df = pd.DataFrame(salidas, columns=["Código", "Descripción", "Ubicación", "Cantidad", "Fecha y hora", "Técnico", "Tipo de salida", "Máquina"])
        st.dataframe(df)
    else:
        st.warning("No se encontró el usuario actual para mostrar el historial.")
    conn.close()

def registrar_tecnico_streamlit():
    st.header("Registro de técnico/usuario")
    with st.form("form_registro_tecnico"):
        nombre = st.text_input("Nombre")
        numero = st.text_input("Número de empleado")
        contrasena = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Registrar")
        if submitted:
            if not (nombre and numero and contrasena):
                st.error("Todos los campos son obligatorios")
            else:
                exito, mensaje = init_db.registrar_usuario(nombre, numero, contrasena)
                if exito:
                    st.success("Técnico registrado correctamente")
                else:
                    st.error(mensaje or "No se pudo registrar el técnico.")

# Lógica principal
def main():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        pantalla_login()
    else:
        menu_principal()

if __name__ == "__main__":
    main()
