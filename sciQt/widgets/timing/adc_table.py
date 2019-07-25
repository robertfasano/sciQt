''' The ADCTable is a child class of IOTable, providing a grid for defining
    sequences of analog input events. Each item in the grid is a TTLButton, a
    toggleable button with a channel attribute. When a TTLButton is queried for
    its state, it returns either [self.channel] (if active) or [] (if inactive).

    A timestep in a sequence might contain an ADC field like 'ADC': ['A0', 'A1'],
    which indicates that channels A0 and A1 should be measured, while all other
    channels are not measured.

    Note that the Sampler ADC only supports measurement of all 8 channels
    simultaneously, so all channels will be measured if just one is toggled.
    However, in a future update, data from unselected channels will be discarded
    before analysis.

    The sampling rate is currently set internally to be once per ms. In a future
    update, a new ADCButton class will be added, which will allow the user to
    define the sampling rate for each timestep. 
'''
from PyQt5.QtGui import QCursor
from sciQt.widgets import DictMenu
from sciQt.widgets.timing import IOTable, IOButton
from sciQt.widgets.timing.ttl_table import TTLButton

class ADCTable(IOTable):
    ''' A table of checkboxes whose state can be mapped to and from a json-formatted
        sequence representation. '''
    def __init__(self, timing_table, channels):
        self.channels = channels
        self.button_widget = TTLButton
        IOTable.__init__(self, timing_table, channels, 'ADC')

    def row_context_menu(self, event):
        ''' Handle right-click action on a row. '''
        row = self.rowAt(event.y())
        actions = {
                    'Set high': lambda: self.set_row_state(row, True),
                    'Set low': lambda: self.set_row_state(row, False),
                    'Hide inactive': lambda: self.hide_inactive_rows(not self.hide_inactive)
                    }
        self.menu = DictMenu('header options', actions)
        self.menu.actions['Hide inactive'].setCheckable(True)
        self.menu.actions['Hide inactive'].setChecked(self.hide_inactive)
        self.menu.popup(QCursor.pos())

    def set_row_state(self, row, state):
        ''' Set all checkboxes in the specified row to a state (True or False) '''
        for col in range(self.columnCount()):
            self.cellWidget(row, col).setChecked(state)
