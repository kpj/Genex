from unittest import TestCase

from individual import *


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
