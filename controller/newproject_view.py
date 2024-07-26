# newproject_view.py
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
import os


class NewProjectView:
    def __init__(self, manager):
        self.manager = manager
        self.newproject_view = None
        self.metadata = {'project_name': None,'tag': None, 'time_unit': None, 'description': None}

    def load_ui(self):
        ui_path = "./viewspyqt5/newproject.ui"
        absolute_path = os.path.abspath(ui_path)
        self.newproject_view = uic.loadUi(absolute_path)
        # Carrega o icone da janela
        icon_path = "./imgs/icone.jpg"
        absolute_icon_path = os.path.abspath(icon_path)
        self.newproject_view.setWindowIcon(QtGui.QIcon(absolute_icon_path))
        self.newproject_view.setFixedSize(800, 600)
        # Botão de Voltar
        self.newproject_view.btnBack.clicked.connect(self.btn_voltar)
        # Botão de Criar
        self.newproject_view.btnCreate.clicked.connect(self.btn_criar)
        # Combo box
        self.newproject_view.comboBox.addItems(["days", "hours"])

        # Definindo foco e ordem de tabulação
        self.inputProjectName = self.newproject_view.findChild(QtWidgets.QLineEdit, 'inputProjectName')
        self.inputTag = self.newproject_view.findChild(QtWidgets.QLineEdit, 'inputTag')
        self.comboBox = self.newproject_view.findChild(QtWidgets.QComboBox, 'comboBox')
        self.inputDesc = self.newproject_view.findChild(QtWidgets.QLineEdit, 'inputDesc')
        self.btnCreate = self.newproject_view.findChild(QtWidgets.QPushButton, 'btnCreate')
        self.btnBack = self.newproject_view.findChild(QtWidgets.QPushButton, 'btnBack')

        # Definir foco inicial
        self.inputProjectName.setFocus()

        # Definir ordem de tabulação no contexto de self.newproject_view
        self.newproject_view.setTabOrder(self.inputProjectName, self.inputTag)
        self.newproject_view.setTabOrder(self.inputTag, self.comboBox)
        self.newproject_view.setTabOrder(self.comboBox, self.inputDesc)
        self.newproject_view.setTabOrder(self.inputDesc, self.btnCreate)
        self.newproject_view.setTabOrder(self.btnCreate, self.btnBack)

        self.newproject_view.show()

    def close(self):
        self.newproject_view.close()
    
    def btn_criar(self):
        # Verifica se todos os campos foram devidamente preenchidos antes de prosseguir para a próxima etapa.
        self.coleta_infos()
        if not (self.metadata['project_name'] and self.metadata['tag'] and self.metadata['description']):
            QMessageBox.warning(self.newproject_view, 'Attention', 'Please make sure to fill in all fields before proceeding.', QMessageBox.Ok)
        else:
            self.manager.show_register_view(self.metadata['project_name'], None, self.metadata)

    def btn_voltar(self):
        self.coleta_infos()
        if self.nome_do_projeto != "" or self.tag != "" or self.desc != "":
            resp = QMessageBox.warning(self.newproject_view, 'Attention', 'Are you sure you want to go back?\nFilled data will be lost.', 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resp == QMessageBox.Yes:
                print("Usuário confirmou a ação de voltar.")
                self.manager.show_welcome_view()
            else:
                print("Usuário cancelou a ação de voltar.")
        else:
            self.manager.show_welcome_view()

    def coleta_infos(self):
        # inputProjectName
        self.nome_do_projeto = self.newproject_view.inputProjectName.text()
        self.metadata['project_name'] = self.nome_do_projeto
        # inputTag
        self.tag = self.newproject_view.inputTag.text()
        self.metadata['tag'] = self.tag
        # Time unit combobox
        self.unidade_de_tempo = self.newproject_view.comboBox.currentText()
        self.metadata['time_unit'] = self.unidade_de_tempo
        # inputDesc
        self.desc = self.newproject_view.inputDesc.toPlainText()
        self.metadata['description'] = self.desc
        #print(f'Novo projeto criado com sucesso.\n\tProject name: {self.nome_do_projeto}\n\tTag: {self.tag}\n\tTime unit: {self.unidade_de_tempo}\n\tDescription:{self.desc}')
        print(self.metadata)

