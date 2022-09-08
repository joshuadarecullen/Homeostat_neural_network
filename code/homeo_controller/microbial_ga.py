import copy
import time
import numpy as np
from scipy.stats import bradford
import random
from random import randint

from multiprocessing import Process, Queue
from utils import queue_to_array

# implementation of a Microbial GA
class MicrobialGA:

    def __init__(self, ctrnn_embryology,
            generations_n=100,
            individuals_n=30,
            gene_transfer_rate=0.5,
            mutation_rate=0.1,
            replace_rate=0.5,
            ranking_level=0):

        self.calculate_fitness = ctrnn_embryology.calculate_fitness
        self.get_random_genotype = ctrnn_embryology.get_random_genotype
        self.ctrnn_embryology = ctrnn_embryology
        self.individuals_n = individuals_n
        self.generations_n = generations_n
        self.gene_transfer_rate = gene_transfer_rate
        self.mutation_rate = mutation_rate
        self.replace_rate = replace_rate
        self.ranking_level = ranking_level

        self.best_individual_fintesses = []
        self.best_historical_fintess = -np.inf
        self.generation_number = 0
        self.generations_data = []


    def initialize_population(self):
        """
        initialized population as a dictionary,
        where each individual obtains a random a genotype and its fitness
        """
        self.population = []

        for _ in range(self.individuals_n):
            genotype = self.get_random_genotype()
            fitness = self.calculate_fitness(genotype)

            individual = {'genotype': genotype, 'fitness': fitness}

            self.population.append(individual)

        self.population = np.array(self.population)

        self.store_generation_data()


    def store_generation_data(self):
        generation_data = {
            'number': self.generation_number,
            'total_fitness': 0,
            'best_individual_genotype': None,
            'best_individual_fitness': None,
            'individuals': []
        }

        best_individual = self.population[0]

        # loop over individuals in the population
        for individual in self.population:
            generation_data['individuals'].append(copy.deepcopy(individual))

            # update the best fit individual
            if individual['fitness'] > best_individual['fitness']:
                best_individual = individual

        generation_data['best_individual_genotype'] = best_individual['genotype']
        generation_data['best_individual_fitness'] = best_individual['fitness']

        self.best_individual_fintesses.append(best_individual['fitness'])
        self.best_historical_fintess = best_individual['fitness']

        # keep track of generation data
        self.generations_data.append(generation_data)


    def mutate(self, value, gene_id, mut_prob):
        """mutation of one gene """

        # mutation is guaranteed to be in (-1, 1)
        value += random.gauss(0.0,mut_prob)

        if value > 1:
            value = 1

        if value < -1:
            value = -1

        return value

    # prevent from competing individual with itself
    def get_random_individual(self, resticted_id=None, min_id=0):
        """
        returns random individual from population if the restricted_id is provided and
        ensures selected individual in not the same, that restricted one if not, executes recursively
        """
        # prioritize good solutions in competing
        if self.ranking_level:
            last_id = len(self.population) - 1
            length = last_id - min_id
            dist = bradford(3, min_id, length)
            individual_id = int(dist.rvs())
            individual_id = last_id - individual_id + min_id

        else:
            individual_id = np.random.randint(min_id, len(self.population))

        # the prevention of individuals competing with themselves
        if resticted_id is not None and individual_id == resticted_id:
            return self.get_random_individual(resticted_id)

        return self.population[individual_id], individual_id


    def get_winner_and_looser(self, individual_1, individual_2):

        if individual_1['fitness'] > individual_2['fitness']:
            return individual_1, individual_2

        return individual_2, individual_1


    # iterate over the genos in the genotype
    def microbial_sex(self, winner, loser):
        for i, _ in enumerate(winner['genotype']):
            if self.gene_transfer_rate > np.random.random():
                loser['genotype'][i] = winner['genotype'][i]

            if self.mutation_rate > np.random.random():
                loser['genotype'][i] = self.mutate(loser['genotype'][i], i, self.mutation_rate)


    def round(self, new_popultaion_q, individual_1, individual_2):

        # reset random seed
        np.random.seed()

        # take a copy of the individuals
        individual_1 = copy.deepcopy(individual_1)
        individual_2 = copy.deepcopy(individual_2)

        winner, loser = self.get_winner_and_looser(individual_1, individual_2)

        # and mutate loser genes with mutation_rate
        self.microbial_sex(winner, loser)

        # update fitness function for loser
        loser['fitness'] = self.calculate_fitness(loser['genotype'])

        new_popultaion_q.put(loser)
        new_popultaion_q.put(winner)


    def tournament_selection(self):

        new_popultaion_q = Queue()
        processes = []

        np.random.shuffle(self.population)

        # repeat number of individuals / 2 times
        for i in range(int(self.individuals_n / 2)):
            individual_1 = self.population[i * 2]
            individual_2 = self.population[i * 2 + 1]
            p = Process(target=self.round, args=(new_popultaion_q, individual_1, individual_2))
            p.start()
            processes.append(p)

        # start the processes
        for p in processes:
            p.join()

        # convert the queue to an array
        self.population = queue_to_array(new_popultaion_q)


    def replace_poor(self):

        if not self.replace_rate:
            return

        # remove bottom half of the replace_rate solutions
        self.population = sorted(self.population, key=lambda x: x['fitness'])

        last_poor = int(self.individuals_n * self.replace_rate)
        first_top = last_poor + 1

        for i in range(int(self.individuals_n * self.replace_rate)):
            ind, _ = self.get_random_individual(min_id=first_top)
            ind = copy.deepcopy(ind)

        for j, _ in enumerate(ind['genotype']):
            if self.mutation_rate > np.random.random():
                ind['genotype'][j] = self.mutate(ind['genotype'][j], j, self.mutation_rate)

            ind['fitness'] = self.calculate_fitness(ind['genotype'])
            self.population[i] = ind


    # main function to evolve ctrnn
    def run(self):

        # initialize population
        self.initialize_population()

        # monitor time taken to execute
        self.start_time = time.time()

        # main hook to evolve of the generations
        while self.generation_number < self.generations_n:

            start = time.time()

            self.generation_number += 1

            print(f'\nGeneration {self.generation_number} of {self.generations_n}')

            self.tournament_selection()

            # finally, replace the poor indviduals in the population
            self.replace_poor()
            self.store_generation_data()

        print(f'Best fitness {self.best_historical_fintess}')
        print(f'Evaluation time: {time.time() - start}')

        print(f'\ntotal time: {time.time() - self.start_time:.2f}\n')
