"""
Definitions of evolutionary operators
"""

import copy
import random

import numpy as np

from individual import add_variables, get_symbols
from data_generator import simulate


class Operators(object):
    def __init__(self):
        self.data = None
        self.dim = None

    def set_data(self, data):
        self.data = data
        self.dim = len(data[0]['data'][0][1])

        add_variables(self.dim)

    def gen_individual(self, raw=False):
        """ Generate basic individual
        """
        def gen_one(depth=0):
            if depth == 0:
                ar = 1
            elif depth >= 2:
                ar = 0
            else:
                ar = None

            starter_nodes = list(get_symbols(arity=ar))
            cur = random.choice(starter_nodes)

            for i in range(cur.arity):
                cur._args[i] = gen_one(depth+1)

            return cur

        if raw:
            return gen_one()
        else:
            return [gen_one() for _ in range(self.dim)]

    def fitness(self, ind_vec):
        """ Compute fitness of single individual
        """
        def func(state, t):
            return np.array([ind.as_lambda()(*state) for ind in ind_vec])

        fitn = []
        for e in self.data:
            init = e['init']
            orig_data = e['data']

            try:
                sim_data = simulate(func, init)
            except (ZeroDivisionError, OverflowError, ValueError):
                return float('inf')

            if sim_data is None:
                return float('inf')

            diffs = []
            for (_, sim), (_, orig) in zip(sim_data, orig_data):
                diffs.append(np.mean((sim - orig)**2))
            fitn.append(np.mean(diffs))
        return np.mean(fitn)

    def mutate(self, ind_vec):
        """ Mutate single individual
        """
        for ind in ind_vec:
            c = random.choice(list(ind))
            self._mutate(c)

    def _mutate(self, sub):
        # vary coefficient
        sub._coeff += random.gauss(0, 1)
        if random.random() < 0.1:
            sub._coeff *= -1

        if len(sub) > 10:
            return

        # change function
        if random.random() < 0.5:
            syms = list(get_symbols(arity=len(sub.args), str_frmt=True))
            sub._sym = random.choice(syms)[0]
        else:
            syms = list(get_symbols(arity=None, str_frmt=True))
            sy, ar = random.choice(syms)

            sub._sym = sy
            sub._args = [self.gen_individual(True) for _ in range(ar)]

    def crossover(self, ind1_vec, ind2_vec):
        """ Compute offspring of two individuals
        """
        for i in range(self.dim):
            ind1_vec[i], ind2_vec[i] = self._crossover(ind1_vec[i], ind2_vec[i])

            if ind1_vec[i] is None or ind2_vec[i] is None:
                return None, None

        return ind1_vec, ind2_vec

    def _crossover(self, ind1, ind2):
        if len(ind1) == 1 or len(ind2) == 1:
            cdiff = (ind1.coeff - ind2.coeff)/10
            ind1._coeff -= cdiff
            ind2._coeff += cdiff

            return ind1, ind2
        if ind1.depth >= 5 or ind2.depth >= 5:
            return None, None

        c1 = random.randrange(len(ind1)-1)
        c2 = random.randrange(len(ind2)-1)

        if random.random() < 10.5:
            cdiff = (ind1[c1].coeff - ind2[c2].coeff)/random.randrange(5, 15)
            ind1[c1]._coeff -= cdiff
            ind2[c2]._coeff += cdiff
            return ind1, ind2
        else:
            return self._exchange_nodes(ind1, ind2, c1, c2)

    def _exchange_nodes(self, ind1, ind2, idx1, idx2):
        """ Exchange nodes at indices
        """
        def parse(cur, repl, goal, count=0):
            for i in range(len(cur.args)):
                if count == goal:
                    cur._args[i] = repl
                    return
                count += 1
                parse(cur.args[i], repl, goal, count)

        sub1 = copy.deepcopy(ind1[idx1])
        sub2 = copy.deepcopy(ind2[idx2])

        parse(ind1, sub2, idx1)
        parse(ind2, sub1, idx2)

        return ind1, ind2
