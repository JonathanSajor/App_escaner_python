import tkinter as tk
from tkinter import ttk, filedialog
import os
import shutil
from db.init_db import registrar_pieza
from barcode.scanner import leer_codigo_barras

class MainWindow(tk.Frame):
    def __init__(self, master=None, id_usuario=None, nombre_usuario=None):
        super().__init__(master)
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Bienvenido al Inventario de Almacén")
        self.label.pack(pady=10)

        # Formulario de registro de pieza
        form_frame = ttk.LabelFrame(self, text="Registrar nueva pieza")
        form_frame.pack(padx=10, pady=10, fill=tk.X)


        etiquetas = ["Código", "descripcion", "Ubicación", "Stock"]
        self.entradas = {}
        for i, campo in enumerate(etiquetas):
            clave = campo.lower().replace('ó', 'o').replace('.', '').replace(' ', '_')
            label = ttk.Label(form_frame, text=campo+":")
            label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entradas[clave] = entry

        # Botón para seleccionar imagen y leer código de barras
        self.boton_imagen = ttk.Button(form_frame, text="Leer código desde imagen", command=self.leer_codigo_desde_imagen)
        self.boton_imagen.grid(row=0, column=2, padx=5, pady=2)

        self.boton_registrar = ttk.Button(form_frame, text="Registrar", command=self.registrar_pieza)
        self.boton_registrar.grid(row=len(etiquetas), column=0, columnspan=3, pady=8)

        self.mensaje = ttk.Label(self, text="")
        self.mensaje.pack(pady=5)

        # Botón para abrir la interfaz de registros creados
        self.boton_ver_registros = ttk.Button(self, text="Ver registros creados", command=self.abrir_lista_piezas)
        self.boton_ver_registros.pack(pady=5)

        # Botón para abrir el formulario de registro de piezas
        self.boton_registro_pieza = ttk.Button(self, text="Registrar movimiento de pieza", command=self.abrir_registro_pieza_form)
        self.boton_registro_pieza.pack(pady=5)

        # Botón para abrir el historial de salidas
        self.boton_historial_salidas = ttk.Button(self, text="Historial de salidas", command=self.abrir_historial_salidas)
        self.boton_historial_salidas.pack(pady=5)

    def abrir_historial_salidas(self):
        from ui.historial_salidas import HistorialSalidas
        if self.id_usuario and self.nombre_usuario:
            HistorialSalidas(self.id_usuario, self.nombre_usuario)
        else:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "No se encontró información de usuario para mostrar el historial.")

    def abrir_registro_pieza_form(self):
        from ui.registro_pieza_form import RegistroPiezaForm
        RegistroPiezaForm(self)

    def abrir_lista_piezas(self):
        from ui.lista_piezas import ListaPiezas
        ListaPiezas(self)

    def leer_codigo_desde_imagen(self):
        archivo = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])
        if archivo:
            codigos = leer_codigo_barras(archivo)
            if codigos:
                codigo = codigos[0]
                if 'codigo' in self.entradas:
                    self.entradas['codigo'].delete(0, tk.END)
                    self.entradas['codigo'].insert(0, codigo)
                    self.mensaje.config(text=f"Código leído: {codigo}", foreground="green")
                else:
                    self.mensaje.config(text="Error interno: campo 'codigo' no encontrado", foreground="red")
                # Guardar imagen en barcode/imagenes con descripcion basado en el código
                destino_dir = os.path.join(os.path.dirname(__file__), '..', 'barcode', 'imagenes')
                destino_dir = os.path.abspath(destino_dir)
                if not os.path.exists(destino_dir):
                    os.makedirs(destino_dir)
                ext = os.path.splitext(archivo)[1]
                destino = os.path.join(destino_dir, f"{codigo}{ext}")
                try:
                    shutil.copy2(archivo, destino)
                except Exception as e:
                    self.mensaje.config(text=f"Imagen no copiada: {e}", foreground="orange")
            else:
                self.mensaje.config(text="No se detectó código de barras en la imagen", foreground="red")



    def registrar_pieza(self):
        datos = {k: v.get() for k, v in self.entradas.items()}
        # Validación simple
        if not all(datos.values()):
            self.mensaje.config(text="Todos los campos son obligatorios", foreground="red")
            return
        try:
            stock = int(datos['stock'])
        except ValueError:
            self.mensaje.config(text="Stock debe ser un número", foreground="red")
            return
        exito, error = registrar_pieza(
            datos['codigo'], datos['descripcion'], datos['ubicacion'], stock
        )
        if exito:
            self.mensaje.config(text="Pieza registrada exitosamente", foreground="green")
            for entry in self.entradas.values():
                entry.delete(0, tk.END)
        else:
            self.mensaje.config(text=f"Error: {error}", foreground="red")
