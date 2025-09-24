from pyzbar.pyzbar import decode
from PIL import Image

def leer_codigo_barras(imagen_path):
    imagen = Image.open(imagen_path)
    resultados = decode(imagen)
    codigos = [r.data.decode('utf-8') for r in resultados]
    return codigos

# Ejemplo de uso:
# print(leer_codigo_barras('ejemplo.png'))
