from PyQt5 import uic, QtWidgets
from controller.window_manager import WindowManager
import qdarktheme


app = QtWidgets.QApplication([])
app.setStyleSheet(qdarktheme.load_stylesheet(theme="dark"))

manager = WindowManager(app)
manager.show_welcome_view()

app.exec_()
