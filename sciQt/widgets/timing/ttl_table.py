from PyQt5.QtGui import QCursor
from sciQt.widgets import DictMenu
from sciQt.widgets.timing import IOTable, IOButton

class TTLButton(IOButton):
    def __init__(self, channel):
        IOButton.__init__(self, channel, active_color = '#ffff00')
        self.channel = channel
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.set_state)

    def get_state(self):
        ''' Returns a list containing either the channel name if checked or nothing
            if unchecked. '''
        if self.isChecked():
            return [self.channel]
        else:
            return []

    def set_state(self):
        self.setProperty('active', self.isChecked())
        self.setStyle(self.style())

class TTLTable(IOTable):
    ''' A table of checkboxes whose state can be mapped to and from a json-formatted
        sequence representation. '''
    def __init__(self, timing_table, ttls):
        self.button_widget = TTLButton
        IOTable.__init__(self, timing_table, ttls, 'TTL')

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
