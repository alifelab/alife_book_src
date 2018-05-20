#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer

# visualizerの初期化。表示領域のサイズを与える。
visualizer = MatrixVisualizer(600, 600)

WIDTH = 600
HEIGHT = 600

# CAのバイナリコーディングされたルール (Wolfram code)
RULE = 110

# CAの結果
# 列方向は空間、行方向は時間
state = np.zeros((HEIGHT, WIDTH), dtype=np.int8)

# 最初の状態を初期化
### ランダム ###
# state[0,:] = np.random.randint(2, size=len(state))
### 中央の１ピクセルのみ１、後は０ ###
state[0, state.shape[1]//2] = 1

t = 0
while visualizer:  # visualizerはウィンドウが閉じられるとFalseを返す
    # 今と次の行を計算
    current_line = t % state.shape[0]
    next_line = (t+1) % state.shape[0]
    t += 1
    for i in range(state.shape[1]):
        # left, center, right cellの状態を取得
        l = state[current_line, i-1]
        c = state[current_line, i]
        r = state[current_line, (i+1)%state.shape[1]]
        # neighbor_cell_codeは現在の状態のバイナリコーディング
        # ex) 現在が[1 1 0]の場合
        #     neighbor_cell_codeは 1*2^2 + 1*2^1 + 0*2^0 = 6となるので、
        #     RULEの６番目のビットが１ならば、次の状態は１となるので、
        #     RULEをneighbor_cell_code分だけビットシフトして１と論理積をとる。
        neighbor_cell_code = 2**2 * l + 2**1 * c + 2**0 * r
        if (RULE >> neighbor_cell_code) & 1:
            state[next_line, i] = 1
        else:
            state[next_line, i] = 0
    # 表示をアップデート。stateは0/1なので、255階調に変換する。
    visualizer.update(state*255)
