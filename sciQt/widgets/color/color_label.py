from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from sciQt.widgets.color import loadPalette, setColor

class ColorLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        loadPalette(self)
        self.setColor = lambda color: setColor(self, color)
        
