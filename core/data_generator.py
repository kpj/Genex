"""
Generate data which model should be fitted to
"""

import numpy as np
from scipy.integrate import odeint


def simulate(func, init, resolution=50):
    """ Simulate given ODE
    """
    ts = np.linspace(0, 10, resolution)
    raw, info = odeint(func, init, ts, full_output=True)
    res = raw.T

    # TODO: use better check for success
    if info['message'] != 'Integration successful.':
        return None

    out = [(cur[0], np.array(cur[1:])) for cur in zip(ts, *res)]
    return out

def generate_data(func, dim):
    """ Generate data from ODE
    """
    out = []
    for init in [(0.5,)*dim, (1,)*dim, (1.5,)*dim]:
        out.append({
            'init': init,
            'data': simulate(func, init)
        })
    return out
