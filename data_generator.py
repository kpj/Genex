"""
Generate data which model should be fitted to
"""

import numpy as np
from scipy.integrate import odeint


def generate_data(resolution=10):
    """ Generate data from ODE
    """
    def func(state, t):
        x, y = state
        return np.array([
            2 * x,
            -5 * y
        ])

    ts = np.linspace(0, 2, resolution)
    init = [1, 1]

    xs, ys = odeint(func, init, ts).T

    #out = [(t, (x, y)) for t, x, y in zip(ts, xs, ys)]
    #return out

    out = [(t, x) for t, x, y in zip(ts, xs, ys)]
    return out
