#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.simulators import VehicleSimulator

# simulatorの初期化 (Appendix参照)
simulator = VehicleSimulator(obstacle_num=5)

while simulator:
    # 現在のセンサー情報を取得
    sensor_data = simulator.get_sensor_data()
    # ブライテンベルグ・ビークルの内部
    left_wheel_speed  = 20 + 20 * sensor_data["left_distance"]
    right_wheel_speed = 20 + 20 * sensor_data["right_distance"]
    # アクションを生成してアップデート
    action = [left_wheel_speed, right_wheel_speed]
    simulator.update(action)
