#!/usr/bin/env python

import unittest
import numpy as np
from neural_net import NeuralNet

class TestNeuralNet(unittest.TestCase):
    def setUp(self):
        self.nn = NeuralNet(2,2,1)

    def test_get_genotype_length(self):
        self.assertEqual(self.nn.get_genotype_length(), 2*2 + 2 * 2 + 1)

    def tearDown(self):
        pass


    def test_genotype(self):
        l = self.nn.get_genotype_length()
        gt = np.random.rand(l)
        self.nn.set_genotype(gt)
        gt2 = self.nn.get_genotype()
        self.assertTrue(np.all(gt==gt2))

    def test_calc(self):
        gt = np.zeros(self.nn.get_genotype_length())
        self.nn.set_genotype(gt)
        input_data = np.ones(2)
        output = self.nn.calc(input_data)
        self.assertEqual(output, 0)


if __name__ == '__main__':
    unittest.main()
