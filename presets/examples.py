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

class FitzHughNagumo(BasePreset):
    """ Spiking neuron model
    """
    def get_system(self):
        def func(state, t):
            v, w = state

            a = .7
            b = .8
            tau = 12.5
            I_ext = .5

            return np.array([
                v - v**3/3 - w + I_ext,
                (v + a - b*w) / tau
            ])
        return func

    def generate_base_individual(self):
        return [
            Individual(1, '({})+({})', [
                Individual(1, '({})-({})', [
                    Individual(1, '({})-({})', [
                        Individual(1, 'VAR_0_', fix_coeff=True),
                        Individual(1, '({})/({})', [
                            Individual(1, 'VAR_0_**3', fix_coeff=True),
                            Individual(random.uniform(1,8), '1')
                        ])
                    ], fix_coeff=True),
                    Individual(1, 'VAR_1_', fix_coeff=True)
                ], fix_coeff=True),
                Individual(random.uniform(0,1), '1')
            ], fix_coeff=True),
            Individual(1, '({})/({})', [
                Individual(1, '({})-({})', [
                    Individual(1, '({})+({})', [
                        Individual(1, 'VAR_0_', fix_coeff=True),
                        Individual(random.uniform(0,1), '1')
                    ], fix_coeff=True),
                    Individual(random.uniform(0,1), 'VAR_1_')
                ], fix_coeff=True),
                Individual(random.uniform(7,18), '1')
            ], fix_coeff=True)
        ]

class LorenzSystem(BasePreset):
    """ Chaotic Lorenz system
    """
    def get_system(self):
        def func(state, t):
            x, y, z = state

            o = 10
            p = 28
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
                        Individual(random.uniform(0,50), '1'),
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
