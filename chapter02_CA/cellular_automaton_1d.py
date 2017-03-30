#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.axes()
ax.set_xticks([])
ax.set_yticks([])
ax.grid(True)

RULE = 110

space = np.zeros((300,300), dtype=np.int8)
### random ###
# space[0,:] = np.random.randint(2, size=len(space))
### dot ###
space[0, space.shape[1]//2] = 1

img = ax.imshow(space, interpolation='nearest', cmap='Greys')

def update(frame):
    global space
    for i in range(space.shape[1]):
        l = space[frame % space.shape[0], i-1]
        c = space[frame % space.shape[0], i]
        r = space[frame % space.shape[0], (i+1)%space.shape[1]]
        neighbor_cell_code = 2**2 * l + 2**1 * c + 2**0 * r
        if (RULE >> neighbor_cell_code) & 1:
            space[(frame+1) % space.shape[0], i] = 1
        else:
            space[(frame+1) % space.shape[0], i] = 0

    img.set_array(space)
    return img,

anim = animation.FuncAnimation(fig, update, interval=50, blit=True)
plt.show(anim)
