import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer
from ant_simulator import AntSimulator
from nn_ga_utils import *
import sys


CONTEXT_NN_NUM = 2

# action function for agent NN
def action(nn_model, observation, prev_context_val):
    nn_input = np.r_[observation, prev_context_val]
    nn_input = nn_input.reshape(1, len(nn_input))
    nn_output = nn_model.predict(nn_input)
    act = np.array([nn_output[0][:2]])
    context_val = nn_output[0][2:]
    return act, context_val


# function to generate NN model and initial context values from gene
def gen_nn_model(gene):
    nn_model = Sequential()
    nn_model.add(InputLayer((7+CONTEXT_NN_NUM,)))
    nn_model.add(Dense(4, activation='sigmoid'))
    nn_model.add(Dense(2+CONTEXT_NN_NUM, activation='sigmoid'))
    decode_weights(nn_model, gene)
    context_val = np.zeros(CONTEXT_NN_NUM)
    return nn_model, context_val


# generage gradation color by value(0-1)
# ex) 0.0 -> red, 0.5 -> green, 1.0 -> blue
def gen_gradation_color(x):
    r = max(-2.0 * x + 1.0, 0.0)
    g = min(2.0 * x, -2.0 * x + 2.0)
    b = max(2.0 * x - 1.0, 0.0)
    return (r, g, b)


# setup agents NN models and initial context values by commandline argments
agent_num = []
agent_nn_model_list = []
agent_nn_context_val_list = []

for i in range(1, len(sys.argv), 2):
    g = np.load(sys.argv[i])
    n = int(sys.argv[i+1])
    agent_num.append(n)
    for j in range(n):
        m, c = gen_nn_model(g)
        agent_nn_model_list.append(m)
        agent_nn_context_val_list.append(c)


N = np.sum(agent_num)
sim = AntSimulator(N, decay_rate=0.999, secretion=True)

# set agent color depends on gene
idx = 0
if len(agent_num) > 1:
    for i, n in enumerate(agent_num):
        x = i / (len(agent_num) - 1)
        c = gen_gradation_color(x)
        for j in range(n):
            sim.set_agent_color(idx, c)
            idx += 1

act = np.empty((N, 2))  # empty matrix (Nx2) to contain action vectors
obs = sim.reset()
while True:
    for i in range(N):
        a, c = action(agent_nn_model_list[i], obs[i], agent_nn_context_val_list[i])
        act[i] = a
        agent_nn_context_val_list[i] = c
    obs = sim.step(act)
