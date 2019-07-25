from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from sciQt.widgets import LabeledEdit, DictDialog
from sciQt.widgets.timing import IOTable, IOButton
from sciQt.tools import parse_units

class DDSButton(IOButton):
    ''' A widget which allows specification of a frequency and attenuation via a popup dialog. '''
    def __init__(self, channel):
        IOButton.__init__(self, channel, size=(75, 50))
        self.clicked.connect(self.create_event)
        self.state = {}

    def get_state(self):
        ''' Returns a dictionary representing the event state with magnitude scaled
            to the base unit. For example, if the button reads '100 MHz', then this
            method will return {'frequency': 100e6}. '''
        if self.state != {}:
            if 'frequency' in self.state:
                self.state['frequency'], freq_string = parse_units(self.state['frequency'], base_unit='Hz')
            return {self.channel: self.state}
        else:
            return {}

    def set_state(self, state):
        ''' Takes a state dictionary of the form {'frequency': 100e6, 'attenuation': 3}
            and displays a unitful string converted to the most compact representation -
            for example, 100e6 is converted to '100 MHz'. '''
        self.state = state
        string = ''
        if 'frequency' in state:
            magnitude, state['frequency'] = parse_units(state['frequency'], base_unit='Hz')
            string += f"{state['frequency']}"
        if 'attenuation' in state:
            if 'frequency' in state:
                string += '\n'
            string += f"-{state['attenuation']} dB"
        self.setText(string)

        self.setProperty('active', string != '')
        self.setStyle(self.style())

    def create_event(self):
        ''' Open a dialog to allow user input of a new frequency and/or attenuation. '''
        state = {'frequency': '', 'attenuation': ''}
        state.update(self.state)
        state, updated = DictDialog(state).get_parameters()
        if not updated:
            return
        self.set_state(state)

class DDSTable(IOTable):
    ''' A table of buttons allowing specification of settings for each DDS
        in the passed "dds" list. '''
    def __init__(self, timing_table, dds):
        self.button_widget = DDSButton
        IOTable.__init__(self, timing_table, dds, 'DDS')
        self.verticalHeader().setDefaultSectionSize(50+self.vertical_margin)
