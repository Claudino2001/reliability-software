from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import os
import csv

class RegisterView:
    def __init__(self, manager):
        self.manager = manager
        self.register_view = None
        self.model = QStandardItemModel()
        self.setup_header_table()
        self.metadata = {}
        self.window_title = None

    def load_ui(self, window_title=None, metadata=None):
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
            self.window_title = window_title

        # Verifica se pessou corretamente
        if metadata:
            self.metadata = metadata
            print(f"Metadata received: {self.metadata}")
            self.update_ui_with_metadata()
        
        # Hit QtLineEdit - Configurar os placeholder texts
        self.register_view.inputTEF.setPlaceholderText("e.g., 10,30")
        self.register_view.inputTR.setPlaceholderText("e.g., 0,50")

        # Botão de registrar as infos que estão no inputs
        self.register_view.btnRegister.clicked.connect(self.btn_register)
        
        # Botão de Cancelar. Volta para o MENU. btnCancel
        self.register_view.btnCancel.clicked.connect(self.btn_cancel)
        
        # Botão de Finalizar. Avançar para a analise de adesão
        self.register_view.btnFinish.clicked.connect(self.manager.show_adhesion_view)

        # Botão para limpar todos os dados da TableView "Clear All"
        self.register_view.btnClearAll.clicked.connect(self.btn_clear_all)

        # Botão de SALVAR no menu
        self.register_view.actionSave.triggered.connect(self.action_btn_save)

        # Adiciona validadores para garantir que apenas números flutuantes possam ser inseridos
        double_validator = QtGui.QDoubleValidator()
        double_validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        double_validator.setDecimals(2)  # Define a precisão decimal

        self.register_view.inputTEF.setValidator(double_validator)
        self.register_view.inputTR.setValidator(double_validator)

        self.register_view.show()
    
    def setup_header_table(self):
        self.model.setHorizontalHeaderLabels(['TEF', 'TR', 'Actions'])

    def btn_clear_all(self):
        # Limpa todos os itens do modelo
        self.model.clear()

        # Redefine os cabeçalhos da tabela após limpar
        self.setup_header_table()

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
    
    def load_csv_data(self, csv_path):
        print(f"Loading CSV Data, instance ID: {id(self)}")
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)

                # Ler o nome do projeto
                self.metadata['project_name'] = self.window_title

                # Processa a primeira linha - Tag
                self.metadata['tag'] = next(reader)[0].split(':')[-1].strip()
                
                # Processa a segunda linha - Time unit
                self.metadata['time_unit'] = next(reader)[0].split(':')[-1].strip()

                # Processa a terceira linha - Description
                self.metadata['description'] = next(reader)[0].split(':')[-1].strip()

                print(f'Arquivo aberto corretamente.')
                print(f"Metadata loaded: {self.metadata}")

                next(reader)  # Pula o cabeçalho
                for row in reader:
                    if row:  # Verifica se a linha não está vazia
                        tef, tr = map(float, row[:2])  # Assume que TEF e TR são as duas primeiras colunas
                        self.insere_tempos_na_tabela(tef, tr)
        except Exception as e:
            self.register_view.setWindowTitle('Error')
            QtWidgets.QMessageBox.critical(self.register_view, 'Error', 
                "Failed to load data from CSV file. Please ensure the file is in the correct format and contains valid data.\nError: " + str(e))
            print(str(e))
            self.manager.show_welcome_view()

    def action_btn_save(self):
        print(f"Saving Data, instance ID: {id(self)}")
        print("Salvando os dados...")
        print(f"Metadata loaded: {self.metadata}")

        if not self.metadata.get('project_name'):
            QtWidgets.QMessageBox.warning(self.register_view, 'Error', 'Project name is not set.')
            return

        # Abrir caixa de diálogo para escolher o diretório base
        directory_info = QtWidgets.QFileDialog.getExistingDirectory(self.register_view, "Select Directory")
        if not directory_info:
            return  # Usuário cancelou a operação

        # Montar o caminho completo onde a pasta do projeto será criada
        project_path = os.path.join(directory_info, self.metadata['project_name'])
        os.makedirs(project_path, exist_ok=True)  # Cria o diretório do projeto se ele não existir

        # Definir o caminho completo do arquivo CSV dentro da pasta do projeto
        file_path = os.path.join(project_path, f"{self.metadata['project_name']}.csv")

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Escreve os metadados
                writer.writerow([f'# Tag: {self.metadata["tag"]}'])
                writer.writerow([f'# Time unit: {self.metadata["time_unit"]}'])
                writer.writerow([f'# Description: {self.metadata["description"]}'])
                writer.writerow(['TEF', 'TR'])  # Cabeçalho dos dados

                # Escreve os dados da tabela
                for row in range(self.model.rowCount()):
                    tef_item = self.model.item(row, 0)
                    tr_item = self.model.item(row, 1)
                    if tef_item and tr_item:
                        writer.writerow([tef_item.text(), tr_item.text()])

            QtWidgets.QMessageBox.information(self.register_view, 'Success', f'Data successfully saved to {file_path}.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.register_view, 'Error', f"Failed to save data to CSV file.\nError: {str(e)}")

    def update_ui_with_metadata(self):
        if self.metadata:
            self.register_view.setWindowTitle(self.metadata.get('project_name', 'Default Title'))
            # Aqui você pode atualizar outros elementos da UI, como labels ou campos de texto, com o `metadata`.

    def close(self):
        self.register_view.close()
