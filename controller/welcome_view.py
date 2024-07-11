# welcome_view.py
from PyQt5 import uic, QtWidgets
import os

class WelcomeView:
    def __init__(self, manager):
        self.manager = manager
        self.welcome_view = None

    def load_ui(self):
        ui_path = "./viewspyqt5/welcome.ui"
        absolute_path = os.path.abspath(ui_path)
        self.welcome_view = uic.loadUi(absolute_path)
        self.welcome_view.setFixedSize(800, 600)
        # Botão criar novo projeto
        self.welcome_view.btnNewProject.clicked.connect(self.manager.show_new_project_view)
        # Botão de Sair
        self.welcome_view.btnExit.clicked.connect(self.manager.quit_application)
        self.welcome_view.show()

    def close(self):
        self.welcome_view.close()