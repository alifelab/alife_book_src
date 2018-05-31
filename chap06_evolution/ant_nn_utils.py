import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer


def generate_nn_model(hidden_neuron_num, context_neuron_num):
    nn_model = Sequential()
    nn_model.add(InputLayer((7+context_neuron_num,)))
    nn_model.add(Dense(hidden_neuron_num, activation='sigmoid'))
    nn_model.add(Dense(2+context_neuron_num, activation='sigmoid'))
    return nn_model


def generate_action(nn_model, sensor_data, context_val):
    nn_input = np.r_[sensor_data, context_val]
    nn_input = nn_input.reshape(1, len(nn_input))
    nn_output = nn_model.predict(nn_input)
    action = np.array([nn_output[0][:2]])
    context_val = nn_output[0][2:]
    return action, context_val


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
    tmp = gen
    for shape, size in zip(w_shape, w_size):
        w.append(tmp[:size].reshape(shape))
        tmp = tmp[size:]
    model.set_weights(w)
