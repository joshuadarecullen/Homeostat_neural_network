from .base import *

# base sensor class. in the current implementation, only contains methods for drawing
class Sensor(System):

    # by default, a Sensor has no position, but one can be specified (and for most sensors will)
    def __init__(self, x=None, y=None, theta=None, color='red', radius=0.2):
        super().__init__(x, y, theta)
        self.color = color
        self.radius = radius

    # draw sensor in the specified matplotlib axes
    def draw(self, ax):
        if self.has_position:
            ax.add_artist(mpatches.Circle((self.x, self.y), self.radius, color=self.color))
            ax.plot(self.x, self.y, 'k.')

    # draw sensor in a pygame display
    def pygame_draw(self, screen, scale, shiftx, shifty):
        if self.has_position:
            pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color=self.color, radius=scale*self.radius)

# a class to define a sensor which detects instances of the LightSource class
class LightSensor(Sensor):
    # construct light sensor
    def __init__(self, light_sources, x, y, theta=0, field_of_view=2*np.pi, noisemaker=None):
        super().__init__(x, y, theta)
        self.light_sources = light_sources  # a list of LightSource instances which this sensor can detect
        self.activation = 0  # sensor activation. this variable is updated in and returned from the step method. it is stored separately in case you want to access it multiple times between simulation steps, although that is unlikely to be necessary
        self.activations = [self.activation]  # for plotting and analysis, a sensor keeps a complete record of its activation over time
        self.noisemaker = noisemaker  # noise source
        self.field_of_view = field_of_view  # sensor angular field of view

    # step light sensor. the sensor has no dynamics, so technically is not stepped in time, but 'step' is used for consistency
    def step(self, dt):
        super().step(dt)  # call System step method, to store xy-coordinates and theta
        self.activation = 0  # begin with zero activation, and add to it for every detected light source
        for source in self.light_sources:  # for every light source the sensor can detect
            angle_to_source = np.arctan2(source.y - self.y, source.x - self.x)  # find angle of vector from light source to sensor
            if np.abs(angle_difference(angle_to_source, self.theta)) <= (self.field_of_view/2):  # if angle is within field fo view, the sensor detects the light
                self.activation += source.get_brightness_at(self.x,self.y)  # stimuli from multiple lights are added linearly

        # add noise, if a noisemaker is implemented
        if self.noisemaker != None:
            self.activation += self.noisemaker.step(dt)

        # record activation
        self.activations.append(self.activation)  # store activation

        # return activation
        return self.activation  # return activation

class WallSensor(Sensor):

    # construct light sensor
    def __init__(self, arena, x, y, theta=0, field_of_view=2*np.pi, noisemaker=None):
        super().__init__(x, y, theta)
        self.arena = arena  # a list of LightSource instances which this sensor can detect
        self.activation = 0  # sensor activation. this variable is updated in and returned from the step method. it is stored separately in case you want to access it multiple times between simulation steps, although that is unlikely to be necessary
        self.activations = [self.activation]  # for plotting and analysis, a sensor keeps a complete record of its activation over time
        self.noisemaker = noisemaker  # noise source
        self.field_of_view = field_of_view  # sensor angular field of view

    # step light sensor. the sensor has no dynamics, so technically is not stepped in time, but 'step' is used for consistency
    def step(self, dt):
        super().step(dt)  # call System step method, to store xy-coordinates and theta
        self.activation = 0  # begin with zero activation, and add to it for every detected light source
        for source in self.light_sources:  # for every light source the sensor can detect
            angle_to_source = np.arctan2(source.y - self.y, source.x - self.x)  # find angle of vector from light source to sensor
            if np.abs(angle_difference(angle_to_source, self.theta)) <= (self.field_of_view/2):  # if angle is within field fo view, the sensor detects the light
                self.activation += source.get_brightness_at(self.x,self.y)  # stimuli from multiple lights are added linearly

        # add noise, if a noisemaker is implemented
        if self.noisemaker != None:
            self.activation += self.noisemaker.step(dt)

        # record activation
        self.activations.append(self.activation)  # store activation

        # return activation
        return self.activation  # return activation
