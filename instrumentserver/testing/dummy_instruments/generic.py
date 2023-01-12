from typing import List

from qcodes import Instrument
from qcodes.utils import validators
import numpy as np
import time


class DummyChannel(Instrument):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.add_parameter('ch0',
                           set_cmd=None,
                           vals=validators.Numbers(0, 1),
                           initial_value=0)

        self.add_parameter('ch1', unit='v',
                           set_cmd=None,
                           vals=validators.Numbers(-1, 1),
                           initial_value=1)

        self.functions['dummy_function'] = self.dummy_function

    def dummy_function(self, *args, **kwargs):
        """Dummy function for specific channels used for testing"""
        print(f'the dummy chanel: {self.name} has been activated with:')
        print(f'args: {args}')
        print(f'kwargs: {kwargs}')
        return True

class DummyInstrumentWithSubmodule(Instrument):
    """A dummy instrument with submodules."""

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.add_parameter('param0',
                           set_cmd=None,
                           vals=validators.Numbers(0, 1),
                           initial_value=0)

        self.add_parameter('param1', unit='v',
                           set_cmd=None,
                           vals=validators.Numbers(-1, 1),
                           initial_value=1)
        for chan_name in ('A', 'B', 'C'):
            channel = DummyChannel('Chan{}'.format(chan_name))
            self.add_submodule(chan_name, channel)

        self.functions['test_func'] = self.test_func
        self.functions['dummy_function'] = self.dummy_function

    def test_func(self, a, b, *args, c: List[int] = [10, 11], **kwargs):
        """
        This is a test function, of course you knew this from the tittle but It's nice to have documentation, isn't it?

        :param a: Very nice parameter.
        :param b: Even nicer parameter
        :param c: This one sucks though.
        """
        return a, b, args[0], c, kwargs['d'], self.param0()

    def dummy_function(self, *args, **kwargs):
        """
        Such a dumb dummy function here doing nothing other than printing and occupying your precious, precious terminal
        space.
        """
        print(f'the dummy chanel: {self.name} has been activated with:')
        print(f'args: {args}')
        print(f'kwargs: {kwargs}')
        return "I am being returned"


class DummyInstrumentTimeout(Instrument):
    """A dummy instrument to test timeout situations."""
    def __init__(self, name: str, *args,  **kwargs):
        super().__init__(name, *args, **kwargs)

        self.random = np.random.randint(10000)

    def get_random(self):
        return self.random

    def get_random_timeout(self):
        time.sleep(10)
        return self.random


class DummyInstrumentRandomNumber(Instrument):
    """A dummy instrument with a few parameters that have random numbers generated on demand"""

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.add_parameter('param0',
                           set_cmd=None,
                           vals=validators.Numbers(1, 10),
                           initial_value=1)

        self.add_parameter('param1',
                           set_cmd=None,
                           vals=validators.Numbers(10, 20),
                           initial_value=10)

        self.add_parameter('param2',
                           set_cmd=None,
                           vals=validators.Numbers(20, 30),
                           initial_value=20)

        self.add_parameter('param3',
                           set_cmd=None,
                           vals=validators.Numbers(30, 40),
                           initial_value=30)

        self.add_parameter('param4',
                           set_cmd=None,
                           vals=validators.Numbers(40, 50),
                           initial_value=40)

    def generate_data(self, name: str):

        if name == 'param0':
            self.parameters[name].set(np.random.randint(1, 10))
        if name == 'param1':
            self.parameters[name].set(np.random.randint(10, 20))
        if name == 'param2':
            self.parameters[name].set(np.random.randint(20, 30))
        if name == 'param3':
            self.parameters[name].set(np.random.randint(30, 40))
        if name == 'param4':
            self.parameters[name].set(np.random.randint(40, 50))

    def get(self, param_name):
        self.generate_data(param_name)
        return self.parameters[param_name].get()
