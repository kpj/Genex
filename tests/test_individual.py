from unittest import TestCase

from core.individual import *


class TestUtils(TestCase):
    def test_item_access(self):
        ind = Individual(5., '({})+({})', [
            Individual(-1.6, '({})**2', [
                Individual(2.8, '1', [])
            ]),
            Individual(3.2, '({})*({})', [
                Individual(3.6, '1', []),
                Individual(3.7, '1', [])
            ])
        ])

        self.assertEqual(ind[0].coeff, -1.6)
        self.assertEqual(ind[0].symbol, '({})**2')
        self.assertEqual(len(ind[0].args), 1)

        self.assertEqual(ind[1].coeff, 2.8)
        self.assertEqual(ind[2].coeff, 3.2)
        self.assertEqual(ind[3].coeff, 3.6)
        self.assertEqual(ind[4].coeff, 3.7)

    def test_serialization(self):
        ind = Individual(1, 'VAR_0_')
        self.assertEqual(repr(ind), '<x_0_>')

        ind = Individual(1.1, 'VAR_0_')
        self.assertEqual(repr(ind), '<1.1*x_0_>')

        ind = Individual(-3., 'VAR_0_')
        self.assertEqual(repr(ind), '<-3*x_0_>')

        ind = Individual(-1., 'VAR_0_')
        self.assertEqual(repr(ind), '<-x_0_>')

        ind = Individual(1., '({})+({})', [
            Individual(2., 'VAR_0_'),
            Individual(-.3, 'VAR_1_')
        ])
        self.assertEqual(repr(ind), '<2*x_0_ - 0.3*x_1_>')

        ind = Individual(2., '({})+({})', [
            Individual(2., 'VAR_0_'),
            Individual(-.3, 'VAR_1_')
        ])
        self.assertEqual(repr(ind), '<4*x_0_ - 0.6*x_1_>')

        ind = Individual(1., '({})-({})', [
            Individual(1, '({})*({})', [
                Individual(1., 'VAR_0_'),
                Individual(1., '({})-({})', [
                    Individual(2.3, '1'),
                    Individual(1, 'VAR_2_')
                ])
            ]),
            Individual(-0.5, 'VAR_1_')
        ])
        self.assertEqual(repr(ind), '<x_0_*(-x_2_ + 2.3) + 0.5*x_1_>')
