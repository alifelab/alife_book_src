#!/usr/bin/env python

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer
import game_of_life_patterns


WIDTH = 50
HEIGHT = 50

space = np.zeros((HEIGHT,WIDTH), dtype=np.int8)

# 初期化
### ランダム ###
space = np.random.randint(2, size=(HEIGHT,WIDTH), dtype=np.int8)
### game_of_life_patterns.pyの中の各パターンを利用 ###
# pattern = game_of_life_patterns.GLIDER
# space[2:2+pattern.shape[0], 2:2+pattern.shape[1]] = pattern

visualizer = MatrixVisualizer((600, 600))

while True:
    next_space = np.empty(space.shape, dtype=np.int8)
    for i in range(space.shape[0]):
        for j in range(space.shape[1]):
            # 自分と近傍のセルの状態を取得
            # c: center (自分自身)
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
    visualizer.update(space*255)
