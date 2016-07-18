"""
Definition of the algorithm used for model optimization
"""

import copy
import random

from tqdm import trange

from operators import Operators


class Evolution(object):
    """ Class which handles general evolution activities
    """
    def __init__(self, pop_size):
        self.population_size = pop_size
        self.population = None

        self.op = Operators()
        self.fit = self.op.fitness

        self.mutation_probability = 0.05

    def set_data(self, data):
        self.op.set_data(data)

    def start(self, step_num):
        """ Commence evolution procedure
        """
        self.population = [self.op.gen_individual()
            for _ in range(self.population_size)]

        for s in trange(step_num):
            # compute evolutionary step
            self._step()

            # keep some statistics
            # TODO

        self.population = sorted(self.population, key=self.fit)
        return self.population

    def _step(self):
        """ Act out single step of natural selection, etc
        """
        # mutations
        for ind in self.population:
            if random.random() < self.mutation_probability:
                self.op.mutate(ind)

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
