#!/usr/bin/env python

import matplotlib as mpl
mpl.use('tkagg')

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scl_lib import draw

#
# Settings and Parameters
#
SPACE_SIZE = 16

INIT_CATALYST_POSITIONS = [(SPACE_SIZE//2,SPACE_SIZE//2)]
INIT_BONDED_LINK_POSITIONS = []

# INIT_CATALYST_POSITIONS = [(16,16), (3,3), (29,29), (3, 29), (29, 3)]
# INIT_BONDED_LINK_POSITIONS = [ \
# (14,13),(15,13),(16,13),(17,13),(18,13), \
# (19,14),(19,15),(19,16),(19,17),(19,18), \
# (18,19),(17,19),(16,19),(15,19),(14,19), \
# (13,18),(13,17),(13,16),(13,15),(13,14)]

SUBSTRATE_DENSITY = 0.8
MOBILITY_FACTOR = {
'HOLE':           0.1,
'SUBSTRATE':      0.1,
'CATALYST':       0.0001,
'LINK':           0.05,
'LINK_SUBSTRATE': 0.05,
}
PRODUCTION_PROBABILITY     = 0.95
DISINTEGRATION_PROBABILITY = 0.0005
BONDING_PROBABILITY        = 0.8
CHAIN_INITIATE_PROB        = 0.1
CHAIN_EXTEND_PROB          = 0.6
CHAIN_SPLICE_PROB          = 0.9
BOND_DECAY_PROBABILITY     = 0.0005
ABSORPTION_PROBABILITY     = 0.5
EMISSION_PROBABILITY       = 0.5


#
# Utility Functions
#

# get list of 4 neumann neighborhood
def get_neumann_neighborhood(x, y):
    n = [((x+1)%SPACE_SIZE, y), ((x-1)%SPACE_SIZE, y), (x, (y+1)%SPACE_SIZE), (x, (y-1)%SPACE_SIZE)]
    return n

# get 1 random neumann neighborhood position of (x,y)
def get_rand_neumann_neighborhood(x, y):
    neighborhood = get_neumann_neighborhood(x, y)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

# get list of 8 moore neighborhood
def get_moore_neighborhood(x, y):
    n = [((x-1)%SPACE_SIZE, (y-1)%SPACE_SIZE), (x, (y-1)%SPACE_SIZE), ((x+1)%SPACE_SIZE, (y-1)%SPACE_SIZE), \
         ((x-1)%SPACE_SIZE,  y              ),                        ((x+1)%SPACE_SIZE,  y              ), \
         ((x-1)%SPACE_SIZE, (y+1)%SPACE_SIZE), (x, (y+1)%SPACE_SIZE), ((x+1)%SPACE_SIZE, (y+1)%SPACE_SIZE)]
    return n

# get 1 random moore neighborhood position of (x,y)
def get_rand_moore_neighborhood(x, y):
    neighborhood = get_moore_neighborhood(x, y)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

# get 2 random moore neighborhood which adjacent each other
def get_rand_2_moore_neighborhood(x, y):
    n0_x, n0_y = get_rand_moore_neighborhood(x, y)
    if x == n0_x:
        n1_x = np.random.choice([(n0_x+1)%SPACE_SIZE, (n0_x-1)%SPACE_SIZE])
        n1_y = n0_y
    elif y == n0_y:
        n1_x = n0_y
        n1_y = np.random.choice([(n0_y+1)%SPACE_SIZE, (n0_y-1)%SPACE_SIZE])
    else:
        n= [(x, n0_y), (n0_x, y)]
        n1_x, n1_y = n[np.random.randint(len(n))]
    return n0_x, n0_y, n1_x, n1_y

# get 2 moore neighborhood of (x,y) which adjacent to (n_,n_y)
def get_adjacent_moore_neighborhood(x, y, n_x, n_y):
    if x == n_x:
        n0_x = (n_x-1)%SPACE_SIZE
        n0_y = n_y
        n1_x = (n_x+1)%SPACE_SIZE
        n1_y = n_y
    elif y == n_y:
        n0_x = n_x
        n0_y = (n_y-1)%SPACE_SIZE
        n1_x = n_x
        n1_y = (n_y+1)%SPACE_SIZE
    else:
        n0_x = x
        n0_y = n_y
        n1_x = n_x
        n1_y = y
    return n0_x, n0_y, n1_x, n1_y

def evaluate_probability(probability):
    return np.random.rand() < probability


#
# Initialization
#
fig = plt.figure(figsize=(8,8))
ax = plt.axes(xlim=(-1,SPACE_SIZE), ylim=(-1,SPACE_SIZE), aspect='equal')
ax.set_xticks([])
ax.set_yticks([])
ax.invert_yaxis()

particles = np.empty((SPACE_SIZE, SPACE_SIZE), dtype=object)
for (x, y), _ in np.ndenumerate(particles):
    if evaluate_probability(SUBSTRATE_DENSITY):
    #elif x > 10 and x < 30 and y > 10 and y < 20:
        p = {'type': 'SUBSTRATE', 'disintegrating': False, 'bonds': []}
    else:
        p = {'type': 'HOLE', 'disintegrating': False, 'bonds': []}
    particles[x,y] = p

for i in range(len(INIT_CATALYST_POSITIONS)):
    x, y = INIT_CATALYST_POSITIONS[i]
    particles[x, y]['type'] = 'CATALYST'

for i in range(len(INIT_BONDED_LINK_POSITIONS)):
    x0, y0 = INIT_BONDED_LINK_POSITIONS[i]
    x1, y1 = INIT_BONDED_LINK_POSITIONS[i-1]
    particles[x0, y0]['type'] = 'LINK'
    particles[x0, y0]['bonds'].append((x1, y1))
    particles[x1, y1]['bonds'].append((x0, y0))


#
# Update Functions
#
def production(particles, x, y):
    p = particles[x,y]
    if p['type'] != 'CATALYST':
        return
    n0_x, n0_y, n1_x, n1_y = get_rand_2_moore_neighborhood(x, y)
    n0_p = particles[n0_x, n0_y]
    n1_p = particles[n1_x, n1_y]
    if n0_p['type'] != 'SUBSTRATE' or n1_p['type'] != 'SUBSTRATE':
        return
    if not evaluate_probability(PRODUCTION_PROBABILITY):
        return
    n0_p['type'] = 'HOLE'
    n1_p['type'] = 'LINK'

def disintegration(particles, x, y):
    p = particles[x,y]
    if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(DISINTEGRATION_PROBABILITY):
        p['disintegrating'] = True

    if not p['disintegrating']:
        return
    # forced emission of substrate
    n_x, n_y = get_rand_moore_neighborhood(x, y)
    n_p = particles[n_x, n_y]
    if p['type'] == 'LINK_SUBSTRATE' and n_p['type'] == 'HOLE':
        p['type']   = 'LINK'
        n_p['type'] = 'SUBSTRATE'
    # disintegration
    n_x, n_y = get_rand_moore_neighborhood(x, y)
    n_p = particles[n_x, n_y]
    if p['type'] == 'LINK' and n_p['type'] == 'HOLE':
        # forced decay of bonds connected to the link
        for b in p['bonds']:
            particles[b[0], b[1]]['bonds'].remove((x, y))
        p['bonds'] = []

        p['type']   = 'SUBSTRATE'
        n_p['type'] = 'SUBSTRATE'
        p['disintegrating'] = False

def bonding(particles, x, y):
    p = particles[x,y]
    n_x, n_y = get_rand_moore_neighborhood(x, y)
    n_p = particles[n_x, n_y]
    if not p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    if not n_p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    if (n_x, n_y) in p['bonds']:
        return
    if len(p['bonds']) >= 2 or len(n_p['bonds']) >= 2:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y)
    if (an0_x, an0_y) in p['bonds'] or (an1_x, an1_y) in p['bonds']:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(n_x, n_y, x, y)
    if (an0_x, an0_y) in n_p['bonds'] or (an1_x, an1_y) in n_p['bonds']:
        return

    # Bonding inhibitted when these 2 situations.
    # 1) thera are bondinb particle in moore neighborhood (chainInhibitBond)
    # 2) thera are Catalyst particle in moore neighborhood (catInhibitBond)
    mn_list = get_moore_neighborhood(x, y)
    for x1, y1 in mn_list:
        # if particles[x1,y1]['type'] is 'CATALYST':
        #     return
        for x2, y2 in mn_list:
            if (x2, y2) in particles[x1,y1]['bonds']:
                return
    mn_list = get_moore_neighborhood(n_x, n_y)
    for x1, y1 in mn_list:
        # if particles[x1,y1]['type'] is 'CATALYST':
        #     return
        for x2, y2 in mn_list:
            if (x2, y2) in particles[x1,y1]['bonds']:
                return
    
                
    if len(p['bonds'])==0 and len(n_p['bonds'])==0:
        prob = CHAIN_INITIATE_PROB
    elif len(p['bonds'])==1 and len(n_p['bonds'])==1:
        prob = CHAIN_SPLICE_PROB
    else:
        prob = CHAIN_EXTEND_PROB
    if evaluate_probability(prob):
        p['bonds'].append((n_x, n_y))
        n_p['bonds'].append((x, y))

def bond_decay(particles, x, y):
    p = particles[x,y]
    if not p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    for b in p['bonds']:
        if evaluate_probability(BOND_DECAY_PROBABILITY):
            pass

def absorption(particles, x, y):
    p = particles[x,y]
    n_x, n_y = get_rand_moore_neighborhood(x, y)
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK' or n_p['type'] != 'SUBSTRATE':
        return
    if not evaluate_probability(ABSORPTION_PROBABILITY):
        return
    p['type']   = 'LINK_SUBSTRATE'
    n_p['type'] = 'HOLE'

def emission(particles, x, y):
    p = particles[x,y]
    n_x, n_y = get_rand_moore_neighborhood(x, y)
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK_SUBSTRATE' or n_p['type'] != 'HOLE':
        return
    if not evaluate_probability(EMISSION_PROBABILITY):
        return
    p['type']   = 'LINK'
    n_p['type'] = 'SUBSTRATE'


#
# Update and Visualization
#
def update(frame):
    # update model
    mobile = np.full(particles.shape, True, dtype=bool)
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            p = particles[x,y]

            n_x, n_y = get_rand_neumann_neighborhood(x, y)
            n_p = particles[n_x, n_y]
            mobility_factor = np.sqrt(MOBILITY_FACTOR[p['type']] * MOBILITY_FACTOR[n_p['type']])
            if mobile[x, y] and mobile[n_x, n_y] and evaluate_probability(mobility_factor) and p != np \
                    and len(p['bonds']) == 0 and len(n_p['bonds']) == 0:
                particles[x,y], particles[n_x,n_y] = n_p, p
                mobile[x, y] = mobile[n_x, n_y] = False

    # Reaction
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            production(particles, x, y)
            disintegration(particles, x, y)
            bonding(particles, x, y)
            bond_decay(particles, x, y)
            absorption(particles, x, y)
            emission(particles, x, y)
    draw(ax, particles)
    return ax.patches


anim = animation.FuncAnimation(fig, update, interval = 80, blit=True)
plt.show(anim)
