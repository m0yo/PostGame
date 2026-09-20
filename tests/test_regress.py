import pytest
from scipy import stats
from minhastats.regress import *

def test_regres_lin_simple():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]

    esperado = stats.linregress(x, y)
    resultado = regress_lin(x, y)

    assert resultado["a"] == pytest.approx(esperado.intercept, abs=1e-6)
    assert resultado["b"] == pytest.approx(esperado.slope, abs=1e-6)
    assert resultado["r"] == pytest.approx(esperado.rvalue, abs=1e-6)

def test_regress_lin_diff(): # teste da regressao linear quando os valores forem diferentes
    with pytest.raises(ValueError):
        regress_lin([1, 2, 3], [1, 2])