#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer
import game_of_life_patterns

# visualizerの初期化 (Appendix参照)
visualizer = MatrixVisualizer()

WIDTH = 50
HEIGHT = 50

state = np.zeros((HEIGHT,WIDTH), dtype=np.int8)
next_state = np.empty((HEIGHT,WIDTH), dtype=np.int8)

# 初期化
### ランダム ###
state = np.random.randint(2, size=(HEIGHT,WIDTH), dtype=np.int8)
### game_of_life_patterns.pyの中の各パターンを利用. 左上(2,2)の位置にセットする. ###
# pattern = game_of_life_patterns.OSCILLATOR
# state[2:2+pattern.shape[0], 2:2+pattern.shape[1]] = pattern

while visualizer:  # visualizerはウィンドウが閉じられるとFalseを返す
    for i in range(HEIGHT):
        for j in range(WIDTH):
            # 自分と近傍のセルの状態を取得
            # c: center (自分自身)
            # nw: north west, ne: north east, c: center ...
            nw = state[i-1,j-1]
            n  = state[i-1,j]
            ne = state[i-1,(j+1)%WIDTH]
            w  = state[i,j-1]
            c  = state[i,j]
            e  = state[i,(j+1)%WIDTH]
            sw = state[(i+1)%HEIGHT,j-1]
            s  = state[(i+1)%HEIGHT,j]
            se = state[(i+1)%HEIGHT,(j+1)%WIDTH]
            neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
            if c == 0 and neighbor_cell_sum == 3:
                next_state[i,j] = 1
            elif c == 1 and neighbor_cell_sum in (2,3):
                next_state[i,j] = 1
            else:
                next_state[i,j] = 0
    state, next_state = next_state, state
    # 表示をアップデート
    visualizer.update(1-state) # 1を黒, 0を白で表示する
