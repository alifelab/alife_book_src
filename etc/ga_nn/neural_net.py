#!/usr/bin/env python

import numpy as np

class NeuralNet(object):
    def __init__(self, input_num, hidden_num, output_num):
        super(NeuralNet, self).__init__()
        self.input_num = input_num
        self.hidden_num = hidden_num
        self.output_num = output_num
        self.weight_0 = np.random.rand(input_num, hidden_num)
        self.bias_0 = np.random.rand(hidden_num)
        self.weight_1 = np.random.rand(hidden_num, output_num)
        self.bias_1 = np.random.rand(output_num)


    def get_genotype_length(self):
        return self.weight_0.size + self.bias_0.size + self.weight_1.size + self.bias_1.size


    def get_genotype(self):
        gt = np.r_[self.weight_0.flatten(), self.bias_0.flatten(), self.weight_1.flatten(), self.bias_1.flatten()]
        return gt


    def set_genotype(self, genotype):
        weight_0_index = 0
        bias_0_index = self.weight_0.size
        weight_1_index = bias_0_index + self.bias_0.size
        bias_1_index = weight_1_index + self.weight_1.size
        self.weight_0 = genotype[weight_0_index:bias_0_index].reshape(self.weight_0.shape)
        self.bias_0 = genotype[bias_0_index:weight_1_index]
        self.weight_1 = genotype[weight_1_index:bias_1_index].reshape(self.weight_1.shape)
        self.bias_1 = genotype[bias_1_index:]


    def __activate(self, v, gain=1.0):
        return 1. / (1 + np.exp(-gain * v))

    def calc(self, input_data):
        assert len(input_data) == self.weight_0.shape[0]
        hidden = self.__activate(np.dot(input_data, self.weight_0) + self.bias_0)
        out = self.__activate(np.dot(hidden, self.weight_1) + self.bias_1)
        return out

    def calc_binary(self, input_data):
        out = self.calc(input_data)
        out_bin = []
        for o in out:
            if out < 0.5:
                out_bin.append(0)
            else:
                out_bin.append(1)
        return out_bin
