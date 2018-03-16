#!/usr/bin/env python

import os, sys
#sys.path.append(os.pardir)

#current_dir = sys.path.abspath(sys.path.dirname(__file__))
#print(current_dir)
#print(
import sys
#sys.path.append('../src')
#parent_dir = path.abspath(path.join(current_dir, pardir))
import numpy as np

from alifebook_lib.simulator import TwoWheelVehicleRobotSimulator
#from .. import alifebook_lib
#from . import simulator


def controll_func(sensor_data):
    left_wheel_speed = 30 * (1 - sensor_data["right_distance"])
    right_wheel_speed = 30 * (1 - sensor_data["left_distance"])
    return left_wheel_speed, right_wheel_speed

sim = TwoWheelVehicleRobotSimulator(controll_func, obstacle_num=5)
sim.controll_func = controll_func
sim.run()

class ClassName(object):
    """docstring for ."""
    def __init__(self, arg):
        super(, self).__init__()
        self.arg = arg
