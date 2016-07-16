"""
Everything plot related
"""

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


def plot_individual(ind, raw_data):
    func = ind.as_lambda()
    t = np.linspace(0, 3, 300)

    plt.figure()

    plt.plot(t, [func(i) for i in t])
    plt.scatter(*zip(*raw_data))
    plt.title(ind.latex_repr())

    plt.show()
