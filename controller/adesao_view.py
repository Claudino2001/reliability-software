from PyQt5 import uic, QtWidgets, QtGui
import os

class AdhesionView:
    def __init__(self, manager):
        self.manager = manager
        self.adhesion_view = None
        self.metadata = {}
        self.model = None

    def load_ui(self, metadata, model):
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
        if model:
            self.model = model  # Armazena o modelo recebido
            print('Tabela recebida na tela de adesão')
            print(self.model)
            self.print_model_data()
            self.gerar_grafico()
        # Botão de Sair
        self.adhesion_view.btnExit.clicked.connect(self.manager.show_welcome_view)
        self.adhesion_view.show()

    def update_ui_with_metadata(self):
        if self.metadata:
            self.adhesion_view.setWindowTitle(self.metadata.get('project_name', 'Project name') + ' - Reliability Analysis')
            self.adhesion_view.labelTag.setText(self.metadata.get('tag', 'Error'))
    
    def print_model_data(self):
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        for row in range(rows):
            for col in range(cols):
                item = self.model.item(row, col)
                if item is not None:
                    print(f"Item at row {row}, column {col}: {item.text()}")
                else:
                    print(f"Item at row {row}, column {col} is None")

    def gerar_grafico(self):
        print("Gerando gráfico...")
    
    def close(self):
        self.adhesion_view.close()
