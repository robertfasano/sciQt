from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QLineEdit, QInputDialog, QHeaderView, QApplication
from PyQt5.QtCore import Qt, QSize
import json
import os
from sciQt.widgets import DictMenu
from PyQt5.QtGui import QCursor

class TTLTable(QTableWidget):
    def __init__(self, timing_table, ttls):
        QTableWidget.__init__(self)
        self.apply_stylesheet()
        self.setShowGrid(False)
        self.vertical_margin = 5
        self.verticalHeader().setDefaultSectionSize(30+self.vertical_margin)
        self.setSelectionMode(self.NoSelection)
        self.verticalHeader().sectionDoubleClicked.connect(self.changeVerticalHeader)
        self.label_width = 90
        self.verticalHeader().setFixedWidth(self.label_width)
        self.TTLs = ttls
        self.setRowCount(len(self.TTLs))
        self.setVerticalHeaderLabels(self.TTLs)
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(self.verticalHeaderMenuEvent)

        self.timing_table = timing_table
        self.timing_table.register(self)   # apply sequence from master table

        QApplication.processEvents() # necessary to align inherited horizontal header with columns

    def sizeHint(self):
        return QSize(self.columnCount()*(75+self.timing_table.horizontal_margin)+60+self.label_width,
                     self.rowCount()*(30+self.vertical_margin)+80)

    def set_row_state(self, row, state):
        for col in range(self.columnCount()):
            self.cellWidget(row, col).setChecked(state)

    def verticalHeaderMenuEvent(self, event):
        row = self.rowAt(event.y())
        actions = {
                    'Set high': lambda: self.set_row_state(row, True),
                    'Set low': lambda: self.set_row_state(row, False)
                    }
        self.menu = DictMenu('header options', actions)
        self.menu.popup(QCursor.pos())

    def insert_timestep(self, col):
        self.insertColumn(col)
        for row in range(len(self.TTLs)):
            self.setCellWidget(row, col, QCheckBox())
        self.resizeToFit()

    def delete_timestep(self, col):
        self.removeColumn(col)
        self.resizeToFit()

    def changeVerticalHeader(self, index):
        channel = self.verticalHeaderItem(index).text().split(':')[0]
        newHeader, ok = QInputDialog.getText(self, 'Rename TTL channel', '', QLineEdit.Normal,'')
        if ok:
            if newHeader != '':
                self.verticalHeaderItem(index).setText(channel +': '+newHeader)
            else:
                self.verticalHeaderItem(index).setText(channel)

    def get_sequence(self):
        sequence = []
        for i in range(self.columnCount()):
            if self.timing_table.hold_column is not None and self.timing_table.hold_column != i:
                continue
            timestep = {'duration': self.model.headerData(i, Qt.Horizontal)}
            ttls = []
            for j in range(self.rowCount()):
                checkbox = self.cellWidget(j, i)
                if checkbox.isChecked():
                    ttls.append(self.verticalHeaderItem(j).text().split(':')[0])
            if ttls != []:
                timestep['TTL'] = ttls
            sequence.append(timestep)

        return sequence

    def set_sequence(self, sequence):
        self.setColumnCount(len(sequence))

        for i, step in enumerate(sequence):
            for j, ttl in enumerate(self.TTLs):
                self.setCellWidget(j, i, QCheckBox())
                if ttl in step['TTL']:
                    self.cellWidget(j,i).setChecked(True)
                else:
                    self.cellWidget(j,i).setChecked(False)

        # self.resizeToFit()

    def resizeToFit(self):
        self.resize(self.sizeHint())
        if self.parent() is not None:
            self.parent().parent().resize(self.parent().parent().sizeHint())

    def apply_stylesheet(self):
        sciQt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        unchecked_icon_path = os.path.join(sciQt_path, 'resources/icons/unchecked.png').replace('\\', '/')
        checked_icon_path = os.path.join(sciQt_path, 'resources/icons/checked.png').replace('\\', '/')
        stylesheet = f"""

        QCheckBox::indicator:unchecked {{
            image: url({unchecked_icon_path});
        }}

        QCheckBox::indicator:checked {{
            image: url({checked_icon_path});
        }}

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
