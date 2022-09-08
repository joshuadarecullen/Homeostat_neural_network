import sys
# path to folder which contains situsim_v1_2
sys.path.insert(1, '~/Documents/university/year_1_Spring_semester/adaptive_systems/situsim/_situsim_v1_v2')
from situsim_v1_2 import *

# base class for sources of disturbance. disturbances can be easily set up to be enabled and disabled at predetermined
# times during a run of a simulation
#   at every time in start_times, the disturbance should become active
#   at every time in end_times, the disturbance should be disabled again
#   N.B. some of these disturbances are severe enough to require adaptation in a robot's controller, and some might be
#   easier to deal with than others
#   - using more than one of these at once could be very challenging
#   - they are fairly easy to create, if you have ideas of your own for disturbances
class DisturbanceSource(System):

    # construct disturbance source
    def __init__(self, start_times=[], end_times=[], enabled=True):
        super().__init__()
        self.enabled = enabled
        if start_times:  # if any start_times are passed in, then the disturbance is initially disabled, and it will not be enabled until the first start time is reached
            self.enabled = False
        self.t = 0  # DisturbanceSources keep track of time internally. a number of classes do this, and it is certainly not the most computationally efficient approach, but it avoids using a global time variable (which could be horrendous)
        self.start_times = start_times
        self.end_times = end_times  # stop_times would be a better name - this will  be fixed in future versions of the simulation

    # step disturbance source. this is where the disturbance gets enabled and disabled. the effect of the disturbance will be applied in the step methods for the subclasses of DisturbancSource
    def step(self, dt):
        self.t += dt  # increment time variable by simulatino step size
        if self.enabled:
            if not self.end_times:  # if the disturbance is enabled, then check if end_times is empty, and if it is, then there is nothing left to do, so just return
                return
            else:  # otherwise, check to see if it is time to disable the disturbance yet
                if self.t > self.end_times[0]:  # always get the end_time at the beginning of the list
                    self.enabled = False
                    self.end_times.pop(0)  # every time an end time is used, it is removed (popped) from the list as it will not be used again
        else:
            if not self.start_times:  # if the disturbance is disabled but there are no start_times remaining, then there is nothing left to do, so just return
                return
            else:  # otherwise, check to see if it is time to enable the disturbance yet
                if self.t > self.start_times[0]:  # always get the start_time at the beginning of the list
                    self.enabled = True
                    self.start_times.pop(0)  # every time a start time is used, it is removed (popped) from the list as it will not be used again


# this simulates the needle on a Unit being physically pushed out of viable limits
class UnitVariableDisturbanceSource(DisturbanceSource):

    # construct disturbance source
    def __init__(self, unit, start_times):
        super().__init__(start_times, [], False) # call DisturbanceSource constructor
        self.unit = unit

    # step disturbance source
    def step(self, dt):
        super().step(dt)
        # if the disturbance source is enabled, disturb the homeostat essential variable
        if self.enabled:
            self.unit.theta[-1] = 5

            self.enabled = False  # unlike a generic DisturbanceSource, this is a one-shot disturbance,
                                  # and so is automatically disable immediately after being applied

# this applies to the basic Robot class, which has only 2 sensors
# for robots with more sensors it would need to be extended
#   on its own, spike noise is unlikely to require adaptation
#   - infrequent spikes may not cause much trouble for a controller, and frequent ones may make sensory signals to
#   unreliable to be useful
class SpikeNoiseDisturbanceSource(DisturbanceSource):

    def __init__(self, robot, spike_noise_params=[0.01, 1.0, -1.0], perturb_left=True, perturb_right=True, start_times=[], end_times=[], enabled=True):
        super().__init__(start_times, end_times, enabled)
        self.robot = robot  # the robot which will be affected by the disturbance
        self.perturb_left = perturb_left  # if True, then the left sensor will be affected by noise
        self.perturb_right = perturb_right   # if True, then the right sensor will be affected by noise
        self.spike_noise_params = spike_noise_params
        if perturb_left:  # params are initially all zero, so disturbance is ready but not yet in effect
            self.robot.left_sensor.noisemaker.noise_sources.append(SpikeNoiseSource(prob=0, pos_size=0, neg_size=0))
        if perturb_right:
            self.robot.right_sensor.noisemaker.noise_sources.append(SpikeNoiseSource(prob=0, pos_size=0, neg_size=0))

    # step noise source
    #   internal noise source is enabled or disabled by setting all of its params to either zeros or desirec values
    #       - this is not the best way to approach the problem, and it will be changed in a future version of the simulation
    def step(self, dt):
        super().step(dt)
        if self.enabled:
            if self.perturb_left:
                self.robot.left_sensor.noisemaker.noise_sources[0].set_params(self.spike_noise_params)
            if self.perturb_right:
                self.robot.right_sensor.noisemaker.noise_sources[0].set_params(self.spike_noise_params)
        else:
            if self.perturb_left:
                self.robot.left_sensor.noisemaker.noise_sources[0].set_params([0, 0, 0])
            if self.perturb_right:
                self.robot.right_sensor.noisemaker.noise_sources[0].set_params([0, 0, 0])


# this applies to the basic Robot class, which has only 2 sensors, but it could easily be copied and modified to affect
# more or less sensors
# it uses a WhiteNoiseSource, which is effectively integrated over time to cause drift in the robot's sensor positions
#   this is a gradual change to the robot's morphology which, if big enough, will require adaptation in the controller
#   depending on how large the maximum move is, and how long the disturbance is applied for, this disturbance can be a
#   major problem, and it may not even be possible for most controllers to adapt if, for example, both sensors end up
#   on the same side of the robot's body
class MovingSensorDisturbanceSource(DisturbanceSource):

    # construct disturbance source
    def __init__(self, robot, max_move=np.pi/36, move_left=True, move_right=False, start_times=[], end_times=[], enabled=True):
        super().__init__(start_times, end_times, enabled)
        self.robot = robot
        self.move_left = move_left  # left sensor will be affected, if this is True
        self.move_right = move_right  # right sensor will be affectd, if this is True
        self.noisesource = WhiteNoiseSource(max_move, -max_move)

    # step disturbance
    def step(self, dt):
        super().step(dt)
        if self.enabled:
            if self.move_left:
                self.robot.left_sensor_angle += self.noisesource.step(dt)
            if self.move_right:
                self.robot.right_sensor_angle += self.noisesource.step(dt)


# this implements a large-scale sensory inversion, which will be quite easy to adapt to, but only if it can be reliably
# detected.
#   - in the case of this disturbance, detection may be the hard part
#   - a relatively easy place to begin would be with a light-seeking robot in an environment with only one light source
#       - then it shouldn't be too hard to detect the sudden change in behaviour this disturbance will cause
#   - in more complex environments, and/or if combined with other disturbances and noise, this becomes a real challenge
class SensoryInversionDisturbanceSource(DisturbanceSource):

    # construct disturbance source
    def __init__(self, robot, start_times):
        super().__init__(start_times, [], False)
        self.robot = robot  # the robot which will be disturbed

    # step disturbance source
    def step(self, dt):
        super().step(dt)
        if self.enabled:  # reqire connections between sensor and motors
            temp = self.robot.left_sensor
            self.robot.left_sensor = self.robot.right_sensor
            self.robot.right_sensor = temp
            temp = self.robot.right_sensor_angle
            self.robot.right_sensor_angle = self.robot.left_sensor_angle
            self.robot.left_sensor_angle = temp

            self.enabled = False  # unlike a generic DisturbanceSource, this is a one-shot disturbance, and so is automatically disable immediately after being applied



# THESE LINES APPLY TO A FEATURE WHICH HAS BEEN DISABLED FOR THIS CHALLENGE, BY BEING COMMENTED OUT - IF YOU UNCOMMENT
# THE LINE IN THE STEP FUNCTION WHICH DISTURBS THE ROBOT, THE EFFECT WILL BE AS DESCRIBED BELOW
# the disturbance also changes the decay_rate parameter of the given robot, a change made specifically for this challenge. when
# the consumables are food, the decay_rate determines the energetic cost of movement. When the consumables are poison,
# penalising movement in the usual way may be an issue - if there is a cost to movement, and a cost to consuming poison,
# then the best strategy to minimise costs may be to simply stop moving (the robot will still lose some energy, even
# when not moving, but this loss happens in either case).
# when the sign of decay_rate is inverted, energy grows when the robot moves, i.e. movement is  directly rewarded,
# so that the best strategy for the robot to maximise energy is to keep moving and avoid poison at the same time.
class NewFoodSwitcheroo(DisturbanceSource):

    # construct disturbance source
    def __init__(self, start_times, enabled, robot=None, consumables=None):
        super().__init__(start_times, end_times=[], enabled=enabled)
        if consumables:
            self.add_consumables(consumables)
        if robot:
            self.add_robot(robot)

    # add robot to DisturbanceSource - this allows for the DisturbanceSource to be created in advance of the Robot,
    # so that the same pattern of using a function to generate DisturbanceSources in advance can be followed as was
    # used in the ealier motor_inversion_challenge.py file
    def add_robot(self, robot):
        self.robot = robot

    # add consumables to DisturbanceSource - this allows for the DisturbanceSource to be created in advance of the
    # consumables, so that the same pattern of using a function to generate DisturbanceSources in advance can be
    # followed as was used in the ealier motor_inversion_challenge.py file
    def add_consumables(self, consumables):
        self.consumables = consumables

    # step disturbance source
    def step(self, dt):
        super().step(dt)
        if self.enabled:
            # self.robot.decay_rate = -self.robot.decay_rate  # switch between penalising and rewarding motion
            for consumable in self.consumables:  # switch consumable types
                if consumable.real_type == Consumables.food:
                    consumable.real_type = Consumables.poison
                elif consumable.real_type == Consumables.poison:
                    consumable.real_type = Consumables.food

            self.enabled = False  # this is a one-shot disturbance, so disable it again immediately


###### My code!!!!

class DisturbLightSource(DisturbanceSource):

    # construct disturbance source
    def __init__(self, current_light_source, start_times):
        super().__init__(start_times, [50, 70, 110], False)

        #TODO - make it move linearly across the map
        # self.max_move = np.pi/36
        # self.min_move = -np.pi/36
        self.current_light_source = current_light_source
        # self.noisesource = WhiteNoiseSource(self.max_move, self.min_move)

    def step(self, dt):
        super().step(dt)
        if self.enabled:

            #TODO randomize the movement of light position
            self.current_light_source.x += 2
            self.current_light_source.y += 2


# Change this into a coupled agent light source with the speed and direction of the robot creating the direction and speed of the lightsource?
# Only coupled when robot in range of brightness
class MovingLightSource(DisturbanceSource):

    #construct disturbance source
    def __init__(self, light_source, max_move=0.01, start_times = [], end_times = []):
        super().__init__(start_times, end_times, False)
        self.light_source = light_source

        self.step_size = 1
        # self.noisesource = WhiteNoiseSource(max_move, -max_move)

    def step(self, dt):
        super().step(dt)
        if self.enabled:

            rfloat = self.sign_gen()

            self.light_source.x += self.step_size * rfloat#self.noisesource.step(dt)
            self.light_source.y += self.step_size * rfloat#self.noisesource.step(dt)

    def sign_gen(self):
        return 1 if np.random.normal(0,1,1) < 0.5 else -1


class ToggleLightSource(DisturbanceSource):

    def __init__(self, light_source, start_times):

        super().__init__(start_times, [70, 100], False)
        self.light_source = light_source

    def step(self, dt):
        super().step(dt)
        if self.enabled:
            self.light_source.is_on = False
        else:
            self.light_source.is_on = True

# class MotorInversionDisturbanceSource(DisturbanceSource):


class TeleportRobot(DisturbanceSource):
    def __init__(self, robot, start_times=[100], end_times=[]):
        super().__init__(start_times, end_times, False)
        self.robot = robot

    def step(self, dt):
        super().step(dt)
        if self.enabled:
            self.robot.state[0] = 499
            self.robot.state[1] = 499
            # self.robot.step(dt)
            self.enabled = False


