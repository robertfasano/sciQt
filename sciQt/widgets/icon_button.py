import os
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from sciQt import path as sciQt_path

class IconButton(QToolButton):
    def __init__(self, filename, func, tooltip='', toggle_icon=None):
        super().__init__()
        self.objectName = 'IconButton'
        self.setStyleSheet("IconButton{background-color: rgba(255, 255, 255, 0);border-style: outset; border-width: 0px;}");
        if func is not None:
            self.clicked.connect(func)
        self.icon = self.load_file(filename)
        self.setIcon(self.icon)
        self.setIconSize(QSize(20,20))
        self.setPopupMode(2)
        self.setToolTip(tooltip)

        if toggle_icon is not None:
            self.toggleIcon = QIcon(toggle_icon)
            self.setCheckable(True)
            self.clicked.connect(self.update_icon)

    def update_icon(self):
        if self.isChecked():
            self.setIcon(self.toggleIcon)
        else:
            self.setIcon(self.icon)

    def load_file(self, name):
        icon_path = os.path.join(sciQt_path, 'resources/icons/')
        existing_icons = [x.split('.')[0] for x in os.listdir(icon_path)]
        if name in existing_icons:
            filename = os.path.join(icon_path, name)
        else:
            filename = name
        return QIcon(filename)
