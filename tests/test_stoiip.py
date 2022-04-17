import pytest
from stoiip_prob import stoiip as stp


def test_stoiip():
    sto = stp.stoiip(250, 40, 0.20, 0.20, 1.24)
    assert sto == 10010322.6

