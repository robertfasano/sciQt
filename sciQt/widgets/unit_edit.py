from sciQt.tools import parse_units
import numpy as np
from PyQt5.QtWidgets import QLineEdit

class UnitEdit(QLineEdit):
    def __init__(self, text='', base_unit = 's'):
        super().__init__(text)
        self.base_unit = base_unit
        self.convert_units()
        self.returnPressed.connect(self.convert_units)

    def convert_units(self):
        if self.text() == '':
            return
        magnitude, text = parse_units(self.text(), base_unit = self.base_unit)
        self._setText(text)
        self.magnitude = magnitude

    def setText(self, text):
        self._setText(text)
        self.convert_units()

    def _setText(self, text):
        QLineEdit.setText(self, text)
