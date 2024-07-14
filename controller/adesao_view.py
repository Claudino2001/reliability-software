from PyQt5 import uic, QtWidgets, QtGui
import os
#import numpy as np
#from scipy.stats import norm
#import matplotlib.pyplot as plt
#from reliability.Fitters import Fit_Weibull_2P, Fit_Lognormal_2P
#from utilities.fitting_functions import compare_distributions


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
            #self.gerar_grafico()
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
        tef_data, _ = self.get_data_from_model()  # Asumindo que tef_data é o que você precisa para a análise
        dist, best_distribution = compare_distributions(tef_data, "_time_unit_") # return dist, best_distribution
        print(f"Melhor distribuição: {best_distribution}")
        # Plot aqui ou defina um método para lidar com plotagem em outra parte do código

    
    def get_data_from_model(self):
        tef_data = []
        tr_data = []
        rows = self.model.rowCount()
        for row in range(rows):
            tef_item = self.model.item(row, 0)
            tr_item = self.model.item(row, 1)
            if tef_item and tr_item:
                tef_data.append(float(tef_item.text()))
                tr_data.append(float(tr_item.text()))
        return np.array(tef_data), np.array(tr_data)

    def close(self):
        self.adhesion_view.close()
