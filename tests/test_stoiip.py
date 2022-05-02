import pytest
import numpy as np
from stoiip_prob.model.stoiip import stoiip


def test_stoiip():
    """
    This test was done to check if the stooip function
    works perfectly using single variables as its inputs.
    """
    sto = stoiip(250, 40, 0.20, 0.20, 1.24)
    assert sto == pytest.approx(10010322.6, rel=1e-6, abs=1e-12)


def test_stoiip_arrays():
    """
    This test is used to check if the stooip function works
    perfectly using arrays of different lengths as its inputs.
    """
    area = np.array([450.0, 500.0, 550.0])
    h = np.array([30.0, 40.0, 50.0])
    poro = np.array([0.12, 0.14, 0.16])
    swc = np.array([0.30, 0.35, 0.40])
    boi = np.array([1.01, 1.1, 1.12])

    sto_array = stoiip(area, h, poro, swc, boi)
    assert sto_array == pytest.approx(
        np.array([8710467.33, 12835963.64, 18286714.29]), rel=1e-6, abs=1e-12
    )
