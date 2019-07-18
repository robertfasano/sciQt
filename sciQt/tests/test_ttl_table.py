from sciQt import TTLTable, Application, TimingTable
import numpy as np
from copy import deepcopy
from PyQt5.QtCore import Qt

def test_ttl_table_set_sequence(qtbot):
    ttls =  [f'A{i}' for i in range(0,8)]
    sequence = [{'duration': 0.2, 'TTL': ['A0']}, {'duration': 0.5, 'TTL': ['A1']}]
    timing_table = TimingTable(deepcopy(sequence), ttls=ttls)

    get_sequence = timing_table.get_sequence()

    for i, step in enumerate(sequence):
        assert step['duration'] == get_sequence[i]['duration']
        assert step['TTL'] == get_sequence[i]['TTL']

def test_ttl_table_user_clicks(qtbot):
    ''' Simulate user clicks to swap TTLs '''
    ttls =  [f'A{i}' for i in range(0,8)]
    sequence = [{'duration': 0.2, 'TTL': ['A0']}, {'duration': 0.5, 'TTL': ['A1']}]
    timing_table = TimingTable(deepcopy(sequence), ttls=ttls)

    table = timing_table.ttl_table
    for row in [0, 1]:
        for col in [0, 1]:
            qtbot.mouseClick(table.cellWidget(row, col), Qt.LeftButton)

    new_sequence = [{'duration': 0.2, 'TTL': ['A1']}, {'duration': 0.5, 'TTL': ['A0']}]
    get_new_sequence = timing_table.get_sequence()

    for i, step in enumerate(new_sequence):
        assert step['TTL'] == get_new_sequence[i]['TTL']
