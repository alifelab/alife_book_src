#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.simulators import AntSimulator
from ant_nn_utils import generate_nn_model, generate_action, decode_weights, CONTEXT_NEURON_NUM

agent_num = []
agent_nn_model_list = []
agent_nn_context_val_list = []

for i in range(1, len(sys.argv), 2):
    gene = np.load(sys.argv[i])
    num = int(sys.argv[i+1])
    agent_num.append(num)
    for j in range(num):
        nn_model = generate_nn_model()
        decode_weights(nn_model, gene)
        context_val = np.zeros(CONTEXT_NEURON_NUM)
        agent_nn_model_list.append(nn_model)
        agent_nn_context_val_list.append(context_val)

N = np.sum(agent_num)
action = np.empty((N, 2)) # 各エージェントのアクションを収めるための (Nx2) の配列

simulator = AntSimulator(N, decay_rate=0.995, hormone_secretion=0.15)

# エージェントの遺伝子ファイル毎に色をセットする
idx = 0
if len(agent_num) > 1:
    for i, n in enumerate(agent_num):
        # xには0-1の間の等間隔の値が入る
        x = i / (len(agent_num) - 1)
        # xに応じてグラデーション色を生成
        r = max(-2.0 * x + 1.0, 0.0)
        g = min(2.0 * x, -2.0 * x + 2.0)
        b = max(2.0 * x - 1.0, 0.0)
        color = (r, g, b)
        for j in range(n):
            simulator.set_agent_color(idx, color)
            idx += 1

while simulator:
    sensor_data = simulator.get_sensor_data()
    for i in range(N):
        a, c = generate_action(agent_nn_model_list[i], sensor_data[i], agent_nn_context_val_list[i])
        action[i] = a
        agent_nn_context_val_list[i] = c
    simulator.update(action)
