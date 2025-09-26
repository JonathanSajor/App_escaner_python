import streamlit as st
from db import init_db

def validar_usuario(usuario, contrasena):
    return init_db.validar_usuario(usuario, contrasena)

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
