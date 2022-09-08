from .base import *

####################################################################################
#                           NoiseSource classes begin
####################################################################################

# a NoiseSource is a kind of plugin object which can be attached to or incorporated into other objects
class NoiseSource(System):

    # construct noise source
    def __init__(self):
        super().__init__()
        self.noise = 0
        self.noises = [self.noise]

    # when stepped, a noise source generates a noise signal. this is where that signal gets stored for later analysis
    def step(self, dt):
        self.noises.append(self.noise)
        return self.noise


# a white noise source. in every simulation step, the noise will take any value in the specified interval
#   note that white noise can often be filtered quite easily
class WhiteNoiseSource(NoiseSource):

    # construct white noise source which will generate noise in the interval [min_val, max_val]
    def __init__(self, min_val, max_val):
        super().__init__()
        self.extent = max_val - min_val  # scale of the noise
        self.min_val = min_val  # minimum value noise will take (i.e. offset)

    # step noise
    def step(self, dt):
        self.noise = self.min_val + (self.extent * np.random.random())  # generate noise
        return super().step(dt)  # call step of NoiseSource to store noise


# brown noise source. technically, brown noise is the integral of white noise, and it is named after Brownian motion
#   note that drift or brown noise can be quite challenging to detect and compensate for
class BrownNoiseSource(NoiseSource):

    # construct brown noise source. max_step_size is the maximum step in either positive or negative direction, i.e.
    # half the scale of the white noise
    def __init__(self, max_step_size):
        super().__init__()
        self.max_step_size = max_step_size

    # step noise source
    def step(self, dt):
        self.noise += self.max_step_size * (2 * np.random.random() - 1)  # generate noise
        return super().step(dt)  # store noise


# a spike noise source generates positive or negative spikes in every simulation step, with the specified probability
# positive and negative spike sizes are specified independently (and either one could have size 0, if they are not
# wanted)
# the duration of a spike is a single simulation step, but as currently implemented nothing prevents two or more steps
# from occurring in a row, which is equivalent to a variable length spike (although this will be rare for low prob
# values)
#   note that this can be a very challenging kind of noise to handle for some controllers
class SpikeNoiseSource(NoiseSource):

    # construct noise source
    def __init__(self, prob, pos_size, neg_size):
        super().__init__()
        self.prob = prob  # probability of a spike
        self.pos_size = pos_size  # size of positive spike
        self.neg_size = neg_size  # size of negative spike

    # this was added for convenience, for use with SpikeNoiseDisturbanceSource, and is used to enable and disable the noise
    # - it does no real harm to do it this way, but it is not consistent with other the way the rest is coded
    #   in a future version this will be changed
    def set_params(self, params):
        self.prob = params[0]
        self.pos_size = params[1]
        self.neg_size = params[2]

    # step noise
    def step(self, dt):
        self.noise = 0  # noise is zero by default
        if np.random.random() < self.prob:  # if a randomly generated number is less than the probability of a spike, then spike
            if np.random.random() < 0.5:  # spikes are positive or negative with equiprobability
                self.noise = self.pos_size  # positive spike
            else:
                self.noise = self.neg_size  # negative spike
        return super().step(dt)  # call step of NoiseSource to store noise


# in the real world, we might expect different types of noise to be superimposed, e.g. low level white noise, plus some
# drift (brown noise), and possibly the occasional big spike coming from somewhere
# this class provides a convenient way to have a single NoiseSource which incorporates all of those kinds of noise
class Noisemaker(NoiseSource):
    def __init__(self, white_noise_params=[0, 0], brown_noise_step=0, spike_noise_params=[0, 0, 0]):
        super().__init__()
        self.noise_sources = []  # list of noise sources
        if white_noise_params != [0, 0]:  # for each type of NoiseSource, it is only added to the list if it has non-zero parameters
            self.noise_sources.append(WhiteNoiseSource(max_val=white_noise_params[0], min_val=white_noise_params[1]))
        if brown_noise_step != 0:
            self.noise_sources.append(BrownNoiseSource(max_step_size=brown_noise_step))
        if spike_noise_params != [0, 0, 0]:
            self.noise_sources.append(SpikeNoiseSource(prob=spike_noise_params[0], pos_size=spike_noise_params[1],
                                                neg_size=spike_noise_params[2]))

    # step noisemaker
    def step(self, dt):
        self.noise = 0
        for noise_source in self.noise_sources:  # for all noise sources, effects are accumulated
            self.noise += noise_source.step(dt)  # accumulated noise may be positive or negative
        return super().step(dt)  # call NoiseSource step to store noise for later analysis


####################################################################################
#                           NoiseSource classes end
####################################################################################
