from .base import *

# base class for Controllers for robots with differential drives
# this class *must be* sub-classed to make actual robot controllers
# - in those subclasses, 'inputs' can be whatever the subclass specifies (it will
# probably be a list of sensor measurements, but that is up to you)
# - the controller must set the variables self.left_speed_command and
# self.right_speed_command, and then at the end of their step methods, call the
# step method of this class with:
#       return super().step(inputs, dt)
# - note that a Controller may or may not have internal dynamics, which might
# be based on the history of its inputs and/or any other state variables or
# memory which you choose to add to your Controller classes
class Controller(System):

    # construct Controller
    def __init__(self, left_noisemaker=None, right_noisemaker=None):
        super().__init__() # call System init
        # noise can be applied to the controller's outputs
        self.left_noisemaker = left_noisemaker
        self.right_noisemaker = right_noisemaker
        # store inputs/outputs for later analysis, and for potential use in controller
        self.inputs = [[0, 0]]
        # control variables and their histories
        self.left_speed_command = 0
        self.right_speed_command = 0
        self.left_speed_commands = [0]
        self.right_speed_commands = [0]

    # step Controller forwards in time
    def step(self, inputs, dt):
        # record inputs - this is primarily for potential use in the controller,
        # rather than for plotting - inputs will generally already be stored
        # elsewhere, e.g. in sensor objects
        self.inputs.append(inputs)
        # apply noise
        if self.left_noisemaker is not None:
            self.left_speed_command += self.left_noisemaker.step(dt)
        if self.right_noisemaker is not None:
            self.right_speed_command += self.right_noisemaker.step(dt)
        # record outputs
        self.left_speed_commands.append(self.left_speed_command)
        self.right_speed_commands.append(self.right_speed_command)
        # return outputs
        return self.left_speed_command, self.right_speed_command
