from sciQt import DictTable, DictTree
import numpy as np

def test_dicttable_set_parameters(qtbot):
    set_params = {'a': np.random.uniform(), 'b': np.random.uniform()}
    table = DictTable(set_params)
    params = table.get_parameters()
    for key in params:
        assert params[key] == set_params[key]

def test_dicttree_set_model(qtbot):
    set_model = {'a': np.random.uniform(), 'b': {'c': np.random.uniform()}}
    table = DictTree(set_model)
    model = table.get_model()

    assert float(model['a']) == set_model['a']
    assert float(model['b']['c']) == set_model['b']['c']
