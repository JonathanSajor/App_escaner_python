
# Instrucciones para agentes AI en este proyecto

## Visión general
Este proyecto es una aplicación de escritorio para la gestión de inventario de almacén, basada en Python, con interfaz gráfica (Tkinter), base de datos SQLite y escaneo de códigos de barras (pyzbar). El flujo principal es:

1. Inicio de sesión de usuario (con roles de técnico/administrador)
2. Registro, consulta y salida de piezas mediante código de barras
3. Persistencia y consulta de datos en SQLite

## Estructura y componentes clave
- `main.py`: punto de entrada, inicializa la ventana principal y el login
- `/ui/`: componentes de interfaz (Tkinter), cada ventana/formulario es un archivo
- `/db/`: lógica de acceso y migración de base de datos (`init_db.py`, `migrar_salidas.py`)
- `/barcode/`: utilidades para escaneo de códigos de barras (`scanner.py`)
- `/models/`: clases de dominio (por ejemplo, `usuario.py`, `pieza.py`)
- `requirements.txt`: dependencias (pyzbar, pillow, etc.)

## Flujos y comandos de desarrollo
- Instalar dependencias: `pip install -r requirements.txt`
- Ejecutar la app: `python main.py`
- Migrar base de datos: `python db/migrar_salidas.py`
- La base de datos SQLite se encuentra en `db/inventario.db`

## Patrones y convenciones
- **UI:** Cada ventana principal es una subclase de `tk.Frame` en `/ui/`. Se pasa el `master` y callbacks explícitos para navegación.
- **DB:** Todas las operaciones de base de datos usan funciones en `/db/init_db.py`. No accedas a SQLite directamente desde la UI.
- **Barcode:** El escaneo se realiza con `barcode/scanner.py` usando pyzbar y Pillow. El flujo típico es seleccionar imagen → decodificar → poblar campo de formulario.
- **Modelos:** Clases simples en `/models/` para representar entidades (ejemplo: `Usuario`).
- **No hay framework de tests**: Si agregas tests, colócalos en `/tests/` y documenta el flujo.

## Ejemplo de flujo de registro de pieza
1. Usuario inicia sesión (`ui/inicio_sesion.py`)
2. Accede a ventana principal (`ui/main_window.py`)
3. Llena formulario y puede leer código desde imagen (`barcode/scanner.py`)
4. Al registrar, se llama a función de DB (`db/init_db.py`)

## Integraciones y dependencias
- pyzbar y pillow para escaneo de códigos
- tkinter para UI (incluido en Python estándar)
- sqlite3 para persistencia (incluido en Python estándar)

## Reglas para agentes AI
- Mantén la separación UI/DB/Barcode/Modelos
- No mezcles lógica de negocio en la UI
- Usa funciones existentes de acceso a datos
- Si agregas nuevas ventanas, sigue el patrón de subclase de `tk.Frame` y registra en `main.py`
- Documenta cualquier flujo nuevo en este archivo

---
Última actualización: 25/09/2025
