import random
import numpy as np
from deap import algorithms, base, creator, tools

GENOTYPE_SIZE=3
N_GEN = 100
N_GEN_SAVE = 10
CX_PB = 0.5
MUT_PB = 0.2
MUT_GAUS_MU = 0.0
MUT_GAUS_SIGMA = 0.1
MUT_GAUS_IND_PB = 0.05

def setup_deap_toolbox(eval_func, seed = 0):
    random.seed(seed)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=GENOTYPE_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", eval_func)
    toolbox.register("mate", tools.cxTwoPoint)
    #toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("mutate", tools.mutGaussian, mu=MUT_GAUS_MU, sigma=MUT_GAUS_SIGMA, indpb=MUT_GAUS_IND_PB)
    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox

def setup_deap_stats():
    #stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats = tools.Statistics()
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    return stats

def evalOneMax(individual):
    #return -abs(sum(individual)),
    return sum(individual),

def main():
    toolbox = setup_deap_toolbox(evalOneMax)
    stats = setup_deap_stats()

    pop = toolbox.population(n=300)
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=N_GEN, stats=stats, verbose=True)
    best_ind = tools.selBest(pop, 1)[0]

    print(best_ind)

    return

if __name__ == "__main__":
    main()
