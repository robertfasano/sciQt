from PyQt5.QtWidgets import QTableWidget, QPushButton, QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from sciQt.widgets import DictMenu, LabeledEdit

class DACButton(QPushButton):
    ''' A widget which allows specification of a voltage via a popup dialog. '''
    def __init__(self):
        QPushButton.__init__(self)
        self.clicked.connect(self.create_event)
        self.setFixedSize(75, 30)
        self.voltage = ''

    def create_event(self):
        ''' Open a dialog to allow user input of a new voltage. '''
        dialog = self.Dialog(self)
        voltage, ok = dialog.get_event()
        if not ok:
            return
        self.setText(f'{voltage}')

    class Dialog(QDialog):
        ''' A custom dialog box allowing voltage specification. '''
        def __init__(self, parent):
            QDialog.__init__(self)
            self.parent = parent
            self.setWindowTitle('New DAC event')
            layout = QVBoxLayout(self)

            self.input = LabeledEdit('Voltage', self.parent.voltage)
            layout.addWidget(self.input)

            # OK and Cancel buttons
            buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            buttons.accepted.connect(self.accept)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

        def get_event(self):
            ''' Open a window, wait for user input, and return the result. '''
            result = self.exec_()
            self.parent.voltage = self.input.text()
            return (self.parent.voltage, result == QDialog.Accepted)

class DACTable(QTableWidget):
    ''' A table of buttons allowing specification of voltages for each DAC
        in the passed "dacs" list. '''
    def __init__(self, timing_table, dacs, sequence=None):
        QTableWidget.__init__(self)
        self.dacs = dacs
        self.setShowGrid(False)
        self.horizontal_margin = 5
        self.vertical_margin = 5
        self.verticalHeader().setDefaultSectionSize(30+self.vertical_margin)
        self.setSelectionMode(self.NoSelection)
        self.label_width = timing_table.label_width
        self.verticalHeader().setFixedWidth(self.label_width)

        self.setRowCount(len(self.dacs))
        self.setVerticalHeaderLabels(self.dacs)
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(self.row_context_menu)

        self.hide_inactive = False

        self.timing_table = timing_table
        timing_table.register(self)

    def row_context_menu(self, event):
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
