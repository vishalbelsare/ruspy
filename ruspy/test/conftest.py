"""This module provides the fixtures for the PYTEST runs."""
import numpy as np
import pytest


@pytest.fixture(scope="module", autouse=True)
def set_seed():
    """Each test is executed with the same random seed."""
    np.random.seed(1223)


@pytest.fixture(scope="session")
def inputs():
    constraints = {"PERIODS": 70000, "BUSES": 200, "discount_factor": 0.9999}
    return constraints
