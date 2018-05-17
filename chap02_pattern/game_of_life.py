#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer
import game_of_life_patterns


WIDTH = 50
HEIGHT = 50

state = np.zeros((HEIGHT,WIDTH), dtype=np.int8)

# 初期化
### ランダム ###
# state = np.random.randint(2, size=(HEIGHT,WIDTH), dtype=np.int8)
### game_of_life_patterns.pyの中の各パターンを利用 ###
pattern = game_of_life_patterns.GLIDER_GUN
state[2:2+pattern.shape[0], 2:2+pattern.shape[1]] = pattern

visualizer = MatrixVisualizer((600, 600))

while True:
    # 次の状態を一時的に保存する変数
    next_state = np.empty(state.shape, dtype=np.int8)
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            # 自分と近傍のセルの状態を取得
            # c: center (自分自身)
            # nw: north west, ne: north east, c: center ...
            nw = space[i-1,j-1]
            n  = state[i-1,j]
            ne = state[i-1,(j+1)%state.shape[1]]
            w  = state[i,j-1]
            c  = state[i,j]
            e  = state[i,(j+1)%state.shape[1]]
            sw = state[(i+1)%state.shape[0],j-1]
            s  = state[(i+1)%state.shape[0],j]
            se = state[(i+1)%state.shape[0],(j+1)%state.shape[1]]
            neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
            if c == 0 and neighbor_cell_sum == 3:
                next_state[i,j] = 1
            elif c == 1 and neighbor_cell_sum in (2,3):
                next_state[i,j] = 1
            else:
                next_state[i,j] = 0
    state = next_state
    visualizer.update(state*255)
