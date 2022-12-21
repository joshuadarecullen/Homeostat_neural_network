import matplotlib.pyplot as plt
import time
import numpy as np

def sigmoid(y, bias):
    return 1 / (1 + np.exp(-(y + bias)))

class CTRNN:

    def __init__(self, w, tau, bias, num_units=0, dt=0.01):

        self.total_time = float(dt)
        self.dt = float(dt)

        self.index = num_units*4
        self.w = w
        self.tau = tau
        self.bias = bias
        self.n_nodes = w.shape[0]
        self.y = [np.zeros((self.n_nodes, 1), dtype=float)]
        self.output_neurons = [np.zeros((num_units*2, 1), dtype=float)]

    def step(self, inputs):

        iterations = int(self.total_time / self.dt) # dictate amount of iterations before collecting using neuron outputs

        # reshape to ensure correct size
        I = np.reshape(inputs, (self.n_nodes, 1)) 

        for i in range(0, iterations):
            self.iterate(I)

        yt = self.y[-1]

        # keeping history of scaled output neurons
        self.output_neurons.append(np.tanh(yt[[8,9,10,11], 0]))

        return self.output_neurons[-1] # return amoutn to be applied to the weights


    # perform the intergration of the neurons
    def iterate(self, I):

        yt = self.y[-1]

        yt1 = yt + self.dt * (1/self.tau) * (-yt + self.w @sigmoid(yt, self.bias) + I)

        self.y.append(yt1)


    def output(unit_num):
        if unit_num == 0:
            return output_neuron[:2]
        if unit_num == 1:
            return output_neuron[2:]

        return self.output_neurons[-1]


    def show(self):
        #plt.ion()
        plt.figure()

        time = range(1, len(self.y))

        y = np.array(self.y[1:])
        y = y.reshape(y.shape[0], y.shape[1])
        y = y[:, [-8, -9, -10, -11]]
        
        # raw values of the ouput neurons
        plt.plot(time, y, linewidth=0.75)
        plt.title('CTRNN Output Neurons')
        plt.ylabel('y')
        plt.xlabel('time')
        plt.legend(['w1','w2','w3','w4'])
        plt.show(block=True)


        # tanh of the output neurons
        tany= np.array(self.output_neurons[1:])
        plt.plot(time, tany, linewidth=0.75)
        plt.title('CTRNN Output Neurons')
        plt.ylabel('tany')
        plt.xlabel('time')
        plt.legend(['w1','w2','w3','w4'])
        plt.show(block=True)


    def set_totaltime(self, total):
        self.total_time = total
