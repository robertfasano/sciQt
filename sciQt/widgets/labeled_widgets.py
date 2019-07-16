from PyQt5.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QComboBox, QWidget

class LabeledEdit(QWidget):
    def __init__(self, label, text):
        QWidget.__init__(self)
        self.edit = QLineEdit(text)
        self.label = QLabel(label+':')

        layout = QHBoxLayout(self)
        for w in [self.label, self.edit]:
            layout.addWidget(w)

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

    def currentText(self):
        return self.box.currentText()
