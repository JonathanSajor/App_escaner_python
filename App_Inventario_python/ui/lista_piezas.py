import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from db.init_db import obtener_piezas, registrar_pieza

class ListaPiezas(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registros de Piezas")
        self.geometry("700x400")
        self.create_widgets()
        self.cargar_piezas()

    def create_widgets(self):
        columnas = ("ID", "Código", "Descripción", "Ubicación", "Stock")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.boton_importar = ttk.Button(self, text="Importar desde Excel", command=self.importar_excel)
        self.boton_importar.pack(pady=5)

    def importar_excel(self):
        archivo = filedialog.askopenfilename(title="Selecciona archivo Excel", filetypes=[("Archivos Excel", "*.xlsx;*.xls")])
        if not archivo:
            return
        # Mostrar ventana de carga con barra de progreso
        loading = tk.Toplevel(self)
        loading.title("Cargando")
        tk.Label(loading, text="Importando registros, por favor espere...").pack(padx=20, pady=(20,5))
        progress = ttk.Progressbar(loading, orient="horizontal", mode="determinate", length=300)
        progress.pack(padx=20, pady=(5,20))
        loading.update()
        self.update()
        try:
            df = pd.read_excel(archivo)
        except Exception as e:
            loading.destroy()
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            return
        requeridas = {"codigo", "descripcion", "ubicacion", "stock"}
        if not requeridas.issubset(df.columns.str.lower()):
            loading.destroy()
            messagebox.showerror("Error", "El archivo debe tener las columnas: codigo, descripcion, ubicacion, stock")
            return
        registros = 0
        total = len(df)
        if total > 0:
            progress["maximum"] = total
        for i, (_, row) in enumerate(df.iterrows(), 1):
            codigo = str(row.get("codigo", "")).strip()
            descripcion = str(row.get("descripcion", "")).strip()
            ubicacion = str(row.get("ubicacion", "")).strip()
            try:
                stock = int(row.get("stock", 0))
            except Exception:
                stock = 0
            if codigo and descripcion and ubicacion:
                exito, _ = registrar_pieza(codigo, descripcion, ubicacion, stock)
                if exito:
                    registros += 1
            progress["value"] = i
            loading.update()
        loading.destroy()
        self.cargar_piezas()
        messagebox.showinfo("Importación completada", f"Se importaron {registros} registros nuevos.")

    def cargar_piezas(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        piezas = obtener_piezas()
        for pieza in piezas:
            self.tabla.insert("", tk.END, values=pieza)
