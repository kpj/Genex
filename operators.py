"""
Definitions of evolutionary operators
"""

import copy
import random

from individual import get_symbols, Individual


class Operators(object):
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data

    def gen_individual(self):
        """ Generate basic individual
        """
        def gen_one(depth=0):
            if depth == 0:
                ar = 1
            elif depth >= 4:
                ar = 0
            else:
                ar = None

            starter_nodes = list(get_symbols(arity=ar))
            cur = random.choice(starter_nodes)

            for i in range(cur.arity):
                cur._args[i] = gen_one(depth+1)

            return cur

        return gen_one()

    def fitness(self, ind):
        """ Compute fitness of single individual
        """
        func = ind.as_lambda()

        try:
            return sum([(y - func(x))**2 for x, y in self.data])/len(self.data)
        except (ZeroDivisionError, OverflowError, ValueError):
            return float('inf')

    def mutate(self, ind):
        """ Mutate single individual
        """
        def _mutate(sub):
            # vary coefficient
            sub._coeff += random.gauss(0, 1)
            if random.random() < 0.1:
                sub._coeff *= -1

            if len(sub) > 10:
                return

            # change function
            if random.random() < 0.9:
                syms = list(get_symbols(arity=len(sub.args), str_frmt=True))
                sub._sym = random.choice(syms)[0]
            else:
                syms = list(get_symbols(arity=None, str_frmt=True))
                sy, ar = random.choice(syms)

                sub._sym = sy
                sub._args = [Individual() for _ in range(ar)]

        c = random.choice(list(ind))
        _mutate(c)

    def crossover(self, ind1, ind2):
        """ Compute offspring of two individuals
        """
        if len(ind1) == 1 or len(ind2) == 1:
            return None, None
        if len(ind1) >= 10 or len(ind2) >= 10:
            return None, None

        c1 = random.randint(1, len(ind1)-1)
        c2 = random.randint(1, len(ind2)-1)

        foo1 = copy.deepcopy(ind1[c1])
        foo2 = copy.deepcopy(ind2[c2])

        def parse(cur, repl, goal, count=1):
            for i in range(len(cur.args)):
                if count == goal:
                    cur._args[i] = repl
                count += 1
                parse(cur._args[i], repl, goal, count)

        parse(ind1, foo2, c1)
        parse(ind2, foo1, c2)

        return ind1, ind2
