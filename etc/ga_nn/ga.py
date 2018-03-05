#!/usr/bin/env python

import numpy as np
from neural_net import NeuralNet
import matplotlib.pyplot as plt

N = 100  # population size
GENERATEION = 1000  # max iteration size of GA

# parameter of GA
MUTATION_RATE = 0.5
MUTATION_SIGMA = 5.0 # Standard deviation of mutation noise
EARLY_STOPPING_FITTNESS_THRESHOLD = -0.0001
BEST_AGENT_SELECTION_RATE = 0.05  # top 5% agents remain its gene to next generation
CROSSOVER_PARENT_SELECTION_RATE = 0.1  # next 10% high scored agents become parent of children

# setupt of task: XOR binary operation
input_data = [[0,0], [0,1], [1,0], [1,1]]
correct_answer = [0, 1, 1, 0]


def fittness(nn):
    error = []
    for d, c in zip(input_data, correct_answer):
        out = nn.calc(d)[0]
        error.append((out - c)**2)
    return -np.average(error)

# calculate accuracy of the network
def check_accuracy(nn):
    correct_answer_num = 0
    for d, c in zip(input_data, correct_answer):
        out = nn.calc_binary(d)[0]
        if int(out) == c:
            correct_answer_num += 1
    accuracy = correct_answer_num / len(input_data)
    return accuracy


def generate_initial_population(N):
    nn_population = []
    for i in range(N):
        nn = NeuralNet(2,2,1)
        gt = np.random.rand(nn.get_genotype_length())
        nn.set_genotype(gt)
        nn_population.append(nn)
    return np.array(nn_population)


def evaluate_population(nn_population):
    pop_fitness = []
    for nn in nn_population:
        f = fittness(nn)
        pop_fitness.append(f)
    return np.array(pop_fitness)


def generate_next_population(population, fitness):
    # sort population by fitness value
    rank_index = np.argsort(fitness)[::-1]
    population_sort = population[rank_index]

    # take some parameters of NN
    gene_length = population[0].get_genotype_length()
    nn_input_num = population[0].input_num
    nn_hidden_num = population[0].hidden_num
    nn_output_num = population[0].output_num

    # top 5% population make same children
    n1 = int(N * BEST_AGENT_SELECTION_RATE)
    next_population = population[:n1]

    # other population are made by crossover with next 10% high fitness population
    n2 = int(N * CROSSOVER_PARENT_SELECTION_RATE)
    parents = population_sort[n1:n1+n2]
    while len(next_population) < len(population):
        # choice 2 parents and take its gene
        parent1 = np.random.choice(parents)
        gene1 = parent1.get_genotype()[:gene_length//2]  # first half of gene
        parent2 = np.random.choice(parents)
        gene2 = parent2.get_genotype()[gene_length//2:]  # last half of gene
        # make gene of child
        child_gene = np.append(gene1, gene2)
        child = NeuralNet(nn_input_num, nn_hidden_num, nn_output_num)
        child.set_genotype(child_gene)
        # add child on next population
        next_population = np.append(next_population, child)

    # mutation
    for p in next_population:
        if np.random.rand() < MUTATION_RATE:
            gene = p.get_genotype()
            mut_idx = np.random.randint(len(gene))
            gene[mut_idx] += np.random.normal(0, MUTATION_SIGMA)
            p.set_genotype(gene)

    return next_population


# setup all population
nn_population = generate_initial_population(N)

# evolution loop
for i in range(GENERATEION):
    # evaluate all population
    fitness = evaluate_population(nn_population)

    # print best fitness and accuracy value
    best_idx = np.argmax(fitness)  # get the index of best NN on population
    best_nn = nn_population[best_idx]
    best_fitness = fitness[best_idx]
    accuracy = check_accuracy(best_nn)
    print("generation:", i, "fitness:", best_fitness, "accuracy:", accuracy)

    # for debug
    # print(fitness)
    # if i % 1 == 0:
    #     y = np.empty((100, 100))
    #     for i1, x1 in enumerate(np.linspace(0, 1, 100)):
    #         for i2, x2 in enumerate(np.linspace(0, 1, 100)):
    #             y[i1, i2] = best_nn.calc([x1, x2])
    #     plt.figure()
    #     plt.pcolor(y, vmin=0, vmax=1)
    #     plt.colorbar()
    #     plt.savefig("fig/test_{:03}.png".format(i))

    # early stopping by perfect answr and good fittness
    if accuracy >= 1.0 and best_fitness > EARLY_STOPPING_FITTNESS_THRESHOLD:
        break

    # generate next population
    nn_population = generate_next_population(nn_population, fitness)


# evaluate last generation
best_idx = np.argmax(fitness)  # get the index of best NN on population
best_nn = nn_population[best_idx]
best_fitness = fitness[best_idx]
accuracy = check_accuracy(best_nn)
print("final generation", "fitness:", best_fitness, "accuracy:", accuracy)
