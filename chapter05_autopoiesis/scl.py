#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


#
# Settings and Parameters
#
SPACE_SIZE = 32

SUBSTRATE_DENSITY = 0.95

# INIT_CATALYST_POSITIONS = [(16,16)]
# INIT_BONDED_LINK_POSITIONS = []

INIT_CATALYST_POSITIONS = [(16,16), (3,3), (29,29), (3, 29), (29, 3)]
INIT_BONDED_LINK_POSITIONS = [ \
(14,13),(15,13),(16,13),(17,13),(18,13), \
(19,14),(19,15),(19,16),(19,17),(19,18), \
(18,19),(17,19),(16,19),(15,19),(14,19), \
(13,18),(13,17),(13,16),(13,15),(13,14)]

MOBILITY_FACTOR = {
'HOLE':           0.9,
'SUBSTRATE':      0.9,
'CATALYST':       0.05,
'LINK':           0.6,
'LINK_SUBSTRATE': 0.6,
}
PRODUCTION_PROBABILITY     = 0.99
DISINTEGRATION_PROBABILITY = 0.05
BONDING_PROBABILITY        = 0.8
BOND_DECAY_PROBABILITY     = 0.1
ABSORPTION_PROBABILITY     = 0.9
EMISSION_PROBABILITY       = 0.9


#
# Utility Functions
#
particle_shapes = np.empty((SPACE_SIZE, SPACE_SIZE), dtype=object)
def draw_particle(ax, x, y, particle_type):
    if particle_shapes[x, y] is not None:
        if isinstance(particle_shapes[x,y], list):
            particle_shapes[x,y][0].remove()
            particle_shapes[x,y][1].remove()
        else:
            particle_shapes[x, y].remove()

    if particle_type == 'HOLE':
        s = None
    elif particle_type is 'SUBSTRATE':
        s = plt.Circle((x, y), 0.25, facecolor='c')
        ax.add_patch(s)
    elif particle_type is 'CATALYST':
        s = plt.Circle((x, y), 0.4, facecolor='m')
        ax.add_patch(s)
    elif particle_type is 'LINK':
        s = plt.Rectangle([x - 0.35, y - 0.35], 0.7, 0.7, edgecolor='b', facecolor='w')
        ax.add_patch(s)
    elif particle_type is 'LINK_SUBSTRATE':
        s0 = plt.Rectangle([x - 0.35, y - 0.35], 0.7, 0.7, edgecolor='b', facecolor='w')
        ax.add_patch(s0)
        s1 = plt.Circle((x, y), 0.25, facecolor='c')
        ax.add_patch(s1)
        s = [s0, s1]
    particle_shapes[x, y] = s

bond_shapes = {}
def draw_bond(ax, x0, y0, x1, y1):
    #print("draw", x0, y0, x1, y1)
    x0_n = SPACE_SIZE if (x0 == 0 and x1 == SPACE_SIZE-1) else x0
    y0_n = SPACE_SIZE if (y0 == 0 and y1 == SPACE_SIZE-1) else y0
    x1_n = SPACE_SIZE if (x1 == 0 and x0 == SPACE_SIZE-1) else x1
    y1_n = SPACE_SIZE if (y1 == 0 and y0 == SPACE_SIZE-1) else y1

    start_x = x0_n + 0.35 * (x1_n - x0_n)
    start_y = y0_n + 0.35 * (y1_n - y0_n)
    end_x = x1_n - 0.35 * (x1_n - x0_n)
    end_y = y1_n - 0.35 * (y1_n - y0_n)
    line = plt.Polygon([(start_x, start_y), (end_x, end_y)], color='b', lw=1.5)
    ax.add_patch(line)
    bond_shapes[(x0, y0, x1, y1)] = line

def clear_bond(ax, x0, y0, x1, y1):
    #print("clear", x0, y0, x1, y1)
    try:
        key = (x0, y0, x1, y1)
        if key in bond_shapes:
            bond_shapes[key].remove()
            bond_shapes.pop(key)
        else:
            key = (x1, y1, x0, y0)
            bond_shapes[key].remove()
            bond_shapes.pop(key)
    except KeyError:
        print(x0,y0,x1,y1)
        print(bond_shapes.keys())
        exit()

def get_rand_neumann_neighborhood(x, y):
    neighborhood = [((x+1)%SPACE_SIZE, y), ((x-1)%SPACE_SIZE, y), \
                    (x, (y+1)%SPACE_SIZE), (x, (y-1)%SPACE_SIZE)]
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

def get_rand_moore_neighborhood(x, y):
    import itertools
    neighborhood = list(itertools.product([(x-1)%SPACE_SIZE, x, (x+1)%SPACE_SIZE],
                                          [(y-1)%SPACE_SIZE, y, (y+1)%SPACE_SIZE]))
    neighborhood.remove((x,y))
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

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
#ax.set_aspect('equal', 'box')
#ax.set_aspect('equal')
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
    draw_particle(ax, x, y, p['type'])

for i in range(len(INIT_CATALYST_POSITIONS)):
    x, y = INIT_CATALYST_POSITIONS[i]
    particles[x, y]['type'] = 'CATALYST'
    draw_particle(ax, x, y, particles[x,y]['type'])

for i in range(len(INIT_BONDED_LINK_POSITIONS)):
    x0, y0 = INIT_BONDED_LINK_POSITIONS[i]
    x1, y1 = INIT_BONDED_LINK_POSITIONS[i-1]
    particles[x0, y0]['type'] = 'LINK'
    draw_particle(ax, x0, y0, particles[x0,y0]['type'])
    particles[x0, y0]['bonds'].append((x1, y1))
    particles[x1, y1]['bonds'].append((x0, y0))
    draw_bond(ax, x0, y0, x1, y1)


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
    draw_particle(ax, n0_x, n0_y, n0_p['type'])
    draw_particle(ax, n1_x, n1_y, n1_p['type'])

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
        draw_particle(ax, x,   y,   p['type'])
        draw_particle(ax, n_x, n_y, n_p['type'])
    # disintegration
    n_x, n_y = get_rand_moore_neighborhood(x, y)
    n_p = particles[n_x, n_y]
    if p['type'] == 'LINK' and n_p['type'] == 'HOLE':
        # forced decay of bonds connected to the link
        for b in p['bonds']:
            particles[b[0], b[1]]['bonds'].remove((x, y))
            clear_bond(ax, x, y, b[0], b[1])
        p['bonds'] = []

        p['type']   = 'SUBSTRATE'
        n_p['type'] = 'SUBSTRATE'
        p['disintegrating'] = False
        draw_particle(ax, x,   y,   p['type'])
        draw_particle(ax, n_x, n_y, n_p['type'])

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
    if not evaluate_probability(BONDING_PROBABILITY):
        return
    p['bonds'].append((n_x, n_y))
    n_p['bonds'].append((x, y))
    draw_bond(ax, x, y, n_x, n_y)

def bond_decay(particles, x, y):
    if not p['type'] in ('LINK', 'LINK_SUBSTRATE'):
        return
    p = particles[x,y]
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
    draw_particle(ax, x,   y,   p['type'])
    draw_particle(ax, n_x, n_y, n_p['type'])

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
    draw_particle(ax, x,   y,   p['type'])
    draw_particle(ax, n_x, n_y, n_p['type'])


#
# Update and Visualization
#

# debug code
# N_s = 0
# N_c = 0
# for x in range(SPACE_SIZE):
#     for y in range(SPACE_SIZE):
#         p = particles[x,y]
#         if p['type'] == 'CATALYST':
#             N_c += 1
#         elif p['type'] == 'SUBSTRATE':
#             N_s += 1
#         elif p['type'] == 'LINK':
#             N_s += 2
#         elif p['type'] == 'LINK_SUBSTRATE':
#             N_s += 3
# print("catalyst:{}, substrate:{}".format(N_c, N_s))

def update(frame):
    # debug code
    # n_s = 0
    # n_c = 0
    # for x in range(SPACE_SIZE):
    #     for y in range(SPACE_SIZE):
    #         p = particles[x,y]
    #         if p['type'] == 'CATALYST':
    #             n_c += 1
    #         elif p['type'] == 'SUBSTRATE':
    #             n_s += 1
    #         elif p['type'] == 'LINK':
    #             n_s += 2
    #         elif p['type'] == 'LINK_SUBSTRATE':
    #             n_s += 3
    # if N_s != n_s or N_c != n_c:
    #     print("# Error!! Total count of particle is changed!! {},{}".format(n_c, n_s))

    # update model
    mobile = np.full(particles.shape, True)
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            p = particles[x,y]

            n_x, n_y = get_rand_neumann_neighborhood(x, y)
            n_p = particles[n_x, n_y]
            mobility_factor = np.sqrt(MOBILITY_FACTOR[p['type']] * MOBILITY_FACTOR[n_p['type']])
            if mobile[x, y] and mobile[n_x, n_y] and evaluate_probability(mobility_factor) and p != np \
                    and len(p['bonds']) == 0 and len(n_p['bonds']) == 0:
                particles[x,y], particles[n_x,n_y] = n_p, p
                draw_particle(ax, x,   y,   n_p['type'])
                draw_particle(ax, n_x, n_y, p['type'])
                mobile[x, y] = mobile[n_x, n_y] = False

    # Reaction
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            production(particles, x, y)
            disintegration(particles, x, y)
            bonding(particles, x, y)
            #bond_decay(particles, x, y)
            absorption(particles, x, y)
            emission(particles, x, y)
    return ax.patches


anim = animation.FuncAnimation(fig, update, interval = 200, blit=True)
plt.show(anim)
