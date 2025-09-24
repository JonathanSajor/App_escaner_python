
import tkinter as tk
from ui.inicio_sesion import LoginWindow
from ui.main_window import MainWindow

def mostrar_ventana_principal(id_usuario, nombre_usuario):
    for widget in root.winfo_children():
        widget.destroy()
    app = MainWindow(root, id_usuario=id_usuario, nombre_usuario=nombre_usuario)
    root.title(f"Inventario de Almacén - Usuario: {nombre_usuario}")

def abrir_registro_tecnico():
    import subprocess
    import sys
    import os
    ruta = os.path.join(os.path.dirname(__file__), 'ui', 'registro_tecnico_form.py')
    subprocess.Popen([sys.executable, ruta])

def main():
    global root
    root = tk.Tk()
    root.title("Inicio de Sesión")
    login = LoginWindow(root, on_login=mostrar_ventana_principal, on_registrar_tecnico=abrir_registro_tecnico)
    root.mainloop()

if __name__ == "__main__":
    main()
