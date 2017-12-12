#!/usr/bin/env python

import numpy as np
from simulator import TwoWheelVehicleRobotSimulator


def controll_func(left_sensor, right_sensor):
    left_wheel_speed = 30 * (1 - right_sensor)
    right_wheel_speed = 30 * (1 - left_sensor)
    return left_wheel_speed, right_wheel_speed


sim = TwoWheelVehicleRobotSimulator()
sim.controll_func = controll_func
sim.run()
