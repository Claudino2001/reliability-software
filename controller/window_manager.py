from PyQt5 import QtWidgets
from controller.welcome_view import WelcomeView
from controller.newproject_view import NewProjectView
from controller.register_view import RegisterView
from controller.adesao_view import AdhesionView


class WindowManager:
    def __init__(self, app):
        self.current_window = None
        self.app = app

    def show_welcome_view(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = WelcomeView(self)
        self.current_window.load_ui()

    def show_new_project_view(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = NewProjectView(self)
        self.current_window.load_ui()

    def show_register_view(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = RegisterView(self)
        self.current_window.load_ui()

    def show_adhesion_view(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = AdhesionView(self)
        self.current_window.load_ui()

    def quit_application(self):
        self.app.quit()