import json
import pickle
# from datatime import datetime
from numpyencoder import NumpyEncoder

from CTRNN_Evolution import CTRNN_Evolution
from microbial_ga import MicrobialGA



def evolve_network(ctrnn_genotype=None,
                 generations_n=10,
                 individuals_n=6,
                 gene_transfer_rate=0.5,
                 mutation_rate=0.05,
                 save_to_file=True,
                 store_only_best=False,
                 interval=100,
                 dt=0.01,
                 hidden_nodes=20,
                 run_parallel=True,
                 replace_rate=0,
                 ranking_level=0,
                 use_genotype_file=None,
                 trials=12,
                 homeo_params={}):

    ctrnn_embryology = CTRNN_Evolution(ctrnn_genotype = ctrnn_genotype,
                                dt=dt,
                                hidden_nodes=hidden_nodes,
                                interval=interval,
                                trials=trials,
                                use_genotype_file=use_genotype_file,
                                homeo_params=homeo_params)

    ga = MicrobialGA(ctrnn_embryology=ctrnn_embryology,
                    generations_n=generations_n,
                    individuals_n=individuals_n,
                    gene_transfer_rate=gene_transfer_rate,
                    mutation_rate=mutation_rate,
                    replace_rate=replace_rate,
                    ranking_level=ranking_level)

    ga.run()

    data = ga.generations_data
    best_solution_fitness = data[-1]['best_individual_fitness']
    best_solution_genotype = data[-1]['best_individual_genotype']
    print('Best solution was:')
    print(best_solution_fitness)
    print('Genotype:')
    print(best_solution_genotype)

    data = {
        'best_solution': {
            'fitness': best_solution_fitness,
            'genotype': best_solution_genotype
        },
        'run': data,
        'settings': {
            'ga': {
                'generations': generations_n,
                'population': individuals_n,
                'gene_transfer_rate': gene_transfer_rate,
                'mutation_rate': mutation_rate,
                'run_parallel': run_parallel,
                'replace_rate': replace_rate,
                'ranking_level': ranking_level,
            },
            'embryology': {
                'hidden_nodes': hidden_nodes,
                'interval': interval,
                'trials': trials,
            }
        },
    }
    path = f'./results/best_soultion.txt'

    pickling_on = open(path,'wb')
    pickle.dump(best_solution_genotype, pickling_on)
    pickling_on.close()


    return data, best_solution_genotype, ctrnn_embryology


if __name__ == "__main__":

    disturb_times = [150, 550, 1250]
    homeo_params = {'duration':2000, 'lower_viability':-1, 'upper_viability':1, 'lower_limit':-10, 
            'upper_limit':10, 'wait_time':10, 'unit_num':2, 'seed': None, 'disturb_times':disturb_times}


    data, best_solution_genotype, embroyology = evolve_network(ctrnn_genotype=None,
                                                             generations_n=5,
                                                             individuals_n=30,
                                                             gene_transfer_rate=0.5,
                                                             mutation_rate=0.1,
                                                             save_to_file=True,
                                                             store_only_best=False,
                                                             interval=100,
                                                             dt=0.01,
                                                             hidden_nodes=12,
                                                             replace_rate=0,
                                                             ranking_level=0,
                                                             use_genotype_file=None,
                                                             trials=12,
                                                             homeo_params=homeo_params)
