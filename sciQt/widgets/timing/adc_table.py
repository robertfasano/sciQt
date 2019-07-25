''' The ADCTable is a child class of IOTable, providing a grid for defining
    sequences of analog voltage input events. Each item in the grid is an ADCButton
    which, when clicked, opens a dialog box allowing the user to set a sampling
    delay for that timestep. When an ADCButton is queried for its state, it returns
    a dictionary like {'delay': 1e-3} indicating a 1 ms sampling delay.

    A timestep in a sequence might contain a DAC field like 'ADC': {'A': 1e-3},
    indicating that samplerA should be sampled every 1 ms for the duration of
    the timestep.
'''

from PyQt5.QtGui import QCursor
from sciQt.widgets import DictMenu, DictDialog
from sciQt.widgets.timing import IOTable, IOButton
from sciQt.tools import parse_units

class ADCButton(IOButton):
    ''' A widget which allows specification of a sampling rate via a popup dialog. '''
    def __init__(self, channel):
        IOButton.__init__(self, channel, active_color = '#00CCCC')

        self.state = {}
        self.clicked.connect(self.create_event)

    def create_event(self):
        ''' Open a dialog to allow user input of a new frequency and/or attenuation. '''
        state = {'delay': ''}
        state.update(self.state)
        state, updated = DictDialog(state).get_parameters()
        if not updated:
            return
        if state == {}:
            self.set_state('')
        else:
            self.set_state(state['delay'])

    def get_state(self):
        if self.state != {}:
            magnitude, delay = parse_units(self.state['delay'], base_unit='s')
            return {self.channel: magnitude}
        else:
            return {}

    def set_state(self, state):
        ''' Takes a float-valued delay and stores in a state dictionary '''
        string = ''
        if state == '':
            self.state = {}
            self.setProperty('active', False)
        else:
            self.state = {'delay': state}
            magnitude, delay = parse_units(self.state['delay'], base_unit='s')
            string += delay
            self.setProperty('active', True)

        self.setText(string)
        self.setStyle(self.style())

class ADCTable(IOTable):
    ''' A table of buttons allowing specification of sampling for each ADC
        in the passed "adcs" list. '''
    def __init__(self, timing_table, adcs):
        self.button_widget = ADCButton
        IOTable.__init__(self, timing_table, adcs, 'ADC')
