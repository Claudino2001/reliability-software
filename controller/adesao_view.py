from PyQt5 import uic, QtWidgets
import os

class AdhesionView:
    def __init__(self, manager):
        self.manager = manager
        self.adhesion_view = None

    def load_ui(self):
        ui_path = "./viewspyqt5/adhesiontest.ui"
        absolute_path = os.path.abspath(ui_path)
        self.adhesion_view = uic.loadUi(absolute_path)
        self.adhesion_view.setFixedSize(900, 600)
        # Botão de Sair
        self.adhesion_view.btnExit.clicked.connect(self.manager.show_welcome_view)
        self.adhesion_view.show()

    def close(self):
        self.adhesion_view.close()
