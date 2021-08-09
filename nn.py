import random as rand
import math

def logistic(layer, weight, bias):
    sum = 0
    for neuron in layer:
        sum += neuron.get_value()
    sum *= weight
    sum += bias
    return 1 / (1 + math.exp(sum))

def linear(layer, weight, bias):
    sum = 0
    for neuron in layer:
        sum += neuron.get_value()
    sum *= weight
    sum += bias
    return sum

def binary(layer, weight, bias):
    sum = 0
    for neuron in layer:
        sum += neuron.get_value()
    sum *= weight
    sum += bias
    if sum > 0:
        return 1
    else:
        return -1

class NeuralNet:
    def __init__(self, layers, activation):
        last_layer = None
        #for each layer, starting with the input
        for layer in layers:
            cur_layer = []
            #for each neuron
            for i in range(layer):
                if last_layer is not None:
                    cur_layer.append(Neuron(activation, last_layer))
                else:
                    cur_layer.append(Neuron(activation))
                    self.input = cur_layer
            last_layer = cur_layer
        self.output = last_layer
    
    def get_neuron(self, layer, neuron):
        layers = [self.output]
        cur_layer = self.output
        while cur_layer[0].layer is not None:
            cur_layer = cur_layer[0].layer
            layers.insert(0, cur_layer)
        return layers[layer][neuron]


class Neuron:
    def __init__(self, activation, layer = None):
        self.layer = layer
        self.activation = activation
        #randomly decide weight and bias
        self.weight = rand.random()
        self.bias = rand.random()
        #randomly decide sign
        if(rand.random() > 0.5):
            self.weight *= -1
        if(rand.random() > 0.5):
            self.bias *= -1

    def get_value(self):
        if self.layer is None:
            return self.value

        self.value = self.activation(self.layer, self.weight, self.bias)
        return self.value

    def set_value(self, value):
        self.value = value

if __name__ == "__main__":
    test_net = NeuralNet([2, 20, 4], binary)
    test_net.input[0].set_value(4)
    test_net.input[1].set_value(6)

    out = []

    for neuron in test_net.output:
        out.append(test_net.get_neuron(1, 5).weight)
    print("output before: " + str(out))

    test_net.get_neuron(1, 5).weight = 500

    out = []
    for neuron in test_net.output:
        out.append(test_net.get_neuron(1, 5).weight)
    print("output after: " + str(out))