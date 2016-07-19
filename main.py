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

    pop = ev.run(100)
    best, bfit = ev.get_individual(0), ev.get_fitness(0)
    print(bfit, best)

    plot_individual(best, ev.op.data)

if __name__ == '__main__':
    main()
