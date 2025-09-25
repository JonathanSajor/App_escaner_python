import sqlite3
import os

# Registrar salida de pieza y actualizar stock
def registrar_salida(id_usuario, codigo, descripcion, ubicacion, cantidad, fecha, nombre_tecnico, tipo_salida, maquina):
    conn = get_connection()
    cursor = conn.cursor()
    # Obtener stock actual
    cursor.execute('SELECT stock FROM piezas WHERE codigo = ?', (codigo,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, 'No existe la pieza con ese código.', None
    stock_actual = row[0]
    try:
        cantidad = int(cantidad)
    except Exception:
        conn.close()
        return False, 'Cantidad inválida.', None
    if cantidad > stock_actual:
        conn.close()
        return False, 'No hay suficiente stock.', None
    nuevo_stock = stock_actual - cantidad
    # Actualizar stock
    cursor.execute('UPDATE piezas SET stock = ? WHERE codigo = ?', (nuevo_stock, codigo))
    # Registrar salida
    cursor.execute('''
        INSERT INTO salidas (id_usuario, codigo, descripcion, ubicacion, cantidad, fecha, nombre_tecnico, tipo_salida, maquina)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_usuario, codigo, descripcion, ubicacion, cantidad, fecha, nombre_tecnico, tipo_salida, maquina))
    conn.commit()
    conn.close()
    return True, None, nuevo_stock

# Función para obtener la ubicación de una pieza por su código
def obtener_ubicacion_por_codigo(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT ubicacion FROM piezas WHERE codigo = ?', (codigo,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""
# Obtener nombre de proceso por abreviatura
def obtener_proceso_por_abreviatura(abreviatura):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM procesos WHERE abreviatura = ?', (abreviatura,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""

# Función para verificar si un código de barras ya existe
def existe_codigo(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM piezas WHERE codigo = ?', (codigo,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

# Función para obtener todos los registros de piezas
def obtener_piezas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, codigo, nombre, ubicacion, stock FROM piezas')
    piezas = cursor.fetchall()
    conn.close()
    return piezas

def get_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'inventario.db')
    return sqlite3.connect(db_path)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS piezas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT,
            ubicacion TEXT,
            stock INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            numero_empleado TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS procesos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            abreviatura TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            codigo TEXT,
            descripcion TEXT,
            ubicacion TEXT,
            cantidad INTEGER,
            fecha TEXT,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

# Función para inicializar la tabla procesos con los valores dados
def inicializar_procesos():
    procesos = [
        ("ROD DRAWING", "RD"),
        ("MULTIDRAWING", "MD"),
        ("BUNCHING", "BN"),
        ("EXTRUSION", "EX"),
        ("E-BEAM", "EB"),
        ("REWINDERS", "RW"),
        ("BRAIDERS", "BR"),
        ("TAPING", "TP"),
        ("RECYCLING", "RC"),
        ("GENERIC", "GE"),
        ("SPECIAL CABLE", "SC"),
        ("FLUOR", "FL"),
        ("UTILITIES", "UT"),
        ("TINNED", "TN"),
        ("FOAMING", "FM"),
        ("UPCAST", "UC")
    ]
    conn = get_connection()
    cursor = conn.cursor()
    for nombre, abrev in procesos:
        cursor.execute('''
            INSERT OR IGNORE INTO procesos (nombre, abreviatura) VALUES (?, ?)
        ''', (nombre, abrev))
    conn.commit()
    conn.close()

# Función para registrar una nueva pieza
def registrar_pieza(codigo, nombre, ubicacion, stock):
    if existe_codigo(codigo):
        return False, "El código de barras ya está registrado."
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO piezas (codigo, nombre, ubicacion, stock)
            VALUES (?, ?, ?, ?)
        ''', (codigo, nombre, ubicacion, stock))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    finally:
        conn.close()

# Función para registrar un nuevo usuario/técnico
def registrar_usuario(nombre, numero_empleado, contrasena):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre, numero_empleado, contrasena)
            VALUES (?, ?, ?)
        ''', (nombre, numero_empleado, contrasena))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: usuarios.numero_empleado' in str(e):
            return False, 'El número de empleado ya está registrado.'
        return False, str(e)
    finally:
        conn.close()

# Función para validar usuario (login)
def validar_usuario(numero_empleado, contrasena):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE numero_empleado = ? AND contrasena = ?', (numero_empleado, contrasena))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

if __name__ == "__main__":
    init_db()
    inicializar_procesos()
