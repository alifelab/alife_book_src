#!/usr/bin/env python

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import BinaryMatrixVisualizer

field_width = 100
field_height = 100

### random ###
# space = np.random.randint(2, size=(field_height,field_width), dtype=np.int8)

### glider ###
# space = np.zeros((field_height,field_width), dtype=np.int8)
# glider = np.array(
# [[0,0,0,0],
#  [0,0,1,0],
#  [0,0,0,1],
#  [0,1,1,1]])
# space[2:2+glider.shape[0],2:2+glider.shape[1]] = glider

### glider gun ###
space = np.zeros((field_height,field_width), dtype=np.int8)
glider_gun = np.array(
[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
 [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
space[2:2+glider_gun.shape[0],2:2+glider_gun.shape[1]] = glider_gun

visualizer = BinaryMatrixVisualizer((600, 600))

while True:
    next_space = np.empty(space.shape, dtype=np.int8)
    for i in range(space.shape[0]):
        for j in range(space.shape[1]):
            # nw: north west, ne: north east, c: center ...
            nw = space[i-1,j-1]
            n  = space[i-1,j]
            ne = space[i-1,(j+1)%space.shape[1]]
            w  = space[i,j-1]
            c  = space[i,j]
            e  = space[i,(j+1)%space.shape[1]]
            sw = space[(i+1)%space.shape[0],j-1]
            s  = space[(i+1)%space.shape[0],j]
            se = space[(i+1)%space.shape[0],(j+1)%space.shape[1]]
            neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
            if c == 0 and neighbor_cell_sum == 3:
                next_space[i,j] = 1
            elif c == 1 and neighbor_cell_sum in (2,3):
                next_space[i,j] = 1
            else:
                next_space[i,j] = 0
    space = next_space
    visualizer.update(space)
