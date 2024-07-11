# newproject_view.py
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
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
        self.newproject_view.btnBack.clicked.connect(self.btn_voltar)
        # Botão de Criar
        self.newproject_view.btnCreate.clicked.connect(self.btn_criar)
        # Combo box
        self.newproject_view.comboBox.addItems(["days", "hours"])
        self.newproject_view.show()

    def close(self):
        self.newproject_view.close()

    def btn_voltar(self):
        resp = QMessageBox.warning(self.newproject_view, 'Attention', 'Are you sure you want to go back?\nFilled data will be lost.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resp == QMessageBox.Yes:
            print("Usuário confirmou a ação de voltar.")
            self.manager.show_welcome_view()
        else:
            print("Usuário cancelou a ação de voltar.")

    def btn_criar(self):
        self.coleta_infos()
        self.manager.show_register_view(self.nome_do_projeto)

    def coleta_infos(self):
        # inputProjectName
        self.nome_do_projeto = self.newproject_view.inputProjectName.text()
        # inputTag
        tag = self.newproject_view.inputTag.text()
        # Time unit combobox
        unidade_de_tempo = self.newproject_view.comboBox.currentText()
        # inputDesc
        desc = self.newproject_view.inputDesc.toPlainText()
        print(self.nome_do_projeto, tag, unidade_de_tempo, desc)
