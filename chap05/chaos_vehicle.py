#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
カオス的な振る舞いのビークル実験用コード
"""

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from t3 import T3
from alifebook_lib.simulators import VehicleSimulator

simulator = VehicleSimulator(obstacle_num=0)
t3 = T3(omega0 = 0.9, omega1 = 0.3, epsilon = 0.1)

t3.set_parameters(omega0 = np.random.rand())
t3.set_parameters(omega1 = np.random.rand())

while simulator:
    sensor_data = simulator.get_sensor_data()
    x, y = t3.next()
    left_wheel_speed = 50 * x
    right_wheel_speed = 50 * y
    action = [left_wheel_speed, right_wheel_speed]
    simulator.update(action)
