from sciQt import TTLTable, Application
import numpy as np

def test_ttl_table_set_sequence(qtbot):
    ttls =  [f'A{i}' for i in range(0,8)]
    sequence = [{'duration': 0.2, 'TTL': ['A0']}, {'duration': 0.5, 'TTL': ['A1']}]
    table = TTLTable(ttls, sequence=sequence)
    get_sequence = table.get_sequence()
    for i, step in enumerate(sequence):
        assert str(step['duration']) == get_sequence[i]['duration']
