# welcome_view.py
from PyQt5 import uic, QtWidgets, QtGui
import os

class WelcomeView:
    def __init__(self, manager):
        self.manager = manager
        self.welcome_view = None

    def load_ui(self):
        ui_path = "./viewspyqt5/welcome.ui"
        absolute_path = os.path.abspath(ui_path)
        self.welcome_view = uic.loadUi(absolute_path)
        icon_path = "./imgs/icone.jpg"
        absolute_icon_path = os.path.abspath(icon_path)
        self.welcome_view.setWindowIcon(QtGui.QIcon(absolute_icon_path))
        self.welcome_view.setFixedSize(800, 600)
        # Botão criar novo projeto
        self.welcome_view.btnNewProject.clicked.connect(self.manager.show_new_project_view)
        # Botão abrir um projeto já existente
        self.welcome_view.btnOpenProject.clicked.connect(self.btn_open_project)
        # Botão de Sair
        self.welcome_view.btnExit.clicked.connect(self.manager.quit_application)
        self.welcome_view.show()

    def close(self):
        self.welcome_view.close()

    def btn_open_project(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do arquivo
        csv_path = QtWidgets.QFileDialog.getOpenFileName(self.welcome_view, "Open CSV File", current_dir, "CSV Files (*.csv)")[0]
        if csv_path:
            file_name = os.path.basename(csv_path)  # Extrai apenas o nome do arquivo com a extensão
            file_name = os.path.splitext(file_name)[0]  # Remove a extensão do arquivo
            self.manager.show_register_view(file_name, csv_path, None)  # Passa o nome do arquivo como título

