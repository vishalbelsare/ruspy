"""
This module contains the functions necessary for the estimation process of transition
probabilities.
"""
import numba
import numpy as np


def estimate_transitions(df):
    """
    The sub function for estimating the transition probabilities. This function
    manages the estimation process of the transition probaiblities and calls the
    necessary subfunctions.

    :param df: A pandas dataframe, which contains for each observation the Bus ID,
               the current state of the bus, the current period and the decision made
               in this period.

    :return: The optimization result of the transition probabilities estimation as a
             dictionary.
    """
    result_transitions = {}
    usage = df["usage"].to_numpy(dtype=float)
    usage = usage[~np.isnan(usage)].astype(int)
    transition_count = np.bincount(usage)
    trans_probs = np.array(transition_count) / np.sum(transition_count)
    ll = loglike(trans_probs, transition_count)
    result_transitions.update(
        {"x": trans_probs, "fun": ll, "trans_count": transition_count}
    )
    return result_transitions


def loglike(trans_probs, transition_count):
    """
    The loglikelihood function for estimating the transition probabilities.

    :param trans_probs:      A numpy array containing transition probabilities.
    :param transition_count: A list with the highest state increase as maximal index
                             and the increase counts as entries.

    :return: The negative loglikelihood value for minimizing the second liklihood
             function.
    """
    ll = np.sum(np.multiply(transition_count, np.log(trans_probs)))
    return -ll


@numba.jit(nopython=True)
def create_transition_matrix(num_states, trans_prob):
    """
    This function creates a markov transition matrix. By the assumptions of the
    underlying model, only the diagonal and elements to the right can have a non-zero
    entry.

    :param num_states:  The size of the state space s.
    :type num_states:   int
    :param trans_prob:  A numpy array containing the transition probabilities for a
                        state increase.

    :return: A two dimensional numpy array containing a s x s markov transition matrix.
    """
    trans_mat = np.zeros((num_states, num_states))
    for i in range(num_states):  # Loop over all states.
        for j, p in enumerate(trans_prob):  # Loop over the possible increases.
            if i + j < num_states - 1:
                trans_mat[i, i + j] = p
            elif i + j == num_states - 1:
                trans_mat[i, num_states - 1] = trans_prob[j:].sum()
            else:
                pass
    return trans_mat
