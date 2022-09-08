import numpy as np
import matplotlib.pyplot as plt
import sys

from multiprocessing import Process, Queue
from utils import queue_to_array

from Homeostat_sim import Homeostat_Simulation

from CTRNN import CTRNN

class CTRNN_Evolution:

    def __init__(self ,ctrnn_genotype = None,
                 dt = 0.01,
                 hidden_nodes = 20,
                 interval = 100,
                 trials = 12,
                 use_genotype_file = None,
                 homeo_params = {}):

        self.dt = dt
        self.interval = interval
        self.use_genotype_file = use_genotype_file
        self.total_nodes = hidden_nodes
        self.homeo_params = homeo_params
        self.trials = trials

        self.ctrnn_genotype = ctrnn_genotype


    def run_simulation(self, fitnesses_q, w, tau, theta):

        # set up homeostat simulation
        homeo_sim = Homeostat_Simulation(dt=self.dt, **self.homeo_params)

        # set up ctrnn with current genotype parameters
        network = CTRNN(w, tau, theta, num_units=0, dt = self.dt)

        # run simulation
        ts, unit_instability_times, _ = homeo_sim.run_simulation_once(network, interval=self.interval)

        # calculate the ctrnns fitness for the simulation run
        fitness = homeo_sim.fitness(unit_instability_times)

        # put into the queue
        return fitnesses_q.put(fitness)


    def calculate_fitness(self, genotype):

        """run simulation given the amount of trials provided"""

        # unpack genotype
        w, tau, bias = self.unpack_genotype(genotype, self.total_nodes)

        fitnesses_q = Queue()
        processes = []

        # run simulations using multiprocessing
        for i in range(self.trials):

            # target function and its parameters
            p = Process(target=self.run_simulation,
                        args=(fitnesses_q, w, tau, bias))
            p.start()
            # add process to list
            processes.append(p)

        # begin processes
        for p in processes:
            p.join()

        fitnesses = queue_to_array(fitnesses_q)

        # catches any nan that may occur from overflow and break numpy mean opperation
        if len(fitnesses) == 0:
            return 0


        # calculate mean of the fitness of the simulations
        fitness = fitnesses.mean()

        return fitness


    # grabs parameters from their place in the genotype
    def take_genes(self, genotype, start, number):
        new_start = start + number
        return genotype[start: start + number], new_start


    def get_random_genotype(self):

        # get the require lengths of the paramters of the ctrnn
        weights_n = self.total_nodes ** 2
        tau_n = self.total_nodes
        theta_n = self.total_nodes

        genes_n = weights_n + tau_n + theta_n
        genotype = np.random.random(size=(genes_n, )) # 168 float

        return genotype


    def unpack_genotype(self, genotype, nodes=None, inputs=1):
        ## unpacking gene 
        # start with gene position 0

        pos = 0

        weights, pos = self.take_genes(genotype, pos, nodes ** 2)
        tau, pos = self.take_genes(genotype, pos, nodes)
        theta, pos = self.take_genes(genotype, pos, nodes)


        # scale the values of the weights from [0, 1] to [-10, 10]
        w = weights.reshape(nodes, nodes)
        w = -10 + w * 20

        # scale the values of the time constant from [0, 1] to [0.1, 5]
        tau = 0.1 + tau.reshape(nodes, 1) * 4.9

        # scale the values of the biases from [0, 1] to [-5, 5]
        theta = -5 + theta.reshape(nodes, 1) * 10

        return w, tau, theta


# Function to test a evolved genotype
    def output(self):

        w, tau, theta = self.unpack_genotype(self.ctrnn_genotype, self.total_nodes)

        homeo_sim = Homeostat_Simulation(dt=self.dt, **self.homeo_params)

        network = CTRNN(w, tau, theta, num_units=0, dt = self.dt)

        ts, _ , homeostat = homeo_sim.run_simulation_once(network, interval=self.interval)
        duration, lower_viability, upper_viability, lower_limit, upper_limit, wait_time, unit_num, seed, disturb_times= self.homeo_params

        # plot all homeostat unit variables over time
        plt.figure()
        for i, unit in enumerate(homeostat.units):
            plt.plot(ts, unit.theta, label='Unit ' + str(i) + ': essential variable')
        plt.plot([ts[0], ts[-1]], [upper_viability, upper_viability], 'r--', label='upper viable boundary')
        plt.plot([ts[0], ts[-1]], [lower_viability, lower_viability], 'r--', label='lower viable boundary')
        plt.title('Essential variables')
        plt.xlabel('t')
        plt.ylabel('Essential variable')
        plt.legend()

        # plot times when homeostat units were adapting
        plt.figure()
        for i, unit in enumerate(homeostat.units):
            plt.plot(ts, unit.was_adapting, label='Unit ' + str(i) + ': was adapting')
        plt.title('Units were adapting')
        plt.xlabel('t')
        plt.ylabel('Adapting')
        plt.legend()

        # plot all homeostat unit weights over time
        plt.figure()
        for i, unit in enumerate(homeostat.units):
            plt.plot(ts[1:], unit.weights_were, label='Unit ' + str(i) + ': weight')
        plt.title('Homeostat unit weights')
        plt.xlabel('t')
        plt.ylabel('Weights')
        plt.legend()

        plt.show()

        network.show()
