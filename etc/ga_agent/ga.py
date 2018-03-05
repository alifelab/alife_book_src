import random
import numpy as np
from deap import algorithms, base, creator, tools
from gasimulator import GAPhysicsSimulator


# parameters
GENOTYPE_SIZE=8
N_POPULATION = 100
N_GEN = 100
MUT_PB = 0.2
MUT_GAUS_MU = 0.0
MUT_GAUS_SIGMA = 0.1
MUT_GAUS_IND_PB = 0.05
CX_PB = 0.5

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
    toolbox.register("mutate", tools.mutGaussian, mu=MUT_GAUS_MU, sigma=MUT_GAUS_SIGMA, indpb=MUT_GAUS_IND_PB)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return toolbox


def setup_deap_stats():
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats.register("save", lambda x: print(type(x), x))
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    return stats


def eval_func(individual):
    sim.reset()
    fitness = sim.run_trial(individual, time_sec=10)
    return fitness,

sim = GAPhysicsSimulator(display=False)

def main():
    toolbox = setup_deap_toolbox(eval_func)
    stats = setup_deap_stats()

    pop = toolbox.population(n=N_POPULATION)
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=CX_PB, mutpb=MUT_PB, ngen=N_GEN, stats=stats, verbose=True)
    best_ind = tools.selBest(pop, 1)[0]

    sim.finish()
    print(best_ind)

    return

if __name__ == "__main__":
    main()
