#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer
from alifebook_lib.simulators import AntSimulator
from alifebook_lib.utils.nn_ga_utils import *


CONTEXT_NN_NUM = 2

nn_model = Sequential()
nn_model.add(InputLayer((7+CONTEXT_NN_NUM,)))
nn_model.add(Dense(4, activation='sigmoid'))
nn_model.add(Dense(2+CONTEXT_NN_NUM, activation='sigmoid'))
context_val = np.zeros(CONTEXT_NN_NUM)

def action(observation):
    global context_val
    o = observation[0]  # in this script, agent num = 1
    nn_input = np.r_[o, context_val]
    nn_input = nn_input.reshape(1, len(nn_input))
    nn_output = nn_model.predict(nn_input)
    act = np.array([nn_output[0][:2]])
    context_val = nn_output[0][2:]
    return act

g = np.load(sys.argv[1])
decode_weights(nn_model, g)

sim = AntSimulator(1)
obs = sim.reset()
#obs = sim.reset(int(sys.argv[2]))
while True:
    act = action(obs)
    obs = sim.step(act)
