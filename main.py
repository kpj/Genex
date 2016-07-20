"""
Main interface of dynamical model optimization
"""

import sys
import pickle

from algorithm import Evolution
from data_generator import generate_data


def main(fname):
    """ Common ground for all modules
    """
    data = generate_data()

    ev = Evolution(40)
    ev.set_data(data)
    pop, df = ev.run(100)

    with open(fname, 'wb') as fd:
        pickle.dump({
            'population': pop,
            'df': df,
            'data': data
        }, fd)

    best, bfit = ev.get_individual(0), ev.get_fitness(0)
    print(bfit, best)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <result file>'.format(sys.argv[0]))
        exit(-1)

    main(sys.argv[1])
