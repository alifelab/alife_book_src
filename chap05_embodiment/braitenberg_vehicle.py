#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.simulators import TwoWheelVehicleRobotSimulator


def controll_func(sensor_data):
    left_wheel_speed = 20 + 20 * sensor_data["left_distance"]
    right_wheel_speed = 20 + 20 * sensor_data["right_distance"]
    return left_wheel_speed, right_wheel_speed

sim = TwoWheelVehicleRobotSimulator(controll_func, obstacle_num=5)
sim.controll_func = controll_func
sim.run()
