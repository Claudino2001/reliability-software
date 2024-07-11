from PyQt5 import uic, QtWidgets
import os

class RegisterView:
    def __init__(self, manager):
        self.manager = manager
        self.register_view = None

    def load_ui(self):
        ui_path = "./viewspyqt5/dataregister.ui"
        absolute_path = os.path.abspath(ui_path)
        self.register_view = uic.loadUi(absolute_path)
        self.register_view.setFixedSize(800, 600)
        # Botão de Cancelar. Volta para o MENU. btnCancel
        self.register_view.btnCancel.clicked.connect()
        self.register_view.show()

    def close(self):
        self.register_view.close()
