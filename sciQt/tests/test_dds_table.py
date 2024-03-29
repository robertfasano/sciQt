from sciQt import DDSTable, Application, TimingTable
import numpy as np
from copy import deepcopy

def test_dds_table_set_sequence(qtbot):
    dds =  [f'A{i}' for i in range(8)]
    sequence = [{'duration': 0.2, 'DDS': {'A0': {'frequency': 300, 'attenuation': 3}}}, {'duration': 0.5, 'TTL': ['A1']}]
    timing_table = TimingTable(deepcopy(sequence))
    table = DDSTable(timing_table, dds)

    get_sequence = timing_table.get_sequence()
    print(get_sequence)
    for i, step in enumerate(sequence):
        assert step['duration'] == get_sequence[i]['duration']
        if 'DDS' in step:
            assert step['DDS'] == get_sequence[i]['DDS']
