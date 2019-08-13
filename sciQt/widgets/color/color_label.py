from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from sciQt import path as sciQt_path

import yaml
import os
with open(os.path.join(sciQt_path, 'config.yml')) as file:
    palette = yaml.load(file, Loader=yaml.SafeLoader)['palette']

class ColorLabel(QLabel):
    def __init__(self, text, red = '#FF0000', blue='#0000FF', green='#00FF00'):
        super().__init__(text)

        style = f'QLabel[color="red"] {{ background-color : {palette["red"]}; }}\n'
        style += f'QLabel[color="blue"] {{ background-color : {palette["blue"]}; }}\n'
        style += f'QLabel[color="green"] {{ background-color : {palette["green"]}; }}\n'

        self.setStyleSheet(style)

    def setColor(self, color):
        self.setProperty('color', color)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
