import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer
from ant_simulator import AntSimulator
from nn_ga_utils import *
import sys


CONTEXT_NN_NUM = 2

def gen_action_func(gene):
    nn_model = Sequential()
    nn_model.add(InputLayer((7+CONTEXT_NN_NUM,)))
    nn_model.add(Dense(4, activation='sigmoid'))
    nn_model.add(Dense(2+CONTEXT_NN_NUM, activation='sigmoid'))
    decode_weights(nn_model, gene)
    context_val_list = [np.zeros(CONTEXT_NN_NUM)]

    def action(observation):
        o = observation
        nn_input = np.r_[o, context_val_list[0]]
        nn_input = nn_input.reshape(1, len(nn_input))
        nn_output = nn_model.predict(nn_input)
        act = np.array([nn_output[0][:2]])
        context_val_list[0] = nn_output[0][2:]
        return act

    return action


# generage gradation color by value(0-1)
# ex) 0.0 -> red, 0.5 -> green, 1.0 -> blue
def gen_gradation_color(x):
    r = max(-2.0 * x + 1.0, 0.0)
    g = min(2.0 * x, -2.0 * x + 2.0)
    b = max(2.0 * x - 1.0, 0.0)
    return (r, g, b)


# setup agent action function by commandline argments
agent_action_funcs = []
agent_num = []
for i in range(1, len(sys.argv), 2):
    g = np.load(sys.argv[i])
    n = int(sys.argv[i+1])
    agent_num.append(n)
    for j in range(n):
        agent_action_funcs.append(gen_action_func(g))


N = np.sum(agent_num)
sim = AntSimulator(N)

# set agent color depends on gene
idx = 0
if len(agent_num) > 1:
    for i, n in enumerate(agent_num):
        x = i / (len(agent_num) - 1)
        c = gen_gradation_color(x)
        for j in range(n):
            sim.set_agent_color(idx, c)
            idx += 1

obs = sim.reset()
while True:
    act = np.concatenate([af(o) for af, o in zip(agent_action_funcs, obs)])
    obs = sim.step(act)
