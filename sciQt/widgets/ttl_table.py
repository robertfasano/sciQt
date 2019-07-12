from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QLineEdit, QInputDialog
from PyQt5.QtCore import Qt
import json
import os

class TTLTable(QTableWidget):
    def __init__(self, ttls, sequence=None):
        QTableWidget.__init__(self)
        self.apply_stylesheet()
        self.setShowGrid(False)
        horizontal_margin = 5
        vertical_margin = 5
        self.horizontalHeader().setDefaultSectionSize(75+horizontal_margin)
        self.verticalHeader().setDefaultSectionSize(30+vertical_margin)
        cols = 4
        self.setColumnCount(cols)
        self.setSelectionMode(self.NoSelection)
        self.setHorizontalHeaderLabels([f'{i}' for i in range(cols)])
        self.horizontalHeader().sectionDoubleClicked.connect(self.changeHorizontalHeader)
        self.TTLs = ttls
        self.setRowCount(len(self.TTLs))
        self.setVerticalHeaderLabels(self.TTLs)

        if sequence is not None:
            self.set_sequence(sequence)

    def add_checkbox(self, row, col):
        self.setCellWidget(row, col, QCheckBox())

    def changeHorizontalHeader(self, index):
        oldHeader = self.horizontalHeaderItem(index).text()
        newHeader, ok = QInputDialog.getText(self,
                                                      'Duration',
                                                      '',
                                                       QLineEdit.Normal,
                                                       oldHeader)
        if ok:
            self.horizontalHeaderItem(index).setText(newHeader)

    def get_sequence(self):
        sequence = []
        for i in range(self.columnCount()):
            timestep = {'duration': self.horizontalHeaderItem(i).text()}
            ttls = []
            for j in range(self.rowCount()):
                checkbox = self.cellWidget(j, i)
                if checkbox.isChecked():
                    ttls.append(self.verticalHeaderItem(j).text())
            timestep['TTL'] = ttls

            sequence.append(timestep)

        return sequence

    def set_sequence(self, sequence):
        self.setColumnCount(0)

        for i, step in enumerate(sequence):
            self.insertColumn(i)
            for j, ttl in enumerate(self.TTLs):
                self.add_checkbox(j, i)
                if ttl in step['TTL']:
                    self.cellWidget(j,i).setChecked(True)
                else:
                    self.cellWidget(j,i).setChecked(False)

        self.setHorizontalHeaderLabels([str(step['duration']) for step in sequence])

    def apply_stylesheet(self):
        sciQt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        unchecked_icon_path = os.path.join(sciQt_path, 'resources/icons/unchecked.png').replace('\\', '/')
        checked_icon_path = os.path.join(sciQt_path, 'resources/icons/checked.png').replace('\\', '/')
        stylesheet = f"""

        QCheckBox::indicator:unchecked {{
            image: url({unchecked_icon_path});
        }}

        QCheckBox::indicator:checked {{
            image: url({checked_icon_path});
        }}

        QTableWidget {{color:"#000000";
                      font-weight: light;
                      font-family: "Exo 2";
                      font-size: 14px;
                      gridline-color: transparent;
                      border-right-color: transparent;
                      border-left-color: transparent;
                      border-color: transparent;}}
        """
        self.setStyleSheet(stylesheet)
