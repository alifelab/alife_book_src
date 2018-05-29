#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from t3 import T3
from alifebook_lib.simulators import VehicleSimulator

t3 = T3(omega0 = 0.9, omega1 = 0.3, epsilon = 0.1)

simulator = VehicleSimulator(obstacle_num=0)
while simulator:
    sensor_data = simulator.get_sensor_data()
    t3.set_parameters(omega0 = 0.5 + 0.5*sensor_data['left_distance'])
    t3.set_parameters(omega1 = 0.5 + 0.5*sensor_data['right_distance'])
    x, y = t3.next()
    left_wheel_speed = 50 * x
    right_wheel_speed = 50 * y
    action = [left_wheel_speed, right_wheel_speed]
    simulator.update(action)
