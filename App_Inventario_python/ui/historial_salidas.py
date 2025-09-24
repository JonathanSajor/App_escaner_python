import tkinter as tk
from tkinter import ttk
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.init_db import get_connection

class HistorialSalidas(tk.Toplevel):
    def __init__(self, id_usuario, nombre_usuario):
        super().__init__()
        self.title(f"Historial de salidas de {nombre_usuario}")
        self.geometry("800x400")
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.create_widgets()
        self.cargar_historial()

    def create_widgets(self):
        self.label = ttk.Label(self, text=f"Historial de salidas de {self.nombre_usuario}", font=("Arial", 14))
        self.label.pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("codigo", "descripcion", "ubicacion", "cantidad", "fecha"), show="headings")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("ubicacion", text="Ubicación")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("fecha", text="Fecha")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def cargar_historial(self):
        conn = get_connection()
        cursor = conn.cursor()
        # Suponiendo que la tabla de salidas tiene un campo id_usuario
        cursor.execute('''SELECT codigo, descripcion, ubicacion, cantidad, fecha FROM salidas WHERE id_usuario = ?''', (self.id_usuario,))
        for row in cursor.fetchall():
            self.tree.insert('', tk.END, values=row)
        conn.close()
