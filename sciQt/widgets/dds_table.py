from PyQt5.QtWidgets import QTableWidget, QPushButton, QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from sciQt.widgets import DictMenu, LabeledEdit

class DDSButton(QPushButton):
    ''' A widget which allows specification of a frequency and attenuation via a popup dialog. '''
    def __init__(self, channel):
        QPushButton.__init__(self)
        self.channel = channel
        self.clicked.connect(self.create_event)
        self.setFixedSize(75, 50)
        self.state = {}

    def update_state(self, state):
        self.state = state
        string = ''
        if 'frequency' in state:
            string += f"{state['frequency']} Hz"
        if 'attenuation' in state:
            if 'frequency' in state:
                string += '\n'
            string += f"-{state['attenuation']} dB"
        self.setText(string)

    def create_event(self):
        ''' Open a dialog to allow user input of a new frequency and/or attenuation. '''
        dialog = self.Dialog(self)
        state, ok = dialog.get_event()
        if not ok:
            return
        self.update_state(state)

    class Dialog(QDialog):
        ''' A custom dialog box allowing frequency/attenuation specification. '''
        def __init__(self, parent):
            QDialog.__init__(self)
            self.parent = parent
            self.setWindowTitle('New DDS event')
            layout = QVBoxLayout(self)

            if 'frequency' in self.parent.state:
                frequency_hint = str(self.parent.state['frequency'])
            else:
                frequency_hint = ''

            if 'attenuation' in self.parent.state:
                attenuation_hint = str(self.parent.state['attenuation'])
            else:
                attenuation_hint = ''

            self.frequency = LabeledEdit('Frequency', frequency_hint)
            layout.addWidget(self.frequency)

            self.attenuation = LabeledEdit('Attenuation', attenuation_hint)
            layout.addWidget(self.attenuation)

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
            state = {}
            if self.frequency.text() != '':
                state['frequency'] = float(self.frequency.text())
            if self.attenuation.text() != '':
                state['attenuation'] = float(self.attenuation.text())
            self.parent.state = state
            return state, result == QDialog.Accepted

class DDSTable(QTableWidget):
    ''' A table of buttons allowing specification of settings for each DDS
        in the passed "dds" list. '''
    def __init__(self, timing_table, dds, sequence=None):
        QTableWidget.__init__(self)
        self.dds = dds
        self.setShowGrid(False)
        self.horizontal_margin = 5
        self.vertical_margin = 5
        self.verticalHeader().setDefaultSectionSize(50+self.vertical_margin)
        self.setSelectionMode(self.NoSelection)
        self.label_width = timing_table.label_width
        self.verticalHeader().setFixedWidth(self.label_width)

        self.setRowCount(len(self.dds))
        self.setVerticalHeaderLabels(self.dds)
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
            self.setCellWidget(row, last, DDSButton(self.dds[row]))

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
            dds = {}
            for j in range(self.rowCount()):
                widget = self.cellWidget(j, i)
                if widget.state != {}:
                    dds[self.verticalHeaderItem(j).text()] = widget.state
            if dds != {}:
                timestep['DDS'] = dds
            sequence.append(timestep)

        return sequence

    def set_sequence(self, sequence):
        self.setColumnCount(len(sequence))

        for i, step in enumerate(sequence):
            for j, dds in enumerate(self.dds):
                self.setCellWidget(j, i, DDSButton(dds))
                if 'DDS' in step:
                    if dds in step['DDS']:
                        self.cellWidget(j, i).update_state(step['DDS'][dds])
