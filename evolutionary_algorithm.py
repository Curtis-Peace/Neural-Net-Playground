from nn import *
from game import *
import multiprocessing as mp
from datetime import datetime
import sys
import os
import random as rand

class EvolutionaryAlgorithm:
    def __init__(self, net_layers, net_activation, generation_size, num_survive, mutation_factor):
        self.net_layers = net_layers
        self.net_activation = net_activation
        self.generation_size = generation_size
        self.generation = []
        self.num_survive = num_survive
        self.mutation_factor = mutation_factor
        for i in range(generation_size):
            neural_net = NeuralNet(self.net_layers, self.net_activation)
            self.generation.append(neural_net)


    def run_game(self, net):
        theApp = Game(False, net, 5000)
        return theApp.on_execute()

    def get_scores(self):
        with mp.Pool(processes=8) as p:
            scores = p.map(self.run_game, self.generation)
            return scores

    def get_average(self, sorted_by_score):
        average_net = NeuralNet(self.net_layers, self.net_activation)
        
        #for each hidden layer
        for i in range(1, len(self.net_layers)):
            #for each neuron in hidden layer
            for j in range(self.net_layers[i]):
                #sum_weight = 0
                sum_bias = 0
                num_weights = len(average_net.get_neuron(i, j).weights)
                new_weights = [0] * num_weights
                #for each network in top num
                for k in range(self.num_survive):
                    sum_bias += sorted_by_score[k][0].get_neuron(i, j).bias
                    #for each weight
                    for l in range(num_weights):
                        new_weights[l] += average_net.get_neuron(i, j).weights[l] / self.num_survive
                average_net.get_neuron(i, j).weights = new_weights
                average_net.get_neuron(i, j).bias = sum_bias / self.num_survive

        return average_net

    def new_generation(self, scores):
        sorted_by_score = sorted(tuple(zip(self.generation, scores)), key = lambda tup: tup[1], reverse = True)
        average = self.get_average(sorted_by_score)
        for net in self.generation:
            #for each hidden layer
            for i in range(1, len(self.net_layers)):
                #for each neuron in hidden layer
                for j in range(self.net_layers[i]):
                    #for each weight
                    for k in range(len(net.get_neuron(i, j).weights)):
                        mutation_weight = rand.random() * self.mutation_factor
                        #randomly decide sign
                        if(rand.random() > 0.5):
                            mutation_weight *= -1
                        net.get_neuron(i, j).weights[k] = average.get_neuron(i, j).weights[k] + mutation_weight
                    mutation_bias = rand.random() * self.mutation_factor
                    #randomly decide sign
                    if(rand.random() > 0.5):
                        mutation_bias *= -1
                    net.get_neuron(i, j).bias = average.get_neuron(i, j).bias + mutation_bias
        #preserve top
        self.generation[0] = sorted_by_score[0][0]

    
if __name__ == "__main__" :
    ea = EvolutionaryAlgorithm([4, 20, 20, 4], relu, 500, 5, .02)
    i = 0
    while True:
        scores = ea.get_scores()
        print(i, sorted(scores, reverse=True)[0:15])
        ea.new_generation(scores)
        i += 1