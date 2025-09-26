import streamlit as st
from datetime import datetime
from db import init_db

def registrar_salida_streamlit():
    st.header("Registro de salida de pieza")
    if 'salida_codigo' not in st.session_state:
        st.session_state['salida_codigo'] = ''
    if 'salida_ubicacion' not in st.session_state:
        st.session_state['salida_ubicacion'] = ''
    if 'salida_maquina' not in st.session_state:
        st.session_state['salida_maquina'] = ''

    def actualizar_autocompletado():
        codigo = st.session_state['salida_codigo']
        if len(codigo) >= 2:
            abrev = codigo[:2].upper()
            try:
                nombre = init_db.obtener_proceso_por_abreviatura(abrev)
            except Exception:
                nombre = ''
            st.session_state['salida_maquina'] = nombre
        else:
            st.session_state['salida_maquina'] = ''
        if len(codigo) > 0:
            try:
                ubicacion = init_db.obtener_ubicacion_por_codigo(codigo)
            except Exception:
                ubicacion = ''
            st.session_state['salida_ubicacion'] = ubicacion
        else:
            st.session_state['salida_ubicacion'] = ''

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
                    st.session_state['salida_codigo'] = ''
                    st.session_state['salida_ubicacion'] = ''
                    st.session_state['salida_maquina'] = ''
                else:
                    st.error(f"Error: {error}")
            except Exception as e:
                st.error(f"Error inesperado: {e}")
