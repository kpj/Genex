"""
Analyze result of evolution
"""

import sys
import pickle

import seaborn as sns
import matplotlib.pylab as plt

from core.plot_functions import plot_individual


def evolution_overview(df):
    """ Give overview of development of population
    """
    if not df.empty:
        plt.figure()
        sns.boxplot(x='step', y='fitness', data=df)
        plt.gca().set_yscale('log')
        plt.savefig('images/fitness_evolution.pdf')

        plt.figure()
        sns.boxplot(x='step', y='expr. depth', data=df)
        plt.savefig('images/depth_evolution.pdf')
    else:
        print('[warning] no statistics available')

def main(fname):
    """ Main hub
    """
    with open(fname, 'rb') as fd:
        res = pickle.load(fd)

    evolution_overview(res['df'])
    plot_individual(res['population'][0]['individual'], res['data'])

if __name__ == '__main__':
    sns.set_style('white')
    plt.style.use('seaborn-poster')

    if len(sys.argv) != 2:
        print('Usage: {} <result file>'.format(sys.argv[0]))
        exit(-1)

    main(sys.argv[1])
