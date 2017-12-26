#!/usr/bin/env python

import numpy as np
from simulator import TwoWheelVehicleRobotSimulator


#def controll_func(left_sensor, right_sensor):
def controll_func(sensor_data):
    left_wheel_speed = 30 * (1 - sensor_data["right_touch"])
    right_wheel_speed = 30 * (1 - sensor_data["left_touch"])
    return left_wheel_speed, right_wheel_speed


sim = TwoWheelVehicleRobotSimulator(obstacle_num=5)
sim.controll_func = controll_func
sim.run()
