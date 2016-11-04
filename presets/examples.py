import random

import numpy as np

from core.individual import Individual
from .base import BasePreset


class LotkaVolterra(BasePreset):
    """ Ecological (non-dimensional) Lotka-Volterra equations
    """
    def get_system(self):
        def func(state, t):
            x, y = state
            return np.array([
                1.5 * x - x * y,
                1.7 * x * y - 3 * y
            ])
        return func

    def generate_base_individual(self):
        return [
            Individual(1., '({})-({})', [
                Individual(random.uniform(0,5), 'VAR_0_', []),
                Individual(1, '({})*({})', [
                    Individual(1., 'VAR_0_', []),
                    Individual(1., 'VAR_1_', [])
                ])
            ]),
            Individual(1., '({})-({})', [
                Individual(1, '({})*({})', [
                    Individual(1., 'VAR_0_', []),
                    Individual(1., 'VAR_1_', [])
                ]),
                Individual(3, 'VAR_1_', []),
            ])
        ]

class LorenzSystem(BasePreset):
    """ Chaotic Lorenz system
    """
    def get_system(self):
        def func(state, t):
            x, y, z = state

            o = 10
            p = 14
            b = 8/3

            return np.array([
                o * (y - x),
                x * (p - z) - y,
                x * y - b * z
            ])
        return func

    def generate_base_individual(self):
        return [
            Individual(random.uniform(0,20), '({})-({})', [
                Individual(1, 'VAR_1_', fix_coeff=True),
                Individual(1, 'VAR_0_', fix_coeff=True)
            ]),
            Individual(1., '({})-({})', [
                Individual(1, '({})*({})', [
                    Individual(1., 'VAR_0_', fix_coeff=True),
                    Individual(1., '({})-({})', [
                        Individual(random.uniform(0,20), '1'),
                        Individual(1, 'VAR_2_', fix_coeff=True)
                    ], fix_coeff=True)
                ], fix_coeff=True),
                Individual(1, 'VAR_1_', fix_coeff=True)
            ], fix_coeff=True),
            Individual(1., '({})-({})', [
                Individual(1, '({})*({})', [
                    Individual(1., 'VAR_0_', fix_coeff=True),
                    Individual(1., 'VAR_1_', fix_coeff=True)
                ], fix_coeff=True),
                Individual(random.uniform(0,5), 'VAR_2_')
            ], fix_coeff=True)
        ]
