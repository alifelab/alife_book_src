#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.axes()
ax.set_xticks([])
ax.set_yticks([])
ax.grid(True)

### random ###
# space = np.random.randint(2, size=(100,100), dtype=np.int8)

### glider ###
space = np.zeros((100,100), dtype=np.int8)
space[2:6,2:6] = np.array([[0,0,0,0],
                           [0,0,1,0],
                           [0,0,0,1],
                           [0,1,1,1]])

img = ax.imshow(space, interpolation='nearest', cmap='Greys')

def update(frame):
    global space
    next_space = np.empty(space.shape, dtype=np.int8)
    for i in range(space.shape[0]):
        for j in range(space.shape[1]):
            target_cell_state = space[i,j]
            neighbor_cell_sum = np.sum(space[i-1:i+2, j-1:j+2]) - target_cell_state
            if target_cell_state == 0 and neighbor_cell_sum == 3:
                next_space[i,j] = 1
            elif target_cell_state == 1 and neighbor_cell_sum in (2,3):
                next_space[i,j] = 1
            else:
                next_space[i,j] = 0
    space = next_space
    img.set_array(space)
    return img,

anim = animation.FuncAnimation(fig, update, interval=50, blit=True)
plt.show(anim)
