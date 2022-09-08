import unittest
import numpy as np
from testcase import MyTestCase
import sys
sys.path.insert(1, '../../..')
from situsim_v1_2 import *

class Test_angle_difference(MyTestCase):

    def test_func(self):

        # these two test the test - not the function
        self.assertNear(1, 1)
        self.assertNotNear(1, 1+0.01)

        # test the function
        self.assertApproxZero(angle_difference(np.pi, 3*np.pi))
        self.assertNotApproxZero(angle_difference(np.pi, 3*np.pi+0.01))

class Test_System(MyTestCase):

    def test_init(self):

        s = System(x=1)
        self.assertTrue(not hasattr(s, 'x'))
        self.assertTrue(not hasattr(s, 'y'))
        self.assertTrue(not hasattr(s, 'theta'))
        self.assertTrue(not hasattr(s, 'xs'))
        self.assertTrue(not hasattr(s, 'ys'))
        self.assertTrue(not hasattr(s, 'thetas'))

        s = System(x=1, y=2)
        self.assertTrue(hasattr(s, 'x'))
        self.assertTrue(hasattr(s, 'y'))
        self.assertTrue(not hasattr(s, 'theta'))
        self.assertTrue(hasattr(s, 'xs'))
        self.assertTrue(hasattr(s, 'ys'))
        self.assertTrue(not hasattr(s, 'thetas'))

        s = System(x=1, y=2, theta=1)
        self.assertTrue(hasattr(s, 'x'))
        self.assertTrue(hasattr(s, 'y'))
        self.assertTrue(hasattr(s, 'theta'))
        self.assertTrue(hasattr(s, 'xs'))
        self.assertTrue(hasattr(s, 'ys'))
        self.assertTrue(hasattr(s, 'thetas'))

        s = System(theta=1)
        self.assertTrue(not hasattr(s, 'x'))
        self.assertTrue(not hasattr(s, 'y'))
        self.assertTrue(hasattr(s, 'theta'))
        self.assertTrue(not hasattr(s, 'xs'))
        self.assertTrue(not hasattr(s, 'ys'))
        self.assertTrue(hasattr(s, 'thetas'))

    def test_step(self):

        s = System(x=1, y=2, theta=1)
        n_steps = 10
        for _ in range(n_steps):
            s.step(0.1)

        self.assertTrue(len(s.xs) == n_steps+1)
        self.assertTrue(len(s.ys) == n_steps+1)
        self.assertTrue(len(s.thetas) == n_steps+1)

class Test_Agent(MyTestCase):

    def test_init(self):

        a = Agent(x=0, y=3, theta=1)
        self.assertTrue(hasattr(a, 'x'))
        self.assertTrue(hasattr(a, 'y'))
        self.assertTrue(hasattr(a, 'theta'))
        self.assertTrue(hasattr(a, 'xs'))
        self.assertTrue(hasattr(a, 'ys'))
        self.assertTrue(hasattr(a, 'thetas'))

        a = Agent(x=0, y=3)
        self.assertTrue(hasattr(a, 'x'))
        self.assertTrue(hasattr(a, 'y'))
        self.assertTrue(not hasattr(a, 'theta'))
        self.assertTrue(hasattr(a, 'xs'))
        self.assertTrue(hasattr(a, 'ys'))
        self.assertTrue(not hasattr(a, 'thetas'))

    def test_step(self):

        a = Agent(x=1, y=2, theta=1)
        n_steps = 10
        for _ in range(n_steps):
            a.step(0.1)

        self.assertTrue(len(a.xs) == n_steps+1)
        self.assertTrue(len(a.ys) == n_steps+1)
        self.assertTrue(len(a.thetas) == n_steps+1)

if __name__ == '__main__':
    unittest.main()
