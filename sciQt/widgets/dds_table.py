from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from sciQt.widgets import LabeledEdit, IOTable, IOButton

class DDSButton(IOButton):
    ''' A widget which allows specification of a frequency and attenuation via a popup dialog. '''
    def __init__(self, channel):
        IOButton.__init__(self, channel, size=(75, 50))
        self.clicked.connect(self.create_event)
        self.state = {}

    def get_state(self):
        if self.state != {}:
            return {self.channel: self.state}
        else:
            return {}

    def set_state(self, state):
        self.state = state
        string = ''
        if 'frequency' in state:
            string += f"{state['frequency']} Hz"
        if 'attenuation' in state:
            if 'frequency' in state:
                string += '\n'
            string += f"-{state['attenuation']} dB"
        self.setText(string)

        self.setProperty('active', string != '')
        self.setStyle(self.style())

    def create_event(self):
        ''' Open a dialog to allow user input of a new frequency and/or attenuation. '''
        dialog = self.Dialog(self)
        state, ok = dialog.get_event()
        if not ok:
            return
        self.set_state(state)

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

class DDSTable(IOTable):
    ''' A table of buttons allowing specification of settings for each DDS
        in the passed "dds" list. '''
    def __init__(self, timing_table, dds):
        self.channels = dds
        self.button_widget = DDSButton
        IOTable.__init__(self, timing_table, dds, 'DDS')
        self.verticalHeader().setDefaultSectionSize(50+self.vertical_margin)
