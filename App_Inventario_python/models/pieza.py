class Pieza:
    def __init__(self, codigo, nombre, ubicacion, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.stock = stock

    def __repr__(self):
        return f"<Pieza {self.codigo} - {self.nombre}>"
