from PyQt5 import uic, QtWidgets, QtGui
import os

class AdhesionView:
    def __init__(self, manager, model):
        self.manager = manager
        self.adhesion_view = None
        self.metadata = {}
        self.model = model

    def load_ui(self, metadata):
        ui_path = "./viewspyqt5/adhesiontest.ui"
        absolute_path = os.path.abspath(ui_path)
        self.adhesion_view = uic.loadUi(absolute_path)
        # Carrega o icone da janela
        icon_path = "./imgs/icone.jpg"
        absolute_icon_path = os.path.abspath(icon_path)
        self.adhesion_view.setWindowIcon(QtGui.QIcon(absolute_icon_path))
        self.adhesion_view.setFixedSize(900, 600)
        # Verifica se pessou corretamente
        if metadata:
            self.metadata = metadata
            print(f"Adesão View\nMetadata received: {self.metadata}")
            self.update_ui_with_metadata()
        # Recebe o model = Tabela
        if self.model:
            print('Modelo recebido na AdhesionView com os seguintes dados:')
            print(self.model)
            self.print_model_data()
            self.gerar_grafico()
        # Botão de voltar para tela anterior: register_view
        self.adhesion_view.btnBack.clicked.connect(self.btn_voltar)
        # Botão de Sair
        self.adhesion_view.btnExit.clicked.connect(self.manager.show_welcome_view)
        self.adhesion_view.show()

    def update_ui_with_metadata(self):
        if self.metadata:
            self.adhesion_view.setWindowTitle(self.metadata.get('project_name', 'Project name') + ' - Reliability Analysis')
            self.adhesion_view.labelTag.setText(self.metadata.get('tag', 'Error'))
    
    def print_model_data(self):
        rows = self.model.rowCount()
        for row in range(rows):
            tef_item = self.model.item(row, 0)
            tr_item = self.model.item(row, 1)
            print(f"Row {row}: TEF = {tef_item.text() if tef_item else 'N/A'}, TR = {tr_item.text() if tr_item else 'N/A'}")
    
    def btn_voltar(self):
        print("Voltando para a tela de registro.")
        self.manager.show_register_view(window_title=self.metadata.get('project_name', 'Project name'), metadata=self.metadata)

    def gerar_grafico(self):
        print("Gerando gráfico...")
    
    def close(self):
        self.adhesion_view.close()
