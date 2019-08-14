from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from sciQt import path as sciQt_path

import yaml
import os
with open(os.path.join(sciQt_path, 'palette.yml')) as file:
    palette = yaml.load(file, Loader=yaml.SafeLoader)

class ColorLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        style = ''
        for category in palette:
            for color, hex in palette[category].items():
                name = f'{category}: {color}'
                style += f'QLabel[color="{name}"] {{ background-color : {hex}; }}\n'
        self.setStyleSheet(style)

    def setColor(self, color):
        self.setProperty('color', color)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
