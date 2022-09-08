import unittest
import numpy as np
from testcase import MyTestCase
import sys
sys.path.insert(1, '../../..')
from situsim_v1_2 import *

class Test_Stimulus(MyTestCase):

    def test_init(self):

        s = Stimulus()
        self.assertTrue(not hasattr(s, 'x'))
        self.assertTrue(not hasattr(s, 'y'))
        self.assertTrue(not hasattr(s, 'theta'))
        self.assertTrue(not hasattr(s, 'xs'))
        self.assertTrue(not hasattr(s, 'ys'))
        self.assertTrue(not hasattr(s, 'thetas'))
        self.assertTrue(s.is_on)

        s = Stimulus(x=1, y=2, is_on=False)
        self.assertTrue(hasattr(s, 'x'))
        self.assertTrue(hasattr(s, 'y'))
        self.assertTrue(not hasattr(s, 'theta'))
        self.assertTrue(hasattr(s, 'xs'))
        self.assertTrue(hasattr(s, 'ys'))
        self.assertTrue(not hasattr(s, 'thetas'))
        self.assertTrue(not s.is_on)

        s = Stimulus(x=1, y=2, theta=1)
        self.assertTrue(hasattr(s, 'x'))
        self.assertTrue(hasattr(s, 'y'))
        self.assertTrue(hasattr(s, 'theta'))
        self.assertTrue(hasattr(s, 'xs'))
        self.assertTrue(hasattr(s, 'ys'))
        self.assertTrue(hasattr(s, 'thetas'))

        s = Stimulus(theta=1)
        self.assertTrue(not hasattr(s, 'x'))
        self.assertTrue(not hasattr(s, 'y'))
        self.assertTrue(hasattr(s, 'theta'))
        self.assertTrue(not hasattr(s, 'xs'))
        self.assertTrue(not hasattr(s, 'ys'))
        self.assertTrue(hasattr(s, 'thetas'))


    def test_get_distance(self):

        s = Stimulus(theta=1)
        self.assertTrue(s.get_distance(0,0) is None)

        s = Stimulus(x=0, y=0, theta=1)
        self.assertNear(s.get_distance(1,1), np.sqrt(2))

        s = Stimulus(x=10, y=0, theta=1)
        self.assertNotNear(s.get_distance(1,1), np.sqrt(2))

class Test_LightSource(MyTestCase):

    def test_init(self):

        ls = LightSource(x=0, y=0)
        self.assertTrue(hasattr(ls, 'x'))
        self.assertTrue(hasattr(ls, 'y'))
        self.assertTrue(not hasattr(ls, 'theta'))
        self.assertTrue(hasattr(ls, 'xs'))
        self.assertTrue(hasattr(ls, 'ys'))
        self.assertTrue(not hasattr(ls, 'thetas'))
        self.assertTrue(ls.is_on)

if __name__ == '__main__':
    unittest.main()
