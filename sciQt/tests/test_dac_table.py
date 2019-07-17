from sciQt import DACTable, Application, TimingTable
import numpy as np

def test_dac_table_set_sequence(qtbot):
    dacs =  [f'A{i}' for i in range(32)]
    sequence = [{'duration': 0.2, 'DAC': {'A0': 1}}, {'duration': 0.5, 'TTL': ['A1']}]
    timing_table = TimingTable(sequence)
    table = DACTable(timing_table, dacs)

    get_sequence = timing_table.get_sequence()

    for i, step in enumerate(sequence):
        assert step['duration'] == get_sequence[i]['duration']
        if 'DAC' in step:
            assert step['DAC'] == get_sequence[i]['DAC']
