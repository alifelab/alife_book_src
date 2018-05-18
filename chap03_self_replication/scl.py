#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import SCLVisualizer
from scl_interaction_functions import *

# visualizerの初期化。表示領域のサイズを与える。
WINDOW_RESOLUTION_W = 600
WINDOW_RESOLUTION_H = 600
visualizer = SCLVisualizer((WINDOW_RESOLUTION_W, WINDOW_RESOLUTION_H))

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
#BONDING_PROBABILITY        = 0.8
BONDING_CHAIN_INITIATE_PROB        = 0.1
BONDING_CHAIN_EXTEND_PROB          = 0.6
BONDING_CHAIN_SPLICE_PROB          = 0.9
BOND_DECAY_PROBABILITY     = 0.0005
ABSORPTION_PROBABILITY     = 0.5
EMISSION_PROBABILITY       = 0.5

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

while True:
    # Mobile
    mobile = np.full(particles.shape, True, dtype=bool)
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            p = particles[x,y]

            n_x, n_y = get_rand_neumann_neighborhood(x, y, SPACE_SIZE)
            n_p = particles[n_x, n_y]
            mobility_factor = np.sqrt(MOBILITY_FACTOR[p['type']] * MOBILITY_FACTOR[n_p['type']])
            if mobile[x, y] and mobile[n_x, n_y] and evaluate_probability(mobility_factor) and p != np \
                    and len(p['bonds']) == 0 and len(n_p['bonds']) == 0:
                particles[x,y], particles[n_x,n_y] = n_p, p
                mobile[x, y] = mobile[n_x, n_y] = False
    # Reaction
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            production(particles, x, y, PRODUCTION_PROBABILITY)
            disintegration(particles, x, y, DISINTEGRATION_PROBABILITY)
            bonding(particles, x, y, BONDING_CHAIN_INITIATE_PROB,
                                     BONDING_CHAIN_SPLICE_PROB,
                                     BONDING_CHAIN_EXTEND_PROB)
            bond_decay(particles, x, y, BOND_DECAY_PROBABILITY)
            absorption(particles, x, y, ABSORPTION_PROBABILITY)
            emission(particles, x, y, EMISSION_PROBABILITY)
    visualizer.update(particles)
