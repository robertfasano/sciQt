''' This script gives a template for a PyQt5 application and showcases the widgets
    included in the sciQt package. '''
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMenuBar, QMenu, QFrame
from PyQt5.QtGui import QFontDatabase
import requests
import os
from abc import abstractmethod
from sciQt import Application

class Frame():
    def __init__(self, parent_layout):
        self.frame = QFrame()
        parent_layout.addWidget(self.frame)
        self.layout = QVBoxLayout()
        self.frame.setLayout(self.layout)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

## define main window
class Dashboard(QMainWindow):
    def __init__(self, title='sciQt'):
        ''' Args:
                title (str): window title
                addr (str): IP address for the backend server
                port (int): port for the backend server
        '''
        self.app = Application()
        super(Dashboard, self).__init__()
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.setCentralWidget(self.widget)

        ## set window style
        self.setWindowTitle(title)
        QFontDatabase.addApplicationFont('resources/fonts/Exo2-Light.ttf')

        sciQt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        stylesheet_path = os.path.join(sciQt_path, 'resources/stylesheets/dashboard.txt')
        with open(stylesheet_path, "r") as file:
            self.setStyleSheet(file.read())

        if os.name == 'nt':
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(title)

        self.buildUI()
        self.show()

        self.app.exec()

    @abstractmethod
    def buildUI(self):
        ''' Overload with custom UI elements '''

    def get(self, url, request = {}, format = 'json'):
        r = requests.get('http://%s:%s/'%(self.addr, self.port)+url)
        if format == 'json':
            return r.json()
        elif format == 'text':
            return r.text
        elif format == 'raw':
            return r.content
