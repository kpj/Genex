import importlib


def load_preset(name):
    """ Load preset from `example.py` by name
    """
    mod = importlib.import_module('presets.examples')
    try:
        return getattr(mod, name)()
    except AttributeError:
        return None

class BasePreset(object):
    def __init__(self):
        """ Define dimensions of model if not given by `self.generate_base_individual`
        """
        self._dim = 0

    @property
    def dim(self):
        base = self.generate_base_individual()
        return self._dim if base is None else len(base)

    def get_system(self):
        """ Return ODE
        """
        raise NotImplementedError

    def generate_base_individual(self):
        """ Generate individual used in initial population.
            Return `None` for random initialization.
        """
        return None
