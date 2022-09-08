import sys
# path folder which contains situsim_v1_2
sys.path.insert(1, '/home/joshua/Documents/homeo_coursework/situsim')
sys.path.insert(1, '/home/joshua/Documents/homeo_coursework/situsim/situsim_extensions')

from situsim_v1_2 import *
from situsim_extensions import *

import pygame
import matplotlib.pyplot as plt
import numpy as np
import time

from Homeostat import Homeostat

from disturbances import DisturbanceSource
from disturbances import UnitVariableDisturbanceSource


class Homeostat_Simulation:

    def __init__(self, dt=0.01, duration=2000, lower_viability=-1, upper_viability=1, lower_limit=-10,
                          upper_limit=10, wait_time=10, unit_num=2, seed=None, disturb_times=[]):

        self.duration = duration
        self.dt = dt
        self.disturb = bool(disturb_times) # only disturb if the times list is not empty
        self.disturb_times = disturb_times
        self.unit_num = unit_num
        self.target = len(disturb_times)

        if seed is not None:
            np.random.seed(seed)

        # construct a Homeostat
        self.homeostat = Homeostat(lower_viability=-1, upper_viability=1, lower_limit=-10,
                          upper_limit=10, wait_time=10, unit_num=2)

    
        if self.disturb:
            disturber = UnitVariableDisturbanceSource(self.homeostat.units[0], self.disturb_times)

            # disturbance list
            self.disturbances = [disturber]


    def fitness_speed(self, unit_instability_times, target):

        reward = 0

        for unit in unit_instability_times:
            total_time = 0
            total_time = sum(unit)

            reward += 1 - (total_time / self.duration) # longer unstable to lower the reward

        return reward # max = 2


    def recovery_amount(self, instability_times, target):

        reward = 0

        for unit_times in instability_times:
            count = len(unit_times)

            # the less amount of times unstable, the higher the score
            # minimum times will be the amount of disturbances
            if count < target and count != 0:
                if unit_times[0] != 2000:
                    reward += count / target
            elif count > target:
                reward += target / count
            elif count == target:
                reward += 1

        return reward # max = 2


    def fitness(self, instability_times):  

        max_num = len(instability_times)

        # Two components
        # first reward how many successful recoveries from instabilty
        # 1. recovery rate (max = num units), max one for each unit
        recovery_reward = self.recovery_amount(instability_times, self.target)

        # 2. speed to stability, max 1 for each unit
        speed_reward = self.fitness_speed(instability_times, self.target)
        reward = recovery_reward + speed_reward

        # scale between 0 and 1, by dividing by the amount of units and the potential max score
        fitness = reward / (max_num * 2)

        return fitness


    def run_simulation_once(self, network, interval):

        # prepare simulation time variables
        t = 0
        ts = [t]
        dt = 0.01

        # the CTRNN data
        network_outputs = [np.zeros((self.unit_num*2, 1), dtype=float)]
        current_outputs = np.zeros((self.unit_num*2,1))
        I_overtime = [np.zeros((self.unit_num*6, 1), dtype=float)]

        # run Homeostat simulation
        while t < self.duration:

            I_1 = np.zeros((self.unit_num*6,1), dtype=float)
            I = []

            # collect the input for the CTRNN network from all units
            for j, unit in enumerate(self.homeostat.units):
                I.append(unit.get_theta())
                I.append(unit.theta_dot[-1])
                for i in unit.weights:
                    I.append(i)

            # 0-7 in the array are inputs
            for i in range(len(I)):
                I_1[i,0] = I[i]

            # track inputs over times
            I_overtime.append(I_1)

            # Step the CTRNN
            network_outputs.append(network.step(I_1))
            current_output = network_outputs[-1]

            # step Homeostat, take the current output of the ctrnn.
            self.homeostat.step(self.dt, current_output)

            if self.disturb:
                # step any disturbances
                for d in self.disturbances:
                    d.step(self.dt)

            # increment time variable and store in ts list for plotting later
            t += dt
            ts.append(t)

        # for loop sequence collects the instability times for each unit
        unit_instability_times = []

        # collect the times taken to stabilise for each unit 
        for i, unit in enumerate(self.homeostat.units):

            # print(unit.get_instability_times())
            if len(unit.get_instability_times()) != 0 and unit.get_current_instability_time() ==0:
                unit_instability_times.append(unit.get_instability_times())

            # check whether the system is unstable at the end of the simulation
            elif len(unit.get_instability_times()) != 0 and unit.get_current_instability_time() != 0:
                unit_times = unit.get_instability_times() 
                init_in = unit.get_initial_instability_time()
                unit_times.append(unit.get_current_instability_time()-init_in) # calculate time of instability
                unit_instability_times.append(unit_times)
            else:
                # if empty set to length of simulation to avoid error in fitness function
                unit_time = [self.duration]
                unit_instability_times.append(unit_time)


        return ts, unit_instability_times, self.homeostat
