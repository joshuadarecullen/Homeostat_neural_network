import os
import numpy as np

# converts the queue to a numpy
def queue_to_array(queue):
    result = []
    while not queue.empty():
        result.append(queue.get())

    return np.array(result)

def get_info(filename=None, file_index=-1):
    data = get_data(filename, file_index)

    r = { 'settings': data['settings'],
          'fitness': data['best_solution']['fitness']}

    return r

