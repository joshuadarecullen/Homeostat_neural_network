import unittest
import numpy as np
from testcase import MyTestCase
import sys
sys.path.insert(1, '../../..')
from situsim_v1_2 import *

class Test_Sensor(MyTestCase):

    def test_init(self):

        s = Sensor()
        self.assertTrue(not hasattr(s, 'x'))
        self.assertTrue(not hasattr(s, 'y'))
        self.assertTrue(not hasattr(s, 'theta'))
        self.assertTrue(not hasattr(s, 'xs'))
        self.assertTrue(not hasattr(s, 'ys'))
        self.assertTrue(not hasattr(s, 'thetas'))

        s = Sensor(x=1, y=2)
        self.assertTrue(hasattr(s, 'x'))
        self.assertTrue(hasattr(s, 'y'))
        self.assertTrue(not hasattr(s, 'theta'))
        self.assertTrue(hasattr(s, 'xs'))
        self.assertTrue(hasattr(s, 'ys'))
        self.assertTrue(not hasattr(s, 'thetas'))

        s = Sensor(x=1, y=2, theta=1)
        self.assertTrue(hasattr(s, 'x'))
        self.assertTrue(hasattr(s, 'y'))
        self.assertTrue(hasattr(s, 'theta'))
        self.assertTrue(hasattr(s, 'xs'))
        self.assertTrue(hasattr(s, 'ys'))
        self.assertTrue(hasattr(s, 'thetas'))

        s = Sensor(theta=1)
        self.assertTrue(not hasattr(s, 'x'))
        self.assertTrue(not hasattr(s, 'y'))
        self.assertTrue(hasattr(s, 'theta'))
        self.assertTrue(not hasattr(s, 'xs'))
        self.assertTrue(not hasattr(s, 'ys'))
        self.assertTrue(hasattr(s, 'thetas'))

class Test_LightSensor(MyTestCase):

    def test_init(self):

        s = LightSensor(light_sources=[], x=1, y=2, theta=3)
        self.assertTrue(hasattr(s, 'x'))
        self.assertTrue(hasattr(s, 'y'))
        self.assertTrue(hasattr(s, 'theta'))
        self.assertTrue(hasattr(s, 'xs'))
        self.assertTrue(hasattr(s, 'ys'))
        self.assertTrue(hasattr(s, 'thetas'))
        self.assertTrue(hasattr(s, 'activation'))
        self.assertTrue(hasattr(s, 'activations'))
        self.assertTrue(hasattr(s, 'noisemaker'))
        self.assertTrue(hasattr(s, 'field_of_view'))

if __name__ == '__main__':
    unittest.main()
