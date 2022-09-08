from CTRNN_Evolution import CTRNN_Evolution
from CTRNN import CTRNN

import numpy as np

def test_ctrnn(dt, world_params={}):

    I = np.zeros((20,1), dtype=float)

    ctrnn_embryology = CTRNN_Evolution(ctrnn_genotype=None,
            dt = dt,
            hidden_nodes=20,
            interval=100,
            trials=0,
            use_genotype_file=False,
            world_params=world_params)

    ctrnn_geno = ctrnn_embryology.get_random_genotype()
    w, tau, bias = ctrnn_embryology.unpack_genotype(ctrnn_geno, nodes=20)
    network = CTRNN(w, tau, bias, num_units = 2)

    print(type(dt))
    # homeo_sim = Homeostat_Simulation(network=network, dt=dt, **world_params)

    outputs = network.step(I)
    print(outputs[:4])
    print(outputs[4:])
    print(outputs)

if __name__ == "__main__":
    disturb_times = [150, 350, 550, 750, 100, 1250, 1500, 1750]
    duration = 1
    lower_viability=-1
    upper_viability=1
    lower_limit=-10
    upper_limit=10
    wait_time=10
    unit_num=2

    dt = 0.01

    # world_params = {duration = 1, lower_viability=-1, upper_viability=1, lower_limit=-10, 
    #         upper_limit=10, wait_time=10, unit_num=2, disturb_times=disturb_times}
    world_params = (duration, lower_viability, upper_viability,
            lower_limit, upper_limit, wait_time, unit_num, disturb_times)

    test_ctrnn(dt, world_params)
