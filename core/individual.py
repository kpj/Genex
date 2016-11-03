"""
Tree-node definitions
"""

import re
import math
import random

from sympy import latex
from sympy.parsing.sympy_parser import parse_expr


SYMBOL_LIST = [
    '1', # constant
    '({}) + ({})', # addition
    '({}) - ({})', # subtraction
    '({}) * ({})', # multiplication
    '({}) / ({})', # division
    '({})**2', # exponentiation
#    '({})**3', # exponentiation
#    'sin({})', # trig. function
#    'e**({})', # exponential
#    'sqrt({})', # square root
]

class Individual(object):
    """ Abstract individual of population
    """
    def __init__(self, coeff=1., symbol='', args=None, varis=None):
        self._coeff = float(coeff)
        self._sym = symbol
        self._args = args if not args is None else []
        self._vars = varis if not varis is None else get_variables()

        assert len(self._args) == self._sym.count('{}'), 'invalid argument number for {c}*{term} ({l1}!={l2})'.format(c=self._coeff, term=self._sym, l1=len(self._args), l2=self._sym.count('{}'))

    @property
    def coeff(self):
        return self._coeff

    @property
    def symbol(self):
        return self._sym

    @property
    def args(self):
        return self._args

    @property
    def variables(self):
        return self._vars

    @property
    def arity(self):
        return len(self.args)

    @property
    def depth(self):
        if len(self.args) == 0:
            return 1
        else:
            return 1 + max([a.depth for a in self.args])

    def __iter__(self):
        """ Iterate over self and all children
        """
        yield self
        for arg in self.args:
            yield from arg

    def __repr__(self):
        """ Generate printable version of Individual
        """
        return '<{}>'.format(self.simplified())

    def __len__(self):
        return 1 + sum([len(a) for a in self.args])

    def __getitem__(self, key):
        return self._getter(self, key)[0]

    def _repr(self):
        if len(self.args) > 0:
            term = self.symbol.format(*[a._repr() for a in self.args])
        else:
            term = self.symbol

        if round(self.coeff, 1) == 1 and len(term) > 0:
            prefix = ''
        elif round(self.coeff, 1) == -1 and len(term) > 0:
            prefix = '-'
        else:
            if int(self.coeff) != self.coeff:
                prefix = '{c:.2}*'.format(c=self.coeff)
            else:
                prefix = '{c:g}*'.format(c=self.coeff)

        return '{p}{t}'.format(p=prefix, t=term)

    def latex_repr(self):
        return '${}$'.format(latex(self.simplified()))

    def simplified(self):
        return parse_expr(self._repr().replace('VAR', 'x'))

    def _getter(self, cur, key, i=0):
        """ Get items depth first
        """
        for a in cur.args:
            if i == key:
                return a, i
            i += 1

            if len(a.args) > 0:
                res, i = self._getter(a, key, i)
                if not res is None:
                    return res, i
        return None, i

    def as_lambda(self):
        return eval('lambda {args}: {body}'.format(
            args=','.join(self.variables),
            body=self._repr()), math.__dict__)

def get_symbols(arity=None, str_frmt=False):
    """ Return list of all available nodes
    """
    for sym in SYMBOL_LIST:
        sym_arity = sym.count('{}')

        if arity is None or arity == sym_arity:
            if str_frmt:
                yield sym, sym_arity
            else:
                yield Individual(1., sym, [
                    Individual() for _ in range(sym_arity)
                ])

def get_variables():
    return [sym for sym in SYMBOL_LIST if 'VAR' in sym]

def add_variables(num):
    SYMBOL_LIST.extend(['VAR_{}_'.format(i) for i in range(num)])
