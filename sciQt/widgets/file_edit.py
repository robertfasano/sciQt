from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QFileDialog
from sciQt.widgets import IconButton

class FileEdit(QWidget):
    ''' A line edit with file dialog extension '''
    def __init__(self, name, default_path, type='file', extension=''):
        QWidget.__init__(self)
        layout = QHBoxLayout(self)
        self.path = default_path
        layout.addWidget(QLabel(name))
        self.edit = QLineEdit(default_path)
        self.textChanged = self.edit.textChanged
        self.text = self.edit.text
        layout.addWidget(self.edit)
        if type == 'folder':
            button = IconButton('load', self.load_folder)
        elif type == 'file':
            button = IconButton('load', self.load_file)
        layout.addWidget(button)
        self.extension = extension

    def load_folder(self):
        filename = QFileDialog.getExistingDirectory(self, 'Choose folder', self.path)
        self.edit.setText(filename)

    def load_file(self):
        filter = f"*{self.extension}"
        filename = QFileDialog.getOpenFileName(self, 'Choose file', self.path, filter)[0]
        self.edit.setText(filename)
