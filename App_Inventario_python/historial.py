import streamlit as st
import pandas as pd
from db import init_db

def historial_salidas_streamlit():
    st.header("Historial de salidas")
    conn = init_db.get_connection()
    cursor = conn.cursor()
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
