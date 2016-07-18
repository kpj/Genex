"""
Definition of the algorithm used for model optimization
"""

import copy
import math
import random

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pylab as plt

from tqdm import trange

from operators import Operators


class Evolution(object):
    """ Class which handles general evolution activities
    """
    def __init__(self, pop_size):
        self.population_size = pop_size

        self.population = []
        self.op = Operators()

        self.mutation_probability = 0.05

    def set_data(self, data):
        self.op.set_data(data)

    def get_fitness(self, idx):
        return self.population[idx]['fitness']

    def get_individual(self, idx):
        return self.population[idx]['individual']

    def start(self, step_num):
        """ Commence evolution procedure
        """
        self.population = [{
            'individual': self.op.gen_individual(),
            'fitness': None
        } for _ in range(self.population_size)]

        df = pd.DataFrame()
        for s in trange(step_num):
            # compute evolutionary step
            self._step()

            # keep some statistics
            for i in range(len(self.population)):
                df = df.append({
                    'step': s,
                    'fitness': self.get_fitness(i)
                }, ignore_index=True)

        #df.set_index('step', inplace=True)
        sns.boxplot(x='step', y='fitness', data=df)
        #plt.gca().set(yscale='log')

        self.sort()
        return self.population

    def sort(self):
        """ Sort population
        """
        self._recompute_fitness()
        self.population = sorted(self.population, key=lambda e: e['fitness'])

    def _recompute_fitness(self):
        """ Recomputes fitness only if needed
        """
        for cur in self.population:
            if cur['fitness'] is None:
                cur['fitness'] = self.op.fitness(cur['individual'])

    def _step(self):
        """ Act out single step of natural selection, etc
        """
        # mutations
        for cur in self.population:
            if random.random() < self.mutation_probability:
                self.op.mutate(cur['individual'])
                cur['fitness'] = None

        # crossover
        self.sort()

        offspring = []
        lp = len(self.population) // 2
        for _ in range(lp):
            idx1 = idx2 = int(math.sqrt(random.randrange(lp**2)))
            while idx1 == idx2:
                idx2 = int(math.sqrt(random.randrange(lp**2)))

            p1, p2 = self.population[idx1], self.population[idx2]
            tmp = self.op.crossover(
                copy.deepcopy(p1['individual']),
                copy.deepcopy(p2['individual']))

            if not tmp[0] is None and not tmp[1] is None:
                c1 = {
                    'individual': tmp[0],
                    'fitness': self.op.fitness(tmp[0])
                }
                c2 = {
                    'individual': tmp[1],
                    'fitness': self.op.fitness(tmp[1])
                }

                offspring.append(
                    c1 if c1['fitness'] > p1['fitness'] else p1)
                offspring.append(
                    c2 if c2['fitness'] > p2['fitness'] else p2)
            else:
                offspring.extend((p1, p2))

        self.population[:] = offspring
