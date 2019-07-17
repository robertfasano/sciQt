from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from sciQt.widgets import LabeledEdit, DictDialog
from sciQt.widgets.timing import IOTable, IOButton

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
        self.channels = dds
        self.button_widget = DDSButton
        IOTable.__init__(self, timing_table, dds, 'DDS')
        self.verticalHeader().setDefaultSectionSize(50+self.vertical_margin)
