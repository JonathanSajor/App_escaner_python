import streamlit as st
from salidas import registrar_salida_streamlit
from piezas import registrar_pieza_streamlit, consultar_piezas_streamlit
from historial import historial_salidas_streamlit

def menu_principal():
    st.markdown("""
        <style>
        .card-menu {
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            justify-content: center;
            margin-top: 2rem;
        }
        .card {
            background: #f8f9fa;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            padding: 2rem 2.5rem;
            min-width: 220px;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: box-shadow 0.2s;
        }
        .card:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.13);
        }
        .card-btn {
            margin-top: 1.2rem;
            padding: 0.7rem 1.5rem;
            border: none;
            border-radius: 8px;
            background: #2563eb;
            color: white;
            font-size: 1.1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        .card-btn:hover {
            background: #1d4ed8;
        }
        </style>
    """, unsafe_allow_html=True)

    st.write(f"### Bienvenido, {st.session_state.get('usuario', '')}")
    st.write(":package: **Sistema de Inventario**")

    col1, col2, col3 = st.columns(3)
    accion = None
    with col1:
        st.markdown('<div class="card">📦<br><b>Registrar pieza</b><br><button class="card-btn" id="btn_registrar_pieza">Ir</button></div>', unsafe_allow_html=True)
        if st.button("Registrar pieza", key="btn_registrar_pieza_real"):
            accion = "Registrar pieza"
        st.markdown('<div class="card">🚚<br><b>Registrar salida</b><br><button class="card-btn" id="btn_registrar_salida">Ir</button></div>', unsafe_allow_html=True)
        if st.button("Registrar salida de pieza", key="btn_registrar_salida_real"):
            accion = "Registrar salida de pieza"
    with col2:
        st.markdown('<div class="card">🔍<br><b>Consultar piezas</b><br><button class="card-btn" id="btn_consultar_piezas">Ir</button></div>', unsafe_allow_html=True)
        if st.button("Consultar piezas", key="btn_consultar_piezas_real"):
            accion = "Consultar piezas"
        st.markdown('<div class="card">📜<br><b>Historial de salidas</b><br><button class="card-btn" id="btn_historial_salidas">Ir</button></div>', unsafe_allow_html=True)
        if st.button("Historial de salidas", key="btn_historial_salidas_real"):
            accion = "Historial de salidas"
    with col3:
        st.markdown('<div class="card">🔒<br><b>Cerrar sesión</b><br><button class="card-btn" id="btn_cerrar_sesion">Ir</button></div>', unsafe_allow_html=True)
        if st.button("Cerrar sesión", key="btn_cerrar_sesion_real"):
            accion = "Cerrar sesión"

    # Lógica de navegación
    if accion == "Registrar pieza":
        registrar_pieza_streamlit()
    elif accion == "Registrar salida de pieza":
        registrar_salida_streamlit()
    elif accion == "Consultar piezas":
        consultar_piezas_streamlit()
    elif accion == "Historial de salidas":
        historial_salidas_streamlit()
    elif accion == "Cerrar sesión":
        st.session_state.clear()
        st.rerun()
