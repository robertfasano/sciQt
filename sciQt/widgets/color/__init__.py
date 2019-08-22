import yaml
import os
from sciQt import path as sciQt_path

def loadPalette(self):
    with open(os.path.join(sciQt_path, 'palette.yml')) as file:
        palette = yaml.load(file, Loader=yaml.SafeLoader)
    style = ''
    for category in palette:
        for color, hex in palette[category].items():
            name = f'{category}: {color}'
            style += f'QLabel[color="{name}"] {{ background-color : {hex}; }}\n'
    self.setStyleSheet(style)

def load_palette_options():
    with open(os.path.join(sciQt_path, 'palette.yml')) as file:
        palette = yaml.load(file, Loader=yaml.SafeLoader)
    options = []
    for category in palette:
        for color, hex in palette[category].items():
            options.append(f'{category}: {color}')
    return options

def setColor(self, color):
    self.setProperty('color', color)
    self.style().unpolish(self)
    self.style().polish(self)
    self.update()

from .color_label import ColorLabel
