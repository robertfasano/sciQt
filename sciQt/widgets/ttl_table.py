from PyQt5.QtWidgets import QTableWidget, QCheckBox, QLineEdit, QInputDialog, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from sciQt.widgets import DictMenu

class TTLTable(QTableWidget):
    ''' A table of checkboxes whose state can be mapped to and from a json-formatted
        sequence representation. '''
    def __init__(self, timing_table, ttls):
        QTableWidget.__init__(self)
        self.setShowGrid(False)
        self.vertical_margin = 5
        self.verticalHeader().setDefaultSectionSize(30+self.vertical_margin)
        self.setSelectionMode(self.NoSelection)
        # self.verticalHeader().sectionDoubleClicked.connect(self.rename_channel)
        self.label_width = timing_table.label_width
        self.verticalHeader().setFixedWidth(self.label_width)
        self.TTLs = ttls
        self.setRowCount(len(self.TTLs))
        self.setVerticalHeaderLabels(self.TTLs)
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(self.row_context_menu)

        self.timing_table = timing_table
        self.timing_table.register(self)   # apply sequence from master table

    def set_row_state(self, row, state):
        ''' Set all checkboxes in the specified row to a state (True or False) '''
        for col in range(self.columnCount()):
            self.cellWidget(row, col).setChecked(state)

    def row_context_menu(self, event):
        ''' Handle right-click action on a row. '''
        row = self.rowAt(event.y())
        actions = {
                    'Set high': lambda: self.set_row_state(row, True),
                    'Set low': lambda: self.set_row_state(row, False)
                    }
        self.menu = DictMenu('header options', actions)
        self.menu.popup(QCursor.pos())

    def insert_timestep(self, col):
        ''' Add a new column of checkboxes '''
        self.insertColumn(col)
        for row in range(len(self.TTLs)):
            self.setCellWidget(row, col, QCheckBox())

    def delete_timestep(self, col):
        ''' Delete a column '''
        self.removeColumn(col)

    def rename_channel(self, index):
        ''' Open a dialog box to allow a channel to be labeled with extra metadata '''
        channel = self.verticalHeaderItem(index).text().split(':')[0]
        newHeader, updated = QInputDialog.getText(self, 'Rename TTL channel', '', QLineEdit.Normal,'')
        if updated:
            if newHeader != '':
                self.verticalHeaderItem(index).setText(channel +': '+newHeader)
            else:
                self.verticalHeaderItem(index).setText(channel)

    def get_sequence(self):
        ''' Returns a json-formatted sequence from the checkbox states. '''
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
        ''' Maps a json-formatted sequence to checkbox states. For example, if
            the sequence contains a timestep {'duration': 1, 'TTL' ['A1']}, then
            the checkbox in the column corresponding to the step and the row
            corresponding to TTL A1 will be checked. '''
        self.setColumnCount(len(sequence))

        for i, step in enumerate(sequence):
            for j, ttl in enumerate(self.TTLs):
                self.setCellWidget(j, i, QCheckBox())
                if ttl in step['TTL']:
                    self.cellWidget(j,i).setChecked(True)
                else:
                    self.cellWidget(j,i).setChecked(False)
