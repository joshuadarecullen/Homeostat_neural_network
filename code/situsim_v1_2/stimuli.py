from .base import *

####################################################################################
#                           Stimulus classes begin
####################################################################################

# this is the base class for stimuli in the environment. it could be used in other ways, but for now is only used as the
# base for the various types of light sources
class Stimulus(System):

    # A Stimulus is on (enabled) by default, but can be disabled so that no sensors will detect it
    def __init__(self, x=None, y=None, theta=None, is_on=True):
        super().__init__(x, y, theta)
        self.is_on = is_on

    # get distance from the given xy coordinates to the Stimulus, if the Stimulus has position
    def get_distance(self, x, y):
        if self.has_position:
            vec = np.array([self.x - x, self.y - y])  # vector from sensor to stimulus
            return np.linalg.norm(vec)  # length of vector, i.e. distance from sensor to stimulus
        else:
            return None


# this class implements a static and noiseless light source. it has two models for decay of brightness over distance,
# inverse square and linear. you should use whichever you find easiest, but that will depend on what kind of controllers
# you are working on
#   in the linear case, brightness decays from the maximum to zero, according to the specified
#   gradient.
#       - the downside to this is that there will be a maximum detection distance, beyond which a sensor will not detect
#       the light, but this is only likely to be a problem if a large decay gradient is used (not that problems are
#       necessarily bad - they can make things more interesting).
#       - the upside to the linear decay model is that it may make it easier to program certain kinds of controller.
#   in the inverse square case, brightness decays in a way which is closer to reality.
#       - the upside to the inverse square model is that there is no hard limit to detection range (although there will
#       be a distance at which a sensor is barely stimulated by it)
#       - the downside is that the inverse square model can make it more difficult to program certain kinds of
#       controller, due to its nonlinearity.
class LightSource(Stimulus):

    # construct light source
    def __init__(self, x, y, theta=None, brightness=1, gradient=0.01, model='inv_sq', is_on=True):
        super().__init__(x, y, theta, is_on)  # call Stimulus constructor
        self.brightness = brightness  # this is the brightness of the light at the source
        self.gradient = gradient  # this determines how quickly the brightness decays when the linear model is used
        self.model = model  # model can be inv_sq, which is realistic, or linear, which is not physically realistic but is easier to work with
        self.is_on = is_on

    # draw light source in the specified matplotlib axes
    def draw(self, ax):
#        if self.is_on:
        ax.add_artist(mpatches.Circle((self.x, self.y), 0.7, color='yellow'))
        ax.add_artist(mpatches.Circle((self.x, self.y), 0.2, color='orange'))
        ax.plot(self.x, self.y, 'r.')

    # draw light source in a pygame display
    def pygame_draw(self, screen, scale, shiftx, shifty):
        # if self.is_on:
        pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color='yellow', radius=scale*0.7)
        pygame.draw.circle(screen, center=(scale*self.x+shiftx, scale*self.y+shifty), color='orange', radius=scale*0.2)

    # get the brightness of the light at the given xy coordinates
    def get_brightness_at(self, x, y):
        # print('LightSource::get_brightness_at')
        # print('   ' + str(self.is_on))
        brightness = 0
        if self.is_on:
            dist = self.get_distance(x, y)
            if self.model == 'inv_sq':
                brightness = self.inv_sq_model(dist)
            elif self.model == 'linear':
                brightness = self.linear_model(dist)
            elif self.model == 'binary':
                brightness = self.brightness
        return brightness

    # for some controllers, it is much easier to work with a linear light decay model. it is not physically realistic,
    # but that does not matter to this assignment
    def linear_model(self, dist):
        return max(self.brightness - self.gradient * dist, 0)

    # this is a more realistic model of light decay. for simple Braitenberg vehicle style robots the nonlinearity of
    # light decay can lead to interesting behaviours
    def inv_sq_model(self, dist):
        return self.brightness / np.power(dist+1, 2)  # 1 is added to fix brightness at dist=0

####################################################################################
#                           Stimulus classes end
####################################################################################
