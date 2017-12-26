#!/usr/bin/env python

import numpy as np
from abc import abstractmethod
from simulator import TwoWheelVehicleRobotSimulator

class SubsumptionModule(object):
    def __init__(self, input_dim, output_dim):
        super(SubsumptionModule, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.inputs = np.zeros(input_dim)
        self.outputs = np.zeros(output_dim)
        self.child_modules = {}
        self.on_init()

    def add_child_module(self, name, module):
        self.child_modules[name] = module

    def set_inputs(self, inputs):
        self.inputs = inputs
        for m in self.child_modules.values():
            m.set_inputs(inputs)

    def update(self):
        for m in self.child_modules.values():
            m.update()
        self.on_update()

    @abstractmethod
    def on_init(self):
        pass

    @abstractmethod
    def on_update(self):
        pass


class AvoidModule(SubsumptionModule):
    def on_init(self):
        pass

    def on_update(self):
        self.outputs[0] = 30 * (1 - self.inputs[1])
        self.outputs[1] = 30 * (1 - self.inputs[0])


class WanderModule(SubsumptionModule):
    TURN_START_STEP = 100
    TURN_END_STEP = 150
    def on_init(self):
        self.counter = 0
        self.add_child_module('avoid', AvoidModule(self.input_dim, self.output_dim))

    def on_update(self):
        # count steps not senser activated
        if np.max(self.inputs) > 0:
            self.counter = 0
        else:
            self.counter = (self.counter + 1) % self.TURN_END_STEP
        if self.counter < self.TURN_START_STEP:
            # not inhibit avoid module
            self.outputs[0] = self.child_modules['avoid'].outputs[0]
            self.outputs[1] = self.child_modules['avoid'].outputs[1]
        elif self.counter == self.TURN_START_STEP:
            # suppress child avoid module and start turning
            if np.random.rand() < 0.5:
                self.outputs[0] = 20
                self.outputs[1] = 30
            else:
                self.outputs[0] = 30
                self.outputs[1] = 20
        else:
            pass


######################
# change architecture
######################

# controller = AvoidModule(2, 2)  # same as braitenberg vehicle
controller = WanderModule(2, 2)  # add wandering module

def controll_func(left_sensor, right_sensor):
    controller.set_inputs([left_sensor, right_sensor])
    controller.update()
    return controller.outputs

if __name__ == '__main__':
    sim = TwoWheelVehicleRobotSimulator(obstacle_num=3, feed_num=30)
    sim.controll_func = controll_func
    sim.run()
