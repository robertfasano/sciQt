import os
from PyQt5.QtWidgets import QTableWidget, QInputDialog, QLineEdit, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QFont
from sciQt.widgets import DictMenu

class CustomHeader(QHeaderView):
    def __init__(self, table):
        QHeaderView.__init__(self, Qt.Horizontal)
        self.table = table
        self.customContextMenuRequested.connect(table.context_menu)
        self.sectionDoubleClicked.connect(table.update_duration)
        self.setDefaultSectionSize(75+5)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def clone(self):
        ''' Returns a new header sharing the same model. '''
        new_header = CustomHeader(self.table)
        new_header.setModel(self.model())
        return new_header

class TimingTable(QTableWidget):
    ''' A master timing table which shares timestep information and basic
        functionalities with child i/o tables (e.g. TTLTable). '''
    def __init__(self, sequence):
        QTableWidget.__init__(self)
        self.children = []
        self.set_sequence(sequence)
        self.horizontal_margin = 5
        self.label_width = 30
        self.setHorizontalHeader(CustomHeader(self))
        self.hold_column = None
        self.menu = None

    def sizeHint(self):
        ''' Returns a size scaled based on number of columns. '''
        return QSize(self.columnCount()*(75+self.horizontal_margin)+60+self.label_width,
                     400)

    def set_sequence(self, sequence):
        ''' Applies a json-formatted sequence to all child tables. '''
        self.setColumnCount(len(sequence))
        self.setHorizontalHeaderLabels([str(step['duration']) for step in sequence])
        for child in self.children:
            child.set_sequence(sequence)
        self.sequence = sequence

    def get_sequence(self):
        ''' Retrieves subsequences from all child tables and aggregates into
            a master sequence. '''
        sequence = []
        for col in range(self.columnCount()):
            sequence.append({'duration': self.horizontalHeaderItem(col)})
        for child in self.children:
            subsequence = child.get_sequence()
            for i, step in enumerate(subsequence):
                sequence[i].update(step)
        return sequence

    def register(self, child):
        ''' Registers a child widget to inherit from this one. '''
        self.children.append(child)
        child.setHorizontalHeader(self.horizontalHeader().clone())
        child.model = child.horizontalHeader().model()
        self.model().columnsInserted.connect(lambda index, first, last: child.insert_timestep(last))
        self.model().columnsRemoved.connect(lambda index, first, last: child.delete_timestep(last))
        child.set_sequence(self.sequence)
        self.apply_stylesheet(child)

    def insert_timestep(self, col):
        ''' Inserts a timestep after the specified column. '''
        self.insertColumn(col)
        self.setHorizontalHeaderItem(col, QTableWidgetItem('0'))

    def delete_timestep(self, col):
        ''' Deletes a timestep. '''
        self.removeColumn(col)

    def hold(self, col):
        ''' Sets the designated column as the hold column. Passing the same
            column as the hold column will reset the hold column. '''
        if col != self.hold_column:
            self.hold_column = col
        else:
            self.hold_column = None

        for i in range(self.columnCount()):
            if self.hold_column is None:
                self.horizontalHeaderItem(i).setForeground(Qt.black)
                self.horizontalHeaderItem(i).setFont(QFont())
            elif i != self.hold_column:
                self.horizontalHeaderItem(i).setForeground(Qt.gray)
                self.horizontalHeaderItem(i).setFont(QFont())
            else:
                self.horizontalHeaderItem(i).setForeground(Qt.black)
                font = QFont()
                font.setBold(True)
                self.horizontalHeaderItem(i).setFont(font)
                self.setColumnHidden(i, False)

    def context_menu(self, event):
        ''' Handles right-click menu on header items. '''
        col = self.columnAt(event.x())
        actions = {'Insert right': lambda: self.insert_timestep(col+1),
                   'Insert left': lambda: self.insert_timestep(col),
                   'Delete': lambda: self.delete_timestep(col),
                   'Hold': lambda: self.hold(col)}

        self.menu = DictMenu('header options', actions)
        self.menu.actions['Hold'].setCheckable(True)
        self.menu.actions['Hold'].setChecked(col==self.hold_column)
        self.menu.popup(QCursor.pos())

    def update_duration(self, index):
        ''' Popup for timestep duration changes. '''
        old_header = self.horizontalHeaderItem(index).text()
        new_header, updated = QInputDialog.getText(self, 'Duration', '', QLineEdit.Normal, old_header)
        if updated:
            self.horizontalHeaderItem(index).setText(new_header)

    @staticmethod
    def apply_stylesheet(table):
        ''' Applies a generic stylesheet to a target child table. '''
        sciQt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        stylesheet = f"""
        QTableWidget {{color:"#000000";
                      font-weight: light;
                      font-family: "Exo 2";
                      font-size: 14px;
                      gridline-color: transparent;
                      border-right-color: transparent;
                      border-left-color: transparent;
                      border-color: transparent;}}

        """
        table.setStyleSheet(stylesheet)
