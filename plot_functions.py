"""
Everything plot related
"""

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

from data_generator import simulate


def plot_data(data, ax, title=''):
    dim = len(data[0][1])

    ts = []
    series_vec = [[] for _ in range(dim)]
    for t, state in data:
        ts.append(t)
        for i, val in enumerate(state):
            series_vec[i].append(val)

    for i, series in enumerate(series_vec):
        ax.plot(ts, series, label='Series {}'.format(i))

    ax.set_title(title, fontsize=32)
    ax.legend(loc='best')

def plot_individual(ind_vec, orig_data):
    def func(state, t):
        return np.array([ind.as_lambda()(*state) for ind in ind_vec])
    sim_data = simulate(func, len(orig_data[0][1]), 100)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    plot_data(
        orig_data, ax1,
        'input data')
    plot_data(
        sim_data, ax2,
        ', '.join([ind.latex_repr() for ind in ind_vec]))
    plt.show()
