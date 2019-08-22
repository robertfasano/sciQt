import os
from PyQt5.QtWidgets import QTableWidget, QTabWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QFont
from sciQt.widgets import DictMenu, DictDialog
from sciQt.widgets.timing import TTLTable, DACTable, DDSTable, ADCTable
from sciQt.tools import parse_units
import numpy as np
from PyQt5.QtWidgets import QLineEdit

class CustomHeader(QHeaderView):
    def __init__(self, table):
        QHeaderView.__init__(self, Qt.Horizontal)
        self.table = table
        self.customContextMenuRequested.connect(table.context_menu)
        self.sectionDoubleClicked.connect(table.update_duration)
        self.setDefaultSectionSize(75+5)
        self.setFixedHeight(35)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def clone(self):
        ''' Returns a new header sharing the same model. '''
        new_header = CustomHeader(self.table)
        new_header.setModel(self.model())
        return new_header

class TimingTable(QTableWidget):
    ''' A master timing table which shares timestep information and basic
        functionalities with child i/o tables (e.g. TTLTable). '''
    def __init__(self, sequence, ttls=None, dacs=None, dds=None, adcs=None, time_unit='s'):
        QTableWidget.__init__(self)
        self.time_unit = time_unit
        self.children = []
        self.set_sequence(sequence)
        self.horizontal_margin = 5
        self.label_width = 35
        self.setHorizontalHeader(CustomHeader(self))
        self.hold_column = None
        self.menu = None

        self.tabs = QTabWidget()
        if ttls is not None:
            self.ttl_table = TTLTable(self, ttls)
            self.tabs.addTab(self.ttl_table, 'TTL')
        if adcs is not None:
            self.adc_table = ADCTable(self, adcs)
            self.tabs.addTab(self.adc_table, 'ADC')
        if dacs is not None:
            self.dac_table = DACTable(self, dacs)
            self.tabs.addTab(self.dac_table, 'DAC')
        if dds is not None:
            self.dds_table = DDSTable(self, dds)
            self.tabs.addTab(self.dds_table, 'DDS')

    @staticmethod
    def apply_stylesheet(table):
        ''' Applies a generic stylesheet to a target child table. '''
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

    def delete_timestep(self, col):
        ''' Deletes a timestep. '''
        self.removeColumn(col)

    def get_sequence(self):
        ''' Retrieves subsequences from all child tables and aggregates into
            a master sequence. '''
        sequence = []
        for col in range(self.columnCount()):
            duration = self.horizontalHeaderItem(col).text().split('\n')[1]
            magnitude, duration = parse_units(duration, base_unit='s')

            name = self.horizontalHeaderItem(col).text().split('\n')[0]
            sequence.append({'duration': magnitude})
            if name != '':
                sequence[-1]['name'] = name
        for child in self.children:
            subsequence = child.get_sequence()
            for i, step in enumerate(subsequence):
                sequence[i].update(step)
        return sequence

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
                # self.setColumnHidden(i, False)

    def insert_timestep(self, col):
        ''' Inserts a timestep after the specified column. '''
        self.insertColumn(col)
        self.setHorizontalHeaderItem(col, QTableWidgetItem('\n0'))

    def register(self, child):
        ''' Registers a child widget to inherit from this one. '''
        self.children.append(child)
        child.setHorizontalHeader(self.horizontalHeader().clone())
        child.model = child.horizontalHeader().model()
        self.model().columnsInserted.connect(lambda index, first, last: child.insert_timestep(last))
        self.model().columnsRemoved.connect(lambda index, first, last: child.delete_timestep(last))
        child.set_sequence(self.sequence)
        self.apply_stylesheet(child)

    def set_sequence(self, sequence):
        ''' Applies a json-formatted sequence to all child tables. '''
        self.setColumnCount(len(sequence))
        labels = []
        for step in sequence:
            header = ''
            if 'name' in step:
                header += step['name']
            magnitude, step['duration'] = parse_units(step['duration'], base_unit='s')

            header += '\n' + str(step['duration'])
            labels.append(header)
        self.setHorizontalHeaderLabels(labels)

        for child in self.children:
            child.set_sequence(sequence)
        self.sequence = sequence

    def sizeHint(self):
        ''' Returns a size scaled based on number of columns. '''
        return QSize(self.columnCount()*(75+self.horizontal_margin)+60+self.label_width,
                     400)

    def update_duration(self, index):
        ''' Popup for timestep duration changes. '''
        old_duration = self.horizontalHeaderItem(index).text().split('\n')[1]
        old_name = self.horizontalHeaderItem(index).text().split('\n')[0]

        parameters = {'Duration': old_duration, 'Name': old_name}
        updates, updated = DictDialog(parameters, units={'Duration': self.time_unit}).get_parameters()
        # magnitude, updates['Duration'] = parse_units(updates['Duration'], base_unit=s)
        if 'Name' not in updates:
            updates['Name'] = ''
        string = f"{updates['Name']}\n{updates['Duration']}"
        if updated:
            self.horizontalHeaderItem(index).setText(string)
