"""
Everything plot related
"""

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

from data_generator import simulate


def plot_data(data, ax_arr, title=''):
    """ Plot solution of first initial condition
    """
    dim = len(data[0]['data'][0][1])

    for cur_data, ax in zip(data, ax_arr):
        ts = []
        series_vec = [[] for _ in range(dim)]
        for t, state in cur_data['data']:
            ts.append(t)
            for i, val in enumerate(state):
                series_vec[i].append(val)

        for i, series in enumerate(series_vec):
            ax.plot(ts, series, label='Series {}'.format(i))

        ax.set_title(title)
        ax.legend(loc='best')

def plot_individual(ind_vec, orig_data):
    # compute series of individual
    def func(state, t):
        return np.array([ind.as_lambda()(*state) for ind in ind_vec])

    sim_data = []
    for e in orig_data:
        init = e['init']
        sim_data.append({
            'init': init,
            'data': simulate(func, init, 100)
        })

    # plot result
    fig, ax_arr = plt.subplots(
        len(orig_data), 2,
        sharex=True) # sharey=True
    plot_data(
        orig_data, ax_arr[:,0],
        'input data')
    plot_data(
        sim_data, ax_arr[:,1],
        ', '.join([ind.latex_repr() for ind in ind_vec]))

    plt.tight_layout()
    plt.savefig('images/result.pdf')
