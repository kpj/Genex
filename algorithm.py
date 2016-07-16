"""
Definition of the algorithm used for model optimization
"""

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
        self.population = sorted(self.population, key=self.fit)
        p1, p2 = self.population[:2]
        c1, c2 = self.op.crossover(p1, p2)
        if not c1 is None and not c2 is None:
            f1 = self.fit(c1)
            f2 = self.fit(c2)

            if min(f1, f2) > self.fit(self.population[-2]):
                self.population[-2:] = c1, c2
