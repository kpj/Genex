from unittest import TestCase

from core.individual import Individual
from core.operators import *


class TestCrossover(TestCase):
    def setUp(self):
        self.op = Operators()

    def test_node_exchange(self):
        term1 = Individual(5., '({})+({})', [
            Individual(-1.6, '1', []),
            Individual(3.2, '1', [])
        ])
        term2 = Individual(-9., '({})+({})', [
            Individual(6.1, '1', []),
            Individual(2.2, '1', [])
        ])

        new1, new2 = self.op._exchange_nodes(term1, term2, 0, 1)

        self.assertEqual(new1.coeff, 5)
        self.assertEqual(new1[0].coeff, 2.2)
        self.assertEqual(new1[1].coeff, 3.2)

        self.assertEqual(new2.coeff, -9)
        self.assertEqual(new2[0].coeff, 6.1)
        self.assertEqual(new2[1].coeff, -1.6)
