#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer
from alifebook_lib.simulators import AntSimulator
from alifebook_lib.utils.nn_ga_utils import decode_weights

def get_gene_length(model):
    return len(encode_weights(model))


def encode_weights(model):
    w = model.get_weights()
    g = np.concatenate([x.flatten() for x in w])
    return g


# GA and trial parameters
ONE_TRIAL_STEP = 5000
POPULATION_SIZE = 50
TOURNAMENT_SIZE = 5

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


gene_length = get_gene_length(nn_model)
population = np.random.random((POPULATION_SIZE, gene_length)) * 10 - 5
offsprings = np.empty(population.shape)

sim = AntSimulator(1)
generation = 0
while True:
    fitness = []

    # evaluate population
    for g in population:
        print('.', end='', flush=True)
        # decode gene and set weights on NN
        decode_weights(nn_model, g)

        #print(nn_model.predict(np.array([[0]*7])))

        # start trial
        obs = sim.reset()
        for i in range(ONE_TRIAL_STEP):
            act = action(obs)
            obs = sim.step(act)

        # get fitness of this trial
        fitness.append(sim.get_fitness()[0])

    # report and save best population
    print()
    print("generation:", generation)
    print("fitness mean:", np.mean(fitness))
    print("         std:", np.std(fitness))
    print("         max:", np.max(fitness))
    print("         min:", np.min(fitness))
    idx = np.argmax(fitness)
    best_individual = population[idx]
    np.save("gen{0:04}_best.npy".format(generation), best_individual)


    np.random.seed()

    # selection
    PARENT_NUM = POPULATION_SIZE // 2
    parents = []
    for i in range(PARENT_NUM):
        idxs = np.random.randint(0, len(population), TOURNAMENT_SIZE)
        fits = np.array(fitness)[idxs]
        winner_idx = idxs[np.argmax(fits)]
        parents.append(population[winner_idx])

    # best population alive next gen
    offsprings[0] = best_individual

    # same as parents N/3
    for i in range(1, POPULATION_SIZE//3):
        offspring_idx = np.random.randint(0, PARENT_NUM)
        offspring = parents[offspring_idx]
        offsprings[i] = offspring


    # mutation N/3
    for i in range(POPULATION_SIZE//3, 2*POPULATION_SIZE//3):
        offspring_idx = np.random.randint(0, PARENT_NUM)
        offspring = parents[offspring_idx]
        mut_idx = np.random.randint(0, gene_length)
        offspring[mut_idx] += np.random.randn()
        offsprings[i] = offspring


    # crossover N/3
    for i in range(2*POPULATION_SIZE//3, POPULATION_SIZE):
        idx1 = np.random.randint(0, PARENT_NUM)
        p1 = parents[idx1]
        idx2 = np.random.randint(0, PARENT_NUM)
        p2 = parents[idx2]
        xo_idx = np.random.randint(1, gene_length)
        offspring = np.r_[p1[:xo_idx], p2[xo_idx:]]
        offsprings[i] = offspring

    population = offsprings.copy()

    generation += 1
