from sciQt import TTLTable, Application, TimingTable
import numpy as np
from copy import deepcopy

def test_ttl_table_set_sequence(qtbot):
    ttls =  [f'A{i}' for i in range(0,8)]
    sequence = [{'duration': 0.2, 'TTL': ['A0']}, {'duration': 0.5, 'TTL': ['A1']}]
    timing_table = TimingTable(deepcopy(sequence))
    table = TTLTable(timing_table, ttls)
    get_sequence = timing_table.get_sequence()
    for i, step in enumerate(sequence):
        assert step['duration'] == get_sequence[i]['duration']
