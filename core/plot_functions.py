"""
Everything plot related
"""

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D # needed for projection='3d'

from .data_generator import simulate


def plot_data(data, ax_arr, title=''):
    """ Plot solution of first initial condition
    """
    dim = len(data[0]['data'][0][1])

    for j, cur_data, ax in zip(range(len(data)), data, ax_arr):
        ts = []
        series_vec = [[] for _ in range(dim)]
        for t, state in cur_data['data']:
            ts.append(t)
            for i, val in enumerate(state):
                series_vec[i].append(val)

        for i, series in enumerate(series_vec):
            ax.plot(ts, series, label='Series {}'.format(i))

        if j == 0:
            ax.set_title(title)
        ax.legend(loc='best')
        ax.set_xlabel(r'$t$')

def plot_data_space(cur_data, ax):
    """ Multi-dimensional plot
    """
    dim = len(cur_data['data'][0][1])

    ts = []
    series_vec = [[] for _ in range(dim)]
    for t, state in cur_data['data']:
        ts.append(t)
        for i, val in enumerate(state):
            series_vec[i].append(val)

    ax.plot(*series_vec)

    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    if dim == 3:
        ax.set_zlabel(r'$z$')

def plot_individual(ind_vec, orig_data):
    # compute series of individual
    def func(state, t):
        return np.array([ind.as_lambda()(*state) for ind in ind_vec])

    sim_data = []
    for e in orig_data:
        init = e['init']
        sim_data.append({
            'init': init,
            'data': simulate(func, init)
        })

    # plot result
    dim = len(orig_data[0]['data'][0][1])
    fig, ax_arr = plt.subplots(
        len(orig_data)+1, 2,
        sharex=True, sharey=True,
        figsize=(13,20))

    plot_data(
        orig_data, ax_arr[:,0],
        'input data')
    plot_data(
        sim_data, ax_arr[:,1],
        '<'+'>\n<'.join([ind.latex_repr() for ind in ind_vec])+'>')

    ax = fig.add_subplot(
        len(orig_data)+1, 2, 7,
        projection='3d' if dim == 3 else None)
    ax_arr[-1,0].axis('off')
    plot_data_space(orig_data[0], ax)

    ax = fig.add_subplot(
        len(orig_data)+1, 2, 8,
        projection='3d' if dim == 3 else None)
    ax_arr[-1,1].axis('off')
    plot_data_space(sim_data[0], ax)

    #plt.tight_layout()
    plt.savefig('images/result.pdf')
