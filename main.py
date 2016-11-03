"""
Main interface of dynamical model optimization
"""

import sys
import pickle

from core.algorithm import Evolution
from core.data_generator import generate_data
from presets.base import load_preset


def main(model_preset, fname):
    """ Common ground for all modules
    """
    pres = load_preset(model_preset)
    if pres is None:
        print('Preset "{}" not found'.format(model_preset))
        exit(-1)
    data = generate_data(pres.get_system(), pres.dim)

    ev = Evolution(40)
    ev.set_data(data)
    ev.set_individual_setter(pres.generate_base_individual)

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
    if len(sys.argv) != 3:
        print('Usage: {} <model preset> <result file>'.format(sys.argv[0]))
        exit(-1)

    main(sys.argv[1], sys.argv[2])
