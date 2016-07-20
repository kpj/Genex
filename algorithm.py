"""
Definition of the algorithm used for model optimization
"""

import copy
import math
import random

import numpy as np
import pandas as pd

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
        self.elitist_fraction = 0.1
        self.culling_fraction = 0.2

    def set_data(self, data):
        self.op.set_data(data)

    def get_fitness(self, idx):
        return self.population[idx]['fitness']

    def get_individual(self, idx):
        return self.population[idx]['individual']

    def run(self, step_num):
        """ Commence evolution procedure
        """
        self.population = self._initialize()

        df = pd.DataFrame()
        for s in trange(step_num):
            # compute evolutionary step
            self._step()

            # keep some statistics
            if s > step_num / 10:
                for i in range(len(self.population)):
                    df = df.append({
                        'step': s,
                        'fitness': self.get_fitness(i),
                        'expr. depth': np.mean([ind.depth for ind in self.get_individual(i)])
                    }, ignore_index=True)

            # check stopping condition
            self.sort()
            if self.get_fitness(0) < 1e-4:
                break

        self.sort()
        return self.population, df

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

    def _initialize(self, size=None):
        """ Set up initial population
        """
        if size is None:
            size = self.population_size

        return [{
            'individual': self.op.gen_individual(),
            'fitness': None
        } for _ in range(size)]

    def _step(self):
        """ Act out single step of natural selection, etc
        """
        self.sort()
        selection = self._select()
        offspring = self._crossover(selection)
        self._mutate(offspring)

        # be an elitist and keep best individuals
        self.sort()
        elite_num = int(self.elitist_fraction * len(self.population))
        offspring[:elite_num] = self.population[:elite_num]

        self.population[:] = offspring
        self.sort()

        # apply culling
        cull_num = int(self.culling_fraction * len(self.population))
        self.population[-cull_num:] = self._initialize(cull_num)

    def _select(self):
        """ Select individuals from population for crossover
        """
        sel = []

        # choose randomly while favouring fit individuals
        lp = len(self.population) // 2
        for _ in range(lp):
            idx1 = idx2 = int(math.sqrt(random.randrange(lp**2+1)))
            while idx1 == idx2:
                idx2 = int(math.sqrt(random.randrange(lp**2+1)))

            p1, p2 = self.population[idx1], self.population[idx2]
            sel.append((p1, p2))

        return sel

    def _crossover(self, sel):
        """ Crossover given individuals and return offspring
        """
        offspring = []
        for p1, p2 in sel:
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
                    c1 if c1['fitness'] < p1['fitness'] else p1)
                offspring.append(
                    c2 if c2['fitness'] < p2['fitness'] else p2)
            else:
                offspring.extend((p1, p2))
        return offspring

    def _mutate(self, individuals):
        """ Mutate given individuals with some probability
        """
        for cur in individuals:
            if random.random() < self.mutation_probability:
                self.op.mutate(cur['individual'])
                cur['fitness'] = None
