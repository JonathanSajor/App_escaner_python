import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.init_db import registrar_usuario

class RegistroTecnicoForm(QWidget):
    def __init__(self, registrar_callback=None):
        super().__init__()
        self.setWindowTitle('Registro de Técnico')
        self.registrar_callback = registrar_callback or self.registrar_usuario_db
        self.init_ui()

    def registrar_usuario_db(self, nombre, numero, contrasena):
        return registrar_usuario(nombre, numero, contrasena)

    def init_ui(self):
        layout = QVBoxLayout()

        self.nombre_label = QLabel('Nombre:')
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)

        self.numero_label = QLabel('Número de Empleado:')
        self.numero_input = QLineEdit()
        layout.addWidget(self.numero_label)
        layout.addWidget(self.numero_input)

        self.contrasena_label = QLabel('Contraseña:')
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.contrasena_label)
        layout.addWidget(self.contrasena_input)

        self.registrar_btn = QPushButton('Registrar')
        self.registrar_btn.clicked.connect(self.registrar)
        layout.addWidget(self.registrar_btn)

        self.setLayout(layout)

    def registrar(self):
        nombre = self.nombre_input.text().strip()
        numero = self.numero_input.text().strip()
        contrasena = self.contrasena_input.text().strip()
        if not nombre or not numero or not contrasena:
            QMessageBox.warning(self, 'Campos incompletos', 'Por favor, completa todos los campos.')
            return
        if self.registrar_callback:
            exito, mensaje = self.registrar_callback(nombre, numero, contrasena)
            if exito:
                QMessageBox.information(self, 'Éxito', 'Técnico registrado correctamente.')
                self.close()
            else:
                QMessageBox.warning(self, 'Error', mensaje or 'No se pudo registrar el técnico.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = RegistroTecnicoForm()
    ventana.show()
    sys.exit(app.exec_())
