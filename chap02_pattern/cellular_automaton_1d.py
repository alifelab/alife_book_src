#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import BinaryMatrixVisualizer

WIDTH = 600
HEIGHT = 400

# RULE is binary coding of CA rule (Wolfram code).
RULE = 110

# space is all field of CA
# space.shape[0] is number of row(=height) of image(=displayed time duration)
# space.shape[1] is number of col(=width) of image(=field size of CA)
space = np.zeros((HEIGHT, WIDTH), dtype=np.int8)

# Initialization
### random ###
# space[0,:] = np.random.randint(2, size=len(space))
### one pixel ###
space[0, space.shape[1]//2] = 1

visualizer = BinaryMatrixVisualizer((WIDTH, HEIGHT))

t = 0
while True:
    current_line = t % space.shape[0]
    next_line = (t+1) % space.shape[0]
    t += 1
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
    visualizer.update(space)
