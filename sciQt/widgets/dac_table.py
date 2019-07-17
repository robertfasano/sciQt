from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from sciQt.widgets import LabeledEdit, IOTable, IOButton

class DACButton(IOButton):
    ''' A widget which allows specification of a voltage via a popup dialog. '''
    def __init__(self, channel):
        IOButton.__init__(self, channel, active_color = '#00CCCC')

        self.voltage = ''
        self.state = {}
        self.clicked.connect(self.create_event)

    def create_event(self):
        ''' Open a dialog to allow user input of a new voltage. '''
        dialog = self.Dialog(self)
        voltage, ok = dialog.get_event()
        if not ok:
            return
        if voltage == '':
            self.set_state(None)
        else:
            self.set_state(float(voltage))

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

    def get_state(self):
        if self.state != {}:
            return {self.channel: self.state['voltage']}
        else:
            return {}

    def set_state(self, state):
        ''' Takes a float-valued voltage and stores in a state dictionary '''
        if state is None:
            self.state = {}
        else:
            self.state = {'voltage': state}
        string = ''

        if 'voltage' in self.state:
            string += f"{self.state['voltage']} V"
            self.setProperty('active', True)
        else:
            self.setProperty('active', False)

        self.setText(string)
        self.setStyle(self.style())

class DACTable(IOTable):
    ''' A table of buttons allowing specification of voltages for each DAC
        in the passed "dacs" list. '''
    def __init__(self, timing_table, dacs):
        self.channels = dacs
        self.button_widget = DACButton
        IOTable.__init__(self, timing_table, dacs, 'DAC')
