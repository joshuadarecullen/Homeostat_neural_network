from .base import *

# a class to represent a motor for a differential drive robot
# - having a class for making motor objects makes it easy to apply motor noise
# and other disturbances to the robot's motors
class Motor(System):

    # construct Motor
    # - a robot has a maximum speed. controller inputs which are larger than this
    # will saturate at the max
    # - the motor inertia coefficient determines how quickly the motor can change its speed
    #       - if the inertia is 0, then the motor can change speed instantaneously
    #           to any new control input
    #       - if the inertia is greater than 0, then the speed may change slowly,
    #       - negative inertia values will be ignored
    # - a motor can be reversed, so that forwards becomes backwards and vice versa
    def __init__(self, max_speed, motor_inertia_coeff=0, reversed=False, noisemaker=None):
        # motors can have noise sources attached to them
        self.noisemaker = noisemaker
        # current speed and history of speed
        self.speed = 0
        self.speeds = [0]
        # system parameters
        self.motor_inertia_coeff = max(0, motor_inertia_coeff) + 1 # limits rate of change of speed
        self.max_speed = max_speed
        self.reversed = reversed

    # step motor forwards in time
    def step(self, speed_command, dt):

        # if motor is reversed, then reverse the control input
        if self.reversed:
            speed_command = -speed_command

        # calculate speed change
        speed_change = (1/self.motor_inertia_coeff) * (speed_command - self.speed)

        # change speed
        self.speed += speed_change

        # apply noise
        if self.noisemaker is not None:
            self.speed += self.noisemaker.step(dt)

        # constrain motor speed
        if self.speed > 0:
            self.speed = min(self.speed, self.max_speed)
        else:
            self.speed = max(self.speed, -self.max_speed)

        # keep record of speed
        self.speeds.append(self.speed)

        # return speed
        return self.speed
