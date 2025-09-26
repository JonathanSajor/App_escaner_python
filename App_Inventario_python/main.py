import streamlit as st
from auth import pantalla_login
from menu import menu_principal

def main():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        pantalla_login()
    else:
        menu_principal()

if __name__ == "__main__":
    main()
