from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import os


class RegisterView:
    def __init__(self, manager):
        self.manager = manager
        self.register_view = None
        self.model = QStandardItemModel()
        self.setup_header_table()

    def load_ui(self, window_title=None):
        ui_path = "./viewspyqt5/dataregister.ui"
        absolute_path = os.path.abspath(ui_path)
        self.register_view = uic.loadUi(absolute_path)
        
        # Carrega o icone da janela
        icon_path = "./imgs/icone.jpg"
        absolute_icon_path = os.path.abspath(icon_path)
        self.register_view.setWindowIcon(QtGui.QIcon(absolute_icon_path))
        
        # Define o tamanho da tela
        self.register_view.setFixedSize(800, 600)

        # Configurar a QTableView
        self.register_view.tableView.setModel(self.model)
        
        # Insere como título da janela o nome do projeto fornecido na view anterior
        if window_title:
            self.register_view.setWindowTitle(window_title)
        
        # Hit QtLineEdit - Configurar os placeholder texts
        self.register_view.inputTEF.setPlaceholderText("e.g., 200,10")
        self.register_view.inputTR.setPlaceholderText("e.g., 1700,50")

        # Botão de registrar as infos que estão no inputs
        self.register_view.btnRegister.clicked.connect(self.btn_register)
        
        # Botão de Cancelar. Volta para o MENU. btnCancel
        self.register_view.btnCancel.clicked.connect(self.btn_cancel)
        
        # Botão de Finalizar. Avançar para a analise de adesão
        self.register_view.btnFinish.clicked.connect(self.manager.show_adhesion_view)

        # Adiciona validadores para garantir que apenas números flutuantes possam ser inseridos
        double_validator = QtGui.QDoubleValidator()
        double_validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        double_validator.setDecimals(2)  # Define a precisão decimal

        self.register_view.inputTEF.setValidator(double_validator)
        self.register_view.inputTR.setValidator(double_validator)

        self.register_view.show()
    
    def setup_header_table(self):
        self.model.setHorizontalHeaderLabels(['TEF', 'TR', 'Actions'])


    def btn_cancel(self):
        ## IMPLEMENTAÇÃO DE SE TEM CERTEZA DE VOLTAR PARA O MENU
        reply = QtWidgets.QMessageBox.warning(self.register_view, 'Attention', 'Are you sure you want to go Menu?\nFilled data will be lost.',
                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.manager.show_welcome_view()

    def btn_register(self):
        # inputTEF e inputTR QLineEdit
        
        tef = self.register_view.inputTEF.text().replace('.', '').replace(',', '.')
        tr = self.register_view.inputTR.text().replace('.', '').replace(',', '.')
        
        # Verifica se os campos não estão vazios e não são zero
        if not tef.strip() or not tr.strip():
            QtWidgets.QMessageBox.warning(self.register_view, 'Error', 'Fields cannot be empty.')
            return
        
        try:
            # Converter para float
            tef_float = float(tef)
            tr_float = float(tr)
            
            # Verifica se os valores são diferentes de zero
            if tef_float == 0 or tr_float == 0:
                QtWidgets.QMessageBox.warning(self.register_view, 'Error', 'Values cannot be zero.')
                self.register_view.inputTEF.setText("")
                self.register_view.inputTR.setText("")
                return
            
            print(f"TEF: {tef_float}, TR: {tr_float}")

            self.insere_tempos_na_tabela(float(tef), float(tr))

            self.register_view.inputTEF.clear()
            self.register_view.inputTR.clear()
        except ValueError:
            # Tratar erro se a conversão falhar
            QtWidgets.QMessageBox.warning(self.register_view, 'Error', 'Please enter valid numbers.')
            return
    
    def insere_tempos_na_tabela(self, tef, tr):
        # Cria itens para TEF e TR e configura como não editáveis
        tef_item = QStandardItem(f"{tef:.2f}")
        tr_item = QStandardItem(f"{tr:.2f}")

        # Configura os itens como não editáveis
        tef_item.setFlags(tef_item.flags() & ~Qt.ItemIsEditable)
        tr_item.setFlags(tr_item.flags() & ~Qt.ItemIsEditable)

        # Cria o botão de exclusão
        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(lambda: self.remove_row(self.model.indexFromItem(tef_item).row()))

        # Adiciona os itens ao modelo
        self.model.appendRow([tef_item, tr_item, QStandardItem()])
        self.register_view.tableView.setIndexWidget(self.model.index(self.model.rowCount() - 1, 2), btn_delete)

    def remove_row(self, row):
        self.model.removeRow(row)

    def close(self):
        self.register_view.close()
