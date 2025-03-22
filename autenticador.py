import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import trabajo

# Credenciales fijas en hexadecimal
ussrs = {
    "admn": bytes.fromhex("6d69737472616c").decode('utf-8'),  # mistral
    "usr1": bytes.fromhex("676f6d697461").decode('utf-8')     # gomitas
}

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)

        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)  # Oculta la contraseña
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)

        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.comprobar)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def comprobar(self):
        usuario = self.input_user.text()
        contraseña = self.input_pass.text()

        if usuario in ussrs and contraseña == ussrs[usuario]:
            self.ejecutarInventario(usuario)
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def ejecutarInventario(self, usuario):
        self.close()  # Cierra solo la ventana de login
        self.main_window = trabajo.main(usuario)  # Guardamos la ventana en una variable
                                                  # Necesario para evitar multiples instancias de QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
