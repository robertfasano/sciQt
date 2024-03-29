''' The DACTable is a child class of IOTable, providing a grid for defining
    sequences of analog voltage outputs. Each item in the grid is a DACButton
    which, when clicked, opens a dialog box allowing the user to set a voltage.
    Set voltages remain constant until another DAC event is reached. When a
    DACButton is queried for its state, it returns a dictionary like {'voltage': 3}
    indicating a 3 V setpoint.

    A timestep in a sequence might contain a DAC field like 'DAC': {'A0': 0, 'A1': 1},
    indicating that channel A0 should be updated to 0 V, channel A1 should be
    updated to 1 V, and all other channels should be unchanged. 
'''
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from sciQt.widgets import LabeledEdit, DictDialog
from sciQt.widgets.timing import IOTable, IOButton
from sciQt.tools import parse_units


class DACButton(IOButton):
    ''' A widget which allows specification of a voltage via a popup dialog. '''
    def __init__(self, channel):
        IOButton.__init__(self, channel, active_color = '#00CCCC')

        self.voltage = ''
        self.state = {}
        self.clicked.connect(self.create_event)

    def create_event(self):
        ''' Open a dialog to allow user input of a new frequency and/or attenuation. '''
        state = {'voltage': ''}
        state.update(self.state)
        state, updated = DictDialog(state).get_parameters()
        if not updated:
            return
        if state == {}:
            self.set_state('')
        else:
            self.set_state(state['voltage'])

    def get_state(self):
        if self.state != {}:
            magnitude, voltage = parse_units(self.state['voltage'], base_unit='V')
            return {self.channel: magnitude}
        else:
            return {}

    def set_state(self, state):
        ''' Takes a float-valued voltage and stores in a state dictionary '''
        string = ''
        if state == '':
            self.state = {}
            self.setProperty('active', False)
        else:
            self.state = {'voltage': state}
            magnitude, voltage = parse_units(self.state['voltage'], base_unit='V')
            string += voltage
            self.setProperty('active', True)

        self.setText(string)
        self.setStyle(self.style())

class DACTable(IOTable):
    ''' A table of buttons allowing specification of voltages for each DAC
        in the passed "dacs" list. '''
    def __init__(self, timing_table, dacs):
        self.button_widget = DACButton
        IOTable.__init__(self, timing_table, dacs, 'DAC')
