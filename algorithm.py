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
        self.fitness = []
        self.sorted = True
        self.op = Operators()

        self.mutation_probability = 0.05

    def set_data(self, data):
        self.op.set_data(data)

    def start(self, step_num):
        """ Commence evolution procedure
        """
        self.population = [self.op.gen_individual()
            for _ in range(self.population_size)]
        self.sorted = False
        self.fitness = [float('inf')] * len(self.population)

        for s in trange(step_num):
            # compute evolutionary step
            self._step()

            # keep some statistics
            # TODO

        self.sort()
        return self.population

    def sort(self):
        """ Sort population if needed
        """
        if not self.sorted:
            self._recompute_fitness()

            self.population = [ind
                for (fit,ind) in sorted(
                    zip(self.fitness, self.population),
                    key=lambda pair: pair[0])]
            self.fitness = sorted(self.fitness)

            self.sorted = True

    def _recompute_fitness(self):
        """ Recomputes fitness only if needed
        """
        for i, ind_vec in enumerate(self.population):
            if not ind_vec[0].valid_fitness:
                self.fitness[i] = self.op.fitness(ind_vec)

            for ind in ind_vec:
                ind.valid_fitness = True

    def _step(self):
        """ Act out single step of natural selection, etc
        """
        # mutations
        for ind in self.population:
            if random.random() < self.mutation_probability:
                self.op.mutate(ind)
                self.sorted = False

        # crossover
        self.sort()

        offspring = []
        lp = len(self.population) // 2
        for _ in range(lp):
            idx1 = idx2 = int(math.sqrt(random.randrange(lp**2)))
            while idx1 == idx2:
                idx2 = int(math.sqrt(random.randrange(lp**2)))

            p1, p2 = self.population[idx1], self.population[idx2]
            c1, c2 = self.op.crossover(
                copy.deepcopy(p1), copy.deepcopy(p2))
            if not c1 is None and not c2 is None:
                offspring.append(c1 if self.op.fitness(c1) > self.fitness[idx1] else p1)
                offspring.append(c2 if self.op.fitness(c2) > self.fitness[idx2] else p2)
            else:
                offspring.extend((p1, p2))

        self.population[:] = offspring
        self.sorted = False
