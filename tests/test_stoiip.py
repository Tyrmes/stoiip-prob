import pytest
from stoiip_prob.stoiip import stoiip


def test_stoiip():
    """"
    This test was done to check if the stooip function
    works perfectly using single variables as its inputs.
    """
    sto = stoiip(250, 40, 0.20, 0.20, 1.24)
    assert sto == pytest.approx(10010322.6, rel=1e-6, abs=1e-12)

