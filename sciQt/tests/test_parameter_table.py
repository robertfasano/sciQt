from sciQt import ParameterTable, Application
import numpy as np

def test_parametertable_set_parameters(qtbot):
    set_params = {'a': np.random.uniform(), 'b': np.random.uniform()}
    table = ParameterTable(set_params)
    params = table.get_parameters()
    for key in params:
        assert params[key] == set_params[key]
