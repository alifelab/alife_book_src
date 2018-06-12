#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.simulators import AntSimulator
from ant_nn_utils import generate_nn_model, generate_action, decode_weights, CONTEXT_NEURON_NUM, get_gene_length

nn_model = generate_nn_model()
# アウトプットの一部をコンテキストニューロンとして次回のインプットに回すための変数
context_val = np.zeros(CONTEXT_NEURON_NUM)

if len(sys.argv) == 1:
    gene = np.random.rand(get_gene_length(nn_model))
else:
    gene = np.load(sys.argv[1])
decode_weights(nn_model, gene)

# 引数はエージェントの数（Appendix参照）
simulator = AntSimulator(1)
simulator.reset()
while True:
    sensor_datas = simulator.get_sensor_data()
    action, context_val = generate_action(nn_model, sensor_datas[0], context_val)
    simulator.update(action)
