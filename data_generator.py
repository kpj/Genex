"""
Generate data which model should be fitted to
"""

import numpy as np
from scipy.integrate import odeint


def simulate(func, dim, resolution=100):
    """ Simulate given ODE
    """
    ts = np.linspace(0, 10, resolution)
    init = [1.8] * dim

    res = odeint(func, init, ts).T

    out = [(cur[0], np.array(cur[1:])) for cur in zip(ts, *res)]
    return out

def generate_data():
    """ Generate data from ODE
    """
    def func(state, t):
        x, y = state
        return np.array([
            1.5 * x - x * y,
            x * y - 3 * y
        ])

    def func(state, t):
        x, y = state
        return np.array([
            x,
            -2
        ])

    return simulate(func, 2)
