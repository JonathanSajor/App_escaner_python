# Proyecto de Inventario de Almacén

Este proyecto es una aplicación de escritorio desarrollada en Python para la gestión de inventario mediante el escaneo de códigos de barras. Incluye:
- Interfaz gráfica con Tkinter
- Base de datos SQLite
- Escaneo de códigos de barras con pyzbar
- Gestión de piezas, usuarios y reportes

## Estructura sugerida
- main.py: punto de entrada de la aplicación
- /db: scripts y archivos de la base de datos
- /ui: componentes de la interfaz gráfica
- /barcode: utilidades para escaneo de códigos
- /models: clases y lógica de negocio
- requirements.txt: dependencias

## Instalación
1. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```
   python main.py
   ```

## Dependencias principales
- pyzbar
- pillow
- tkinter (incluido en la mayoría de instalaciones de Python)
- sqlite3 (incluido en la mayoría de instalaciones de Python)

## Notas
- Se recomienda usar un lector de códigos de barras USB o la cámara web.
- Los módulos y carpetas se crearán en los siguientes pasos.