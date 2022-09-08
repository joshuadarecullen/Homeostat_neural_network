import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
pygame = None
try:
    import pygame
except:
    print("WARNING: pygame module not found, visualisations will not be shown. " +
          "You should be able to install pygame with:\n" +
          "     pip install pygame")
from enum import Enum


####################################################################################
#                           utility functions begin
####################################################################################

# for any two angles, return difference in the interval of [-pi, pi]
def angle_difference(angle1, angle2):
    diff = (angle1 - angle2) % (2*np.pi)
    if diff > np.pi:
        diff -= (2*np.pi)
    return diff

# generate random number from uniform interval
# - numpy already has a function for this, but I wrote this and used it in many places before thinking to check that
def random_in_interval(minimum=0, maximum=1):
    width = maximum - minimum
    return (width * np.random.random()) + minimum

####################################################################################
#                           utility functions end
####################################################################################
####################################################################################
#                           System class begins
####################################################################################

# Conceptually, all entities in the simulation are systems. For this reason,
# other classes inherit from this one.
# In the current implementation, this is not strictly necessary, as not all
# classes share properties with this one.
class System:
    # construct System. Many systems have xy-coordinates and orientations (theta), but for some, such as Controllers and Disturbances, it is
    # not useful to give them these variables. For those systems, has_position and/or has_orientation are set to false
    def __init__(self, x=None, y=None, theta=None):
        self.has_position = not (x is None or y is None)
        if self.has_position:
            self.x = x
            self.y = y
            self.xs = [x]
            self.ys = [y]
        self.has_orientation = theta is not None
        if self.has_orientation:
            self.theta = theta
            self.thetas = [theta]

    # systems with position and/or orientation will *need* to call this method,
    # from their own step method
    def step(self, dt):
        if self.has_position:
            self.xs.append(self.x)
            self.ys.append(self.y)
        if self.has_orientation:
            self.thetas.append(self.theta)


####################################################################################
#                           System class ends
####################################################################################

####################################################################################
#                           Agent classes begin
####################################################################################


# the base class for agents. currently only differential drive robots are implemented, but other types of agent could
# also be implemented easily enough
class Agent(System):

    def __init__(self, x, y, theta=None):
        super().__init__(x, y, theta)  # call System constructor. xy-variables are handled there

    # Agent has no step, so if one of its subclasses makes a call to super().step,
    # then the call will go to System.step()

####################################################################################
#                           Agent classes end
####################################################################################
