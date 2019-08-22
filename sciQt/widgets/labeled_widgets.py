from PyQt5.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QComboBox, QWidget

class LabeledEdit(QWidget):
    def __init__(self, label, text):
        QWidget.__init__(self)
        self.edit = QLineEdit(text)
        self.label = QLabel(label+':')

        layout = QHBoxLayout(self)
        for w in [self.label, self.edit]:
            layout.addWidget(w)

        self.textChanged = self.edit.textChanged

    def text(self):
        return self.edit.text()

class LabeledComboBox(QWidget):
    def __init__(self, label, options):
        QWidget.__init__(self)
        self.box = QComboBox()
        for op in options:
            self.box.addItem(op)
        self.label = QLabel(label+':')

        layout = QHBoxLayout(self)
        for w in [self.label, self.box]:
            layout.addWidget(w)

        self.setCurrentIndex = self.box.setCurrentIndex
        self.currentTextChanged = self.box.currentTextChanged

    def currentText(self):
        return self.box.currentText()
