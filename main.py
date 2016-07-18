"""
Main interface of dynamical model optimization
"""

from algorithm import Evolution
from data_generator import generate_data
from plot_functions import plot_individual


def main():
    """ Common ground for all modules
    """
    data = generate_data()

    ev = Evolution(40)
    ev.set_data(data)

    best, bfit = pop[0], ev.fitness[0]
    print(bfit, best)

    plot_individual(best, ev.op.data)

if __name__ == '__main__':
    main()
