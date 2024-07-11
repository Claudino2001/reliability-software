# newproject_view.py
from PyQt5 import uic, QtWidgets

import os

class NewProjectView:
    def __init__(self, manager):
        self.manager = manager
        self.newproject_view = None

    def load_ui(self):
        ui_path = "./viewspyqt5/newproject.ui"
        absolute_path = os.path.abspath(ui_path)
        self.newproject_view = uic.loadUi(absolute_path)
        self.newproject_view.setFixedSize(800, 600)
        # Botão de Voltar
        self.newproject_view.btnBack.clicked.connect(self.manager.show_welcome_view)
        # Botão de Criar
        self.newproject_view.btnCreate.clicked.connect(self.manager.show_register_view)

        self.newproject_view.show()

    def close(self):
        self.newproject_view.close()