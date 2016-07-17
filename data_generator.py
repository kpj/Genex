"""
Generate data which model should be fitted to
"""

import numpy as np
from scipy.integrate import odeint


def simulate(func, init, resolution=50):
    """ Simulate given ODE
    """
    ts = np.linspace(0, 10, resolution)
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

    #def func(state, t):
    #    x, y = state
    #    return np.array([
    #        x,
    #        -2
    #    ])

    out = []
    for init in [(0.5, 0.5), (1, 1), (1.5, 1.5)]:
        out.append({
            'init': init,
            'data': simulate(func, init)
        })
    return out
