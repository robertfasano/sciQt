from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QDialogButtonBox, QGridLayout
from PyQt5.QtCore import Qt

class DictDialog(QDialog):
    def __init__(self, parameters):
        QDialog.__init__(self)
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
        result = self.exec_()
        parameters = {}
        for key in self.edits:
            parameters[key] = self.edits[key].text()
        return (parameters, result == QDialog.Accepted)
