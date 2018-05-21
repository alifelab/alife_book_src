#
# Utility Functions
#

import numpy as np

# get list of 4 neumann neighborhood
def get_neumann_neighborhood(x, y, space_size):
    n = [((x+1)%space_size, y), ((x-1)%space_size, y), (x, (y+1)%space_size), (x, (y-1)%space_size)]
    return n

# get 1 random neumann neighborhood position of (x,y)
def get_random_neumann_neighborhood(x, y, space_size):
    neighborhood = get_neumann_neighborhood(x, y, space_size)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

# get list of 8 moore neighborhood
def get_moore_neighborhood(x, y, space_size):
    n = [((x-1)%space_size, (y-1)%space_size), (x, (y-1)%space_size), ((x+1)%space_size, (y-1)%space_size), \
         ((x-1)%space_size,  y              ),                        ((x+1)%space_size,  y              ), \
         ((x-1)%space_size, (y+1)%space_size), (x, (y+1)%space_size), ((x+1)%space_size, (y+1)%space_size)]
    return n

# get 1 random moore neighborhood position of (x,y)
def get_random_moore_neighborhood(x, y, space_size):
    neighborhood = get_moore_neighborhood(x, y, space_size)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

# get 2 random moore neighborhood which adjacent each other
def get_random_2_moore_neighborhood(x, y, space_size):
    n0_x, n0_y = get_random_moore_neighborhood(x, y, space_size)
    if x == n0_x:
        n1_x = np.random.choice([(n0_x+1)%space_size, (n0_x-1)%space_size])
        n1_y = n0_y
    elif y == n0_y:
        n1_x = n0_y
        n1_y = np.random.choice([(n0_y+1)%space_size, (n0_y-1)%space_size])
    else:
        n= [(x, n0_y), (n0_x, y)]
        n1_x, n1_y = n[np.random.randint(len(n))]
    return n0_x, n0_y, n1_x, n1_y

# get 2 moore neighborhood of (x,y) which adjacent to (n_,n_y)
def get_adjacent_moore_neighborhood(x, y, n_x, n_y, space_size):
    if x == n_x:
        n0_x = (n_x-1)%space_size
        n0_y = n_y
        n1_x = (n_x+1)%space_size
        n1_y = n_y
    elif y == n_y:
        n0_x = n_x
        n0_y = (n_y-1)%space_size
        n1_x = n_x
        n1_y = (n_y+1)%space_size
    else:
        n0_x = x
        n0_y = n_y
        n1_x = n_x
        n1_y = y
    return n0_x, n0_y, n1_x, n1_y

def evaluate_probability(probability):
    return np.random.rand() < probability
