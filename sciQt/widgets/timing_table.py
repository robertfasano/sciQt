from PyQt5.QtWidgets import QTableWidget, QInputDialog, QLineEdit, QTableWidgetItem, QHeaderView, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QFont
from sciQt.widgets import DictMenu

class CustomHeader(QHeaderView):
    def __init__(self, table):
        QHeaderView.__init__(self, Qt.Horizontal)
        self.table = table
        self.customContextMenuRequested.connect(table.headerMenuEvent)
        self.sectionDoubleClicked.connect(table.changeHorizontalHeader)
        self.setDefaultSectionSize(75+5)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def clone(self):
        newHeader = CustomHeader(self.table)
        newHeader.setModel(self.model())
        return newHeader

class TimingTable(QTableWidget):
    def __init__(self, sequence):
        QTableWidget.__init__(self)
        self.children = []
        self.set_sequence(sequence)
        self.horizontal_margin = 5
        self.setHorizontalHeader(CustomHeader(self))
        self.hold_column = None

    def set_sequence(self, sequence):
        self.setColumnCount(len(sequence))
        self.setHorizontalHeaderLabels([str(step['duration']) for step in sequence])
        for child in self.children:
            child.set_sequence(sequence)
        self.sequence = sequence

    def get_sequence(self):
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

    def insert_timestep(self, col):
        self.insertColumn(col)
        self.setHorizontalHeaderItem(col, QTableWidgetItem('0'))

    def delete_timestep(self, col):
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

    def headerMenuEvent(self, event):
        col = self.columnAt(event.x())
        actions = {
                    'Insert right': lambda: self.insert_timestep(col+1),
                    'Insert left': lambda: self.insert_timestep(col),
                    'Delete': lambda: self.delete_timestep(col),
                    'Hold': lambda: self.hold(col)
                    }

        self.menu = DictMenu('header options', actions)
        self.menu.actions['Hold'].setCheckable(True)
        self.menu.actions['Hold'].setChecked(col==self.hold_column)
        self.menu.popup(QCursor.pos())

    def changeHorizontalHeader(self, index):
        oldHeader = self.horizontalHeaderItem(index).text()
        newHeader, ok = QInputDialog.getText(self, 'Duration', '', QLineEdit.Normal, oldHeader)
        if ok:
            self.horizontalHeaderItem(index).setText(newHeader)
