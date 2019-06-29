from sciQt import DictTree
import numpy as np

def test_dicttree_set_model(qtbot):
    set_model = {'a': np.random.uniform(), 'b': {'c': np.random.uniform()}}
    table = DictTree(set_model)
    model = table.get_model()

    assert float(model['a']) == set_model['a']
    assert float(model['b']['c']) == set_model['b']['c']
