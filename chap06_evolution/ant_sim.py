import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer
from ant_simulator import AntSimulator
import sys

def get_gene_length(model):
    return len(encode_weights(model))


def encode_weights(model):
    w = model.get_weights()
    g = np.concatenate([x.flatten() for x in w])
    return g


def decode_weights(model, gen):
    w_shape = [wi.shape for wi in model.get_weights()]
    w_size = [wi.size for wi in model.get_weights()]

    w = []
    tmp = g
    for shape, size in zip(w_shape, w_size):
        w.append(tmp[:size].reshape(shape))
        tmp = tmp[size:]
    model.set_weights(w)

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
    #print(nn_input)
    nn_input = nn_input.reshape(1, len(nn_input))
    #print(nn_input)
    nn_output = nn_model.predict(nn_input)
    act = np.array([nn_output[0][:2]])
    context_val = nn_output[0][2:]
    return act

sim = AntSimulator(1)

g = np.load(sys.argv[1])
decode_weights(nn_model, g)

obs = sim.reset(int(sys.argv[2]))
while True:
    act = action(obs)
    obs = sim.step(act)
