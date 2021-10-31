import os, sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebEngineWidgets
import plotly
import multiprocessing

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp/temp.html"))

def save(fig):
    plotly.offline.plot(fig, filename=file_path, auto_open=False)

def view():
    multiprocessing.Process(target=PlotlyViewer).start()

class PlotlyViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        # Create a QApplication instance or use the existing one if it exists
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

        super().__init__()

        self.load(QUrl.fromLocalFile(file_path))
        self.setWindowTitle("Plotly Viewer")
        self.show()

        self.app.exec_()

    @staticmethod
    def closeEvent(_):
        os.remove(file_path)
