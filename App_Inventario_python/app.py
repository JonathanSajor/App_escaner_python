import streamlit as st
from db import init_db

# Función para validar usuario (puedes mejorarla según tu lógica actual)
def validar_usuario(usuario, contrasena):
    return init_db.validar_usuario(usuario, contrasena)

# Pantalla de inicio de sesión
def pantalla_login():
    st.title("Inicio de Sesión")
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    login_btn = st.button("Iniciar sesión")
    if login_btn:
        if validar_usuario(usuario, contrasena):
            st.session_state['logged_in'] = True
            st.session_state['usuario'] = usuario
            st.success(f"¡Bienvenido, {usuario}!")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# Menú principal (placeholder)

def menu_principal():
    st.sidebar.title("Menú")
    opciones = [
        "Registrar pieza",
        "Consultar piezas",
        "Historial de salidas",
        "Registrar técnico",
        "Cerrar sesión"
    ]
    seleccion = st.sidebar.radio("Selecciona una opción", opciones)
    st.write(f"Usuario: {st.session_state.get('usuario', '')}")
    if seleccion == "Registrar pieza":
        registrar_pieza_streamlit()
    elif seleccion == "Consultar piezas":
        consultar_piezas_streamlit()
    elif seleccion == "Historial de salidas":
        historial_salidas_streamlit()
    elif seleccion == "Registrar técnico":
        registrar_tecnico_streamlit()
    elif seleccion == "Cerrar sesión":
        st.session_state.clear()
        st.experimental_rerun()

# --- Formularios e interfaces migradas ---
import pandas as pd
from db import init_db
from barcode.scanner import leer_codigo_barras

def registrar_pieza_streamlit():
    st.header("Registrar nueva pieza")
    with st.form("form_registro_pieza"):
        col1, col2 = st.columns(2)
        with col1:
            codigo = st.text_input("Código")
            descripcion = st.text_input("Descripción")
        with col2:
            ubicacion = st.text_input("Ubicación")
            stock = st.text_input("Stock")
        imagen = st.file_uploader("Leer código desde imagen", type=["png", "jpg", "jpeg", "bmp"])
        if imagen is not None:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(imagen.read())
                codigos = leer_codigo_barras(tmp.name)
            if codigos:
                st.success(f"Código leído: {codigos[0]}")
                codigo = codigos[0]
        submitted = st.form_submit_button("Registrar")
        if submitted:
            if not (codigo and descripcion and ubicacion and stock):
                st.error("Todos los campos son obligatorios")
            else:
                try:
                    stock_int = int(stock)
                except ValueError:
                    st.error("Stock debe ser un número")
                    return
                exito, error = init_db.registrar_pieza(codigo, descripcion, ubicacion, stock_int)
                if exito:
                    st.success("Pieza registrada exitosamente")
                else:
                    st.error(f"Error: {error}")

def consultar_piezas_streamlit():
    st.header("Consulta de piezas")
    piezas = init_db.obtener_piezas()
    df = pd.DataFrame(piezas, columns=["ID", "Código", "Descripción", "Ubicación", "Stock"])
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
        cursor.execute('''SELECT codigo, descripcion, ubicacion, cantidad, fecha FROM salidas WHERE id_usuario = ?''', (id_usuario,))
        salidas = cursor.fetchall()
        df = pd.DataFrame(salidas, columns=["Código", "Descripción", "Ubicación", "Cantidad", "Fecha"])
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
