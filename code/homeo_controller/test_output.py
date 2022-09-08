import pickle

from CTRNN_Evolution import CTRNN_Evolution
from microbial_ga import MicrobialGA



def evolve_network(ctrnn_genotype=None,
                 interval=100,
                 dt=0.01,
                 hidden_nodes=20,
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



    ctrnn_embryology.output()

if __name__ == "__main__":

    disturb_times = [250, 700, 1200, 1600]
    homeo_params = {'duration':2000, 'lower_viability':-1, 'upper_viability':1, 'lower_limit':-10, 
            'upper_limit':10, 'wait_time':10, 'unit_num':2, 'seed': None, 'disturb_times':disturb_times}

    path = './results/best_solution.txt'
    pickling_on = open(path,'rb')
    ctrnn_genotype = pickle.load(pickling_on)
    print(ctrnn_genotype)
    evolve_network(ctrnn_genotype=ctrnn_genotype,
            interval=100,
            dt=0.01,
            hidden_nodes=12,
            use_genotype_file=None,
            trials=12,
            homeo_params=homeo_params)
