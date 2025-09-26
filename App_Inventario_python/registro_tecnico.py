import streamlit as st
from db import init_db

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
