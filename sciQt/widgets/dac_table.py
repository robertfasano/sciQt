from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QLineEdit, QInputDialog, QPushButton, QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt, QSize
import json
import os
from sciQt.widgets import DictMenu, LabeledEdit, LabeledComboBox
from PyQt5.QtGui import QCursor, QFont

class DACButton(QPushButton):
    def __init__(self):
        QPushButton.__init__(self)
        self.clicked.connect(self.createEvent)
        self.setFixedSize(75, 30)

    def createEvent(self, parent = None):
        dialog = self.Dialog(self)
        voltage, ok = dialog.getEvent()
        if not ok:
            return
        self.setText(f'{voltage}')

    class Dialog(QDialog):
        def __init__(self, parent):
            QDialog.__init__(self)
            self.setWindowTitle('New DAC event')
            layout = QVBoxLayout(self)

            self.input = LabeledEdit('Voltage', '')
            layout.addWidget(self.input)

            # OK and Cancel buttons
            buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            buttons.accepted.connect(self.accept)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

        def getEvent(self, parent = None):
            result = self.exec_()
            return (self.input.text(), result == QDialog.Accepted)

class DACTable(QTableWidget):
    def __init__(self, timing_table, dacs, sequence=None):
        QTableWidget.__init__(self)
        self.dacs = dacs
        self.apply_stylesheet()
        self.setShowGrid(False)
        self.horizontal_margin = 5
        self.vertical_margin = 5
        self.verticalHeader().setDefaultSectionSize(30+self.vertical_margin)
        self.setSelectionMode(self.NoSelection)
        self.label_width = 90
        self.verticalHeader().setFixedWidth(self.label_width)

        self.setRowCount(len(self.dacs))
        self.setVerticalHeaderLabels(self.dacs)
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(self.headerMenuEvent)

        self.hide_inactive = False

        self.timing_table = timing_table
        timing_table.register(self)

    def headerMenuEvent(self, event):
        col = self.columnAt(event.x())
        actions = {
                    'Hide inactive': lambda: self.hide_inactive_rows(not self.hide_inactive)
                    }

        self.menu = DictMenu('header options', actions)
        self.menu.actions['Hide inactive'].setCheckable(True)
        self.menu.actions['Hide inactive'].setChecked(self.hide_inactive)
        self.menu.popup(QCursor.pos())

    def insert_timestep(self, last):
        self.insertColumn(last)
        for row in range(self.rowCount()):
            self.setCellWidget(row, last, DACButton())

    def delete_timestep(self, last):
        self.removeColumn(last)
        self.resizeToFit()

    def hide_inactive_rows(self, hidden):
        self.hide_inactive = hidden
        for row in range(self.rowCount()):
            inactive = True
            for col in range(self.columnCount()):
                if self.cellWidget(row, col).text() != '':
                    inactive = False
            self.setRowHidden(row, False)
            if inactive:
                self.setRowHidden(row, hidden)

    def get_sequence(self):
        sequence = []
        for i in range(self.columnCount()):
            timestep = {'duration': self.model.headerData(i, Qt.Horizontal)}
            dacs = {}
            for j in range(self.rowCount()):
                edit = self.cellWidget(j, i)
                if edit.text() != '':
                    dacs[self.verticalHeaderItem(j).text()] = float(edit.text())
            if dacs != {}:
                timestep['DAC'] = dacs
            sequence.append(timestep)

        return sequence

    def set_sequence(self, sequence):
        self.setColumnCount(len(sequence))

        for i, step in enumerate(sequence):
            for j, dac in enumerate(self.dacs):
                self.setCellWidget(j, i, DACButton())
                if 'DAC' in step:
                    if dac in step['DAC']:
                        v = step['DAC'][dac]
                        self.cellWidget(j, i).setText(f'{v}')

        self.resizeToFit()

    def resizeToFit(self):
        self.resize(self.sizeHint())
        if self.parent() is not None:
            self.parent().parent().resize(self.parent().parent().sizeHint())

    def sizeHint(self):
        return QSize(self.columnCount()*(75+self.horizontal_margin)+50+self.label_width, self.rowCount()*(30+self.vertical_margin)+80)

    def apply_stylesheet(self):
        sciQt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        stylesheet = f"""
        QTableWidget {{color:"#000000";
                      font-weight: light;
                      font-family: "Exo 2";
                      font-size: 14px;
                      gridline-color: transparent;
                      border-right-color: transparent;
                      border-left-color: transparent;
                      border-color: transparent;}}

        """
        self.setStyleSheet(stylesheet)
