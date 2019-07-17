from PyQt5.QtWidgets import QTableWidget, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from sciQt.widgets import DictMenu

class IOTable(QTableWidget):
    def __init__(self, timing_table, channels, io_type):
        QTableWidget.__init__(self)
        self.setRowCount(len(channels))
        self.setVerticalHeaderLabels(channels)
        self.timing_table = timing_table
        self.io_type = io_type
        self.setShowGrid(False)
        self.vertical_margin = 5
        self.verticalHeader().setDefaultSectionSize(30+self.vertical_margin)
        self.setSelectionMode(self.NoSelection)
        ## self.verticalHeader().sectionDoubleClicked.connect(self.rename_channel)
        self.label_width = timing_table.label_width
        self.verticalHeader().setFixedWidth(self.label_width)
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(self.row_context_menu)
        self.timing_table.register(self)
        self.hide_inactive = False

    def delete_timestep(self, col):
        ''' Delete a column '''
        self.removeColumn(col)

    def get_sequence(self):
        sequence = []
        for col in range(self.columnCount()):
            timestep = {'duration': self.model.headerData(col, Qt.Horizontal)}

            channels = {}
            if self.io_type in ['TTL', 'ADC']:
                channels = []
            for row in range(self.rowCount()):
                if self.io_type in ['TTL', 'ADC']:
                    channels.extend(self.cellWidget(row, col).get_state())
                else:
                    channels.update(self.cellWidget(row, col).get_state())

            if len(channels) > 0:
                timestep[self.io_type] = channels

            sequence.append(timestep)
        return sequence

    def hide_inactive_rows(self, hidden):
        self.hide_inactive = hidden
        for row in range(self.rowCount()):
            inactive = True
            for col in range(self.columnCount()):
                if self.cellWidget(row, col).property('active'):
                    inactive = False
            self.setRowHidden(row, False)
            if inactive:
                self.setRowHidden(row, hidden)

    def insert_timestep(self, last):
        self.insertColumn(last)
        for row in range(self.rowCount()):
            ch = self.verticalHeaderItem(row).text()
            self.setCellWidget(row, last, self.button_widget(ch))

    def rename_channel(self, index):
        ''' Open a dialog box to allow a channel to be labeled with extra metadata '''
        channel = self.verticalHeaderItem(index).text().split(':')[0]
        newHeader, updated = QInputDialog.getText(self, 'Rename channel', '', QLineEdit.Normal,'')
        if updated:
            if newHeader != '':
                self.verticalHeaderItem(index).setText(channel +': '+newHeader)
            else:
                self.verticalHeaderItem(index).setText(channel)

    def row_context_menu(self, event):
        actions = {
                    'Hide inactive': lambda: self.hide_inactive_rows(not self.hide_inactive)
                    }

        self.menu = DictMenu('header options', actions)
        self.menu.actions['Hide inactive'].setCheckable(True)
        self.menu.actions['Hide inactive'].setChecked(self.hide_inactive)
        self.menu.popup(QCursor.pos())

    def set_sequence(self, sequence):
        self.setColumnCount(len(sequence))

        for i, step in enumerate(sequence):
            for j, ch in enumerate(self.channels):
                self.setCellWidget(j, i, self.button_widget(ch))
                if self.io_type in step:
                    if self.io_type in ['TTL', 'ADC']:
                        self.cellWidget(j, i).setChecked(ch in step[self.io_type])
                    else:
                        if ch in step[self.io_type]:
                            self.cellWidget(j, i).set_state(step[self.io_type][ch])
