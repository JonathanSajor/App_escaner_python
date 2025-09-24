import tkinter as tk
from tkinter import ttk
from datetime import datetime

class RegistroPiezaForm(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registro de Salida de Pieza")
        self.geometry("500x500")
        self.create_widgets()

    def create_widgets(self):
        self.campos = [
            ("Código de pieza", "codigo"),
            ("Ubicación de pieza", "ubicacion"),
            ("Máquina", "maquina"),
            ("Tipo de salida", "tipo"),
            ("Piezas salientes", "cantidad"),
            ("Nombre del técnico", "tecnico"),
            ("Fecha", "fecha"),
            ("Descripción", "descripcion"),
        ]

        self.entradas = {}
        for i, (etiqueta, clave) in enumerate(self.campos):
            label = ttk.Label(self, text=etiqueta+":")
            label.grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            if clave == "tipo":
                entry = ttk.Combobox(self, values=["Correctivo", "Preventivo", "Sistematico"])
                entry.current(0)
            elif clave == "fecha":
                entry = ttk.Entry(self)
                entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            else:
                entry = ttk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entradas[clave] = entry

        # Vincular evento de cambio en el campo código para autocompletar máquina y ubicación
        self.entradas["codigo"].bind("<KeyRelease>", self.autocompletar_campos)

        self.boton_guardar = ttk.Button(self, text="Guardar registro", command=self.guardar_registro)
        self.boton_guardar.grid(row=len(self.campos), column=0, columnspan=2, pady=20)
        self.mensaje = ttk.Label(self, text="")
        self.mensaje.grid(row=len(self.campos)+1, column=0, columnspan=2)
        self.boton_guardar = ttk.Button(self, text="Guardar registro", command=self.guardar_registro)
        self.boton_guardar.grid(row=len(self.campos), column=0, columnspan=2, pady=20)
        self.mensaje = ttk.Label(self, text="")
        self.mensaje.grid(row=len(self.campos)+1, column=0, columnspan=2)

    def autocompletar_campos(self, event=None):
        codigo = self.entradas["codigo"].get()
        # Autocompletar máquina
        if len(codigo) >= 2:
            abrev = codigo[:2].upper()
            try:
                from db.init_db import obtener_proceso_por_abreviatura
                nombre = obtener_proceso_por_abreviatura(abrev)
            except Exception:
                nombre = ""
            self.entradas["maquina"].delete(0, tk.END)
            self.entradas["maquina"].insert(0, nombre)
        else:
            self.entradas["maquina"].delete(0, tk.END)

        # Autocompletar ubicación
        if len(codigo) > 0:
            try:
                from db.init_db import obtener_ubicacion_por_codigo
                ubicacion = obtener_ubicacion_por_codigo(codigo)
            except Exception:
                ubicacion = ""
            self.entradas["ubicacion"].delete(0, tk.END)
            if ubicacion:
                self.entradas["ubicacion"].insert(0, ubicacion)
        else:
            self.entradas["ubicacion"].delete(0, tk.END)

    def guardar_registro(self):
        datos = {k: v.get() for k, v in self.entradas.items()}
        # Validación campo codigo: exactamente 9 caracteres, solo mayúsculas y números
        codigo = datos.get("codigo", "")
        if not (len(codigo) == 9 and codigo.isalnum() and codigo.isupper()):
            self.mensaje.config(text="Código: exactamente 9 caracteres, solo mayúsculas y números (sin signos ni minúsculas)", foreground="red")
            return
        # Validación campo ubicacion
        ubicacion = datos.get("ubicacion", "")
        if not (ubicacion.isalnum() and ubicacion.isupper() and len(ubicacion) <= 7):
            self.mensaje.config(text="Ubicación: solo mayúsculas y números, máx 7 caracteres", foreground="red")
            return
        # Validación campo cantidad
        cantidad = datos.get("cantidad", "")
        if not (cantidad.isdigit() and cantidad != ""):
            self.mensaje.config(text="Cantidad: solo números", foreground="red")
            return

        # Obtener datos adicionales
        descripcion = datos.get("descripcion", "")
        fecha = datos.get("fecha", "")
        nombre_tecnico = datos.get("tecnico", "")
        tipo_salida = datos.get("tipo", "")
        maquina = datos.get("maquina", "")
        # Obtener id_usuario si está disponible en el master principal
        id_usuario = getattr(self.master, 'id_usuario', None)
        if id_usuario is None:
            self.mensaje.config(text="No se pudo determinar el usuario actual.", foreground="red")
            return
        try:
            from db.init_db import registrar_salida
            exito, error, nuevo_stock = registrar_salida(
                id_usuario, codigo, descripcion, ubicacion, cantidad, fecha, nombre_tecnico, tipo_salida, maquina
            )
            if exito:
                self.mensaje.config(text=f"Registro guardado. Stock actualizado: {nuevo_stock}", foreground="green")
            else:
                self.mensaje.config(text=f"Error: {error}", foreground="red")
        except Exception as e:
            self.mensaje.config(text=f"Error inesperado: {e}", foreground="red")
