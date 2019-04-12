"""
This module contains tests for the simulation process. The setting and the true
results of the simulation are saved in resources/simulation_test/linear_5_agents.pkl.
This module first takes the settings and simulates a dataset. Then the results are
compared to the true saved results.
"""


import pickle
import pytest
from pandas.testing import assert_frame_equal
from numpy.testing import assert_array_equal
from ruspy.simulation.simulation import simulate
from ruspy.ruspy_config import TEST_RESOURCES_DIR


case_1 = pickle.load(open(TEST_RESOURCES_DIR + 'simulation_test/linear_5_agents.pkl',
                          'rb'))

@pytest.fixture
def inputs():
    out = {}
    init_dict = case_1[0]
    out['df'], out['unobs'], out['utilities'], num_states = \
        simulate(init_dict['simulation'])
    return out

@pytest.fixture
def outputs():
    out = {}
    out['df'] = case_1[1]
    out['unobs'] = case_1[2]
    out['utilities'] = case_1[3]
    return out


def test_states(inputs, outputs):
    assert_frame_equal(inputs['df'], outputs['df'])


def test_unobs(inputs, outputs):
    assert_array_equal(inputs['unobs'], outputs['unobs'])


def test_utilities(inputs, outputs):
    assert_array_equal(inputs['utilities'], outputs['utilities'])



