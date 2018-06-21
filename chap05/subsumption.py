#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from abc import abstractmethod
from alifebook_lib.simulators import VehicleSimulator

class SubsumptionModule(object):
    def __init__(self):
        super(SubsumptionModule, self).__init__()
        self.__inputs = {}
        self.__outputs = {}
        self.child_modules = {}
        self.set_active_module_name("")
        self.on_init()

    def add_child_module(self, name, module):
        self.child_modules[name] = module

    def set_inputs(self, inputs):
        self.__inputs = inputs
        for m in self.child_modules.values():
            m.set_inputs(inputs)

    def get_input(self, name):
        return self.__inputs.get(name, None)

    def set_output(self, name, val):
        self.__outputs[name] = val

    def get_output(self, name):
        return self.__outputs.get(name, None)

    def update(self):
        for m in self.child_modules.values():
            m.update()
        self.on_update()

    def set_active_module_name(self, name):
        self.__active_module_name = name

    def get_active_module_name(self):
        return self.__active_module_name

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
        self.set_output("left_wheel_speed",  10 + 30 * self.get_input("left_distance"))
        self.set_output("right_wheel_speed", 10 + 30 * self.get_input("right_distance"))
        self.set_active_module_name(self.__class__.__name__)


class WanderModule(SubsumptionModule):
    TURN_START_STEP = 100
    TURN_END_STEP = 180
    def on_init(self):
        self.counter = 0
        self.add_child_module('avoid', AvoidModule())

    def on_update(self):
        if self.get_input("right_distance") < 0.001 and self.get_input("left_distance") < 0.001:
            self.counter = (self.counter + 1) % self.TURN_END_STEP
        else:
            self.counter = 0

        if self.counter < self.TURN_START_STEP:
            # counterがTURN_START_STEPに達するまでは下位のモジュールを抑制しない
            self.set_output("left_wheel_speed",  self.child_modules['avoid'].get_output("left_wheel_speed"))
            self.set_output("right_wheel_speed", self.child_modules['avoid'].get_output("right_wheel_speed"))
            self.set_active_module_name(self.child_modules['avoid'].get_active_module_name())
        elif self.counter == self.TURN_START_STEP:
            # ランダムに左回りか右回りを決定して車輪の速度をセットする
            if np.random.rand() < 0.5:
                self.set_output("left_wheel_speed",  15)
                self.set_output("right_wheel_speed", 10)
            else:
                self.set_output("left_wheel_speed",  10)
                self.set_output("right_wheel_speed", 15)
            self.set_active_module_name(self.__class__.__name__)
        else:
            # counterがリセットされるまでは車輪の速度はそのまま
            pass


from t3 import T3

class ChaosWanderModule(SubsumptionModule):
    def on_init(self):
        self.add_child_module('avoid', AvoidModule())
        self.t3 = T3(omega0 = 0.9, omega1 = 0.3, epsilon = 0.1)
        self.t3.set_parameters(omega0 = np.random.rand())
        self.t3.set_parameters(omega1 = np.random.rand())

    def on_update(self):
        x, y = self.t3.next()  # update chaos dynamics
        if self.get_input("right_distance") < 0.001 and self.get_input("left_distance") < 0.001:
            # 距離センサーが触れない間はカオスを利用して動き回る
            left_wheel_speed = 50 * x
            right_wheel_speed = 50 * y
            self.set_output("left_wheel_speed",  left_wheel_speed)
            self.set_output("right_wheel_speed", right_wheel_speed)
            self.set_active_module_name(self.__class__.__name__)
        else:
            # 距離センサーが検知したら、avoid層で回避して、カオスのパラメターも変更して別の振る舞いを獲得する
            self.set_output("left_wheel_speed",  self.child_modules['avoid'].get_output("left_wheel_speed"))
            self.set_output("right_wheel_speed", self.child_modules['avoid'].get_output("right_wheel_speed"))
            self.t3.set_parameters(omega0 = np.random.rand())
            self.t3.set_parameters(omega1 = np.random.rand())
            self.set_active_module_name(self.child_modules['avoid'].get_active_module_name())


class ExploreModule(SubsumptionModule):
    def on_init(self):
        # カオスバージョンのwander moduleに切替可能
        self.add_child_module('wander', WanderModule())
        #self.add_child_module('wander', ChaosWanderModule())

    def on_update(self):
        if self.get_input('feed_touching'):
            # エサを検知したので下位のモジュールは抑制してスピードダウン
            self.set_output("left_wheel_speed",  0)
            self.set_output("right_wheel_speed", 0)
            self.set_active_module_name(self.__class__.__name__)
        else:
            # エサがない時は下位のモジュールは抑制せずにそのままアウトプットとする
            self.set_output("left_wheel_speed",  self.child_modules['wander'].get_output("left_wheel_speed"))
            self.set_output("right_wheel_speed", self.child_modules['wander'].get_output("right_wheel_speed"))
            self.set_active_module_name(self.child_modules['wander'].get_active_module_name())


######################
# change architecture
######################
controller = AvoidModule()
#controller = WanderModule()
#controller = ChaosWanderModule()  # ワンダーモジュールの内部にカオスを入れる
#controller = ExploreModule()

# simulatorの初期化 (Appendix参照)
simulator = VehicleSimulator(obstacle_num=5, feed_num=40)

while simulator:
    # 現在のセンサー情報を取得
    sensor_data = simulator.get_sensor_data()
    # サブサンプションのコントローラをアップデート
    controller.set_inputs(sensor_data)
    controller.update()

    # アクションを生成してアップデート
    left_wheel_speed  = controller.get_output('left_wheel_speed')
    right_wheel_speed = controller.get_output('right_wheel_speed')
    action = [left_wheel_speed, right_wheel_speed]
    color = (0, 0, 255)
    active_module = controller.get_active_module_name()
    if active_module is "AvoidModule":
        simulator.set_bodycolor((255, 0, 0))
    elif active_module in ("WanderModule", "ChaosWanderModule"):
        simulator.set_bodycolor((0, 255, 0))
    elif active_module in ("ExploreModule", "ChaosExploreModule"):
        simulator.set_bodycolor((0, 0, 255))
    simulator.update(action)
