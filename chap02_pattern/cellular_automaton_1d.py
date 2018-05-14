#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from alifebook_lib.visualizer import BinaryMatrixVisualizer

fig = plt.figure()
ax = plt.axes()
ax.set_xticks([])
ax.set_yticks([])
ax.grid(True)

# RULE is binary coding of CA rule (Wolfram code).
# https://en.wikipedia.org/wiki/Wolfram_code
# https://goo.gl/VpyH4k
RULE = 110

# space is all field of CA
# space.shape[0] is number of row(=height) of image(=displayed time duration)
# space.shape[1] is number of col(=width) of image(=field size of CA)
space = np.zeros((300,300), dtype=np.int8)

visualizer = BinaryMatrixVisualizer(space)
while True:
    space[0,0] += 1
    visualizer.update()

# Initialization
### random ###
# space[0,:] = np.random.randint(2, size=len(space))
### one pixel ###
space[0, space.shape[1]//2] = 1

img = ax.imshow(space, interpolation='nearest', cmap='Greys')

# update function of animation.
# frame is integer and incremented every frame, 0,1,2...
def update(frame):
    global space
    current_line = frame % space.shape[0]
    next_line = (frame+1) % space.shape[0]
    for i in range(space.shape[1]):  # size of 1-D CA size = image width
        # current state of left, center and right cell
        l = space[current_line, i-1]
        c = space[current_line, i]
        r = space[current_line, (i+1)%space.shape[1]]
        # neighbor_cell_code is binary coding of current state.
        # ex) when current state is [1 1 0],
        #     neighbor_cell_code = 1*2^2 + 1*2^1 + 0*2^0 = 6
        #     if 6th bit of RULE is 1, then next state is 1. otherwith 0.
        neighbor_cell_code = 2**2 * l + 2**1 * c + 2**0 * r
        # check neighbor_cell_code-th bit by taking and with 1.
        if (RULE >> neighbor_cell_code) & 1:
            space[next_line, i] = 1
        else:
            space[next_line, i] = 0

    img.set_array(space)
    return img,

anim = animation.FuncAnimation(fig, update, interval=50, blit=True)
plt.show(anim)
