import sqlite3
import os

def migrar_salidas():
    db_path = os.path.join(os.path.dirname(__file__), 'inventario.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    columnas = [
        ("nombre_tecnico", "TEXT"),
        ("tipo_salida", "TEXT"),
        ("maquina", "TEXT")
    ]
    for nombre, tipo in columnas:
        try:
            cursor.execute(f"ALTER TABLE salidas ADD COLUMN {nombre} {tipo}")
            print(f"Columna '{nombre}' agregada.")
        except sqlite3.OperationalError as e:
            if f"duplicate column name: {nombre}" in str(e) or f"already exists" in str(e):
                print(f"La columna '{nombre}' ya existe.")
            else:
                print(f"Error al agregar columna '{nombre}': {e}")
    conn.commit()
    conn.close()
    print("Migración completada.")

if __name__ == "__main__":
    migrar_salidas()
