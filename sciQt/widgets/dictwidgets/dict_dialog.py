from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QDialogButtonBox, QGridLayout
from PyQt5.QtCore import Qt
from sciQt.tools import parse_units

class DictDialog(QDialog):
    def __init__(self, parameters, units=None):
        QDialog.__init__(self)
        if units is None:
            units = {}
        self.units = units
        self.setWindowTitle('Edit parameters')
        layout = QGridLayout(self)
        self.edits = {}
        for row, key in enumerate(parameters):
            self.edits[key] = QLineEdit(str(parameters[key]))
            self.edits[key] = QLineEdit(str(parameters[key]))
            layout.addWidget(QLabel(key), row, 0)
            layout.addWidget(self.edits[key], row, 1)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_parameters(self):
        ''' Open a window, wait for user input, and return the result. '''
        result = self.exec_params()
        parameters = {}
        for key in self.edits:
            if self.edits[key].text() != '':
                parameters[key] = self.edits[key].text()
                if key in self.units:
                    magnitude, parameters[key] = parse_units(parameters[key], self.units[key])
        return (parameters, result == QDialog.Accepted)

    def exec_params(self):
        self.edits[list(self.edits.keys())[0]].selectAll()
        return self.exec_()
