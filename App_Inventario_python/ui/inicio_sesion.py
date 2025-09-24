import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.init_db import get_connection

class LoginWindow(tk.Frame):
    def __init__(self, master=None, on_login=None, on_registrar_tecnico=None):
        super().__init__(master)
        self.master = master
        self.on_login = on_login
        self.on_registrar_tecnico = on_registrar_tecnico
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Inicio de Sesión", font=("Arial", 16))
        self.label.pack(pady=10)

        self.usuario_label = ttk.Label(self, text="Número de Empleado:")
        self.usuario_label.pack(pady=5)
        self.usuario_entry = ttk.Entry(self)
        self.usuario_entry.pack(pady=5)

        self.contrasena_label = ttk.Label(self, text="Contraseña:")
        self.contrasena_label.pack(pady=5)
        self.contrasena_entry = ttk.Entry(self, show="*")
        self.contrasena_entry.pack(pady=5)

        self.login_btn = ttk.Button(self, text="Iniciar Sesión", command=self.login)
        self.login_btn.pack(pady=10)

        self.registrar_btn = ttk.Button(self, text="Registrar técnico", command=self.registrar_tecnico)
        self.registrar_btn.pack(pady=5)

    def login(self):
        numero = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        if not numero or not contrasena:
            messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre FROM usuarios WHERE numero_empleado=? AND contrasena=?', (numero, contrasena))
        row = cursor.fetchone()
        conn.close()
        if row:
            if self.on_login:
                self.on_login(row[0], row[1])
        else:
            messagebox.showerror("Error", "Número de empleado o contraseña incorrectos.")

    def registrar_tecnico(self):
        if self.on_registrar_tecnico:
            self.on_registrar_tecnico()
