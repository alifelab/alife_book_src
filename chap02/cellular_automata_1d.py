#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import ArrayVisualizer

# visualizerの初期化 (Appendix参照)
visualizer = ArrayVisualizer()

SPACE_SIZE = 600

# CAのバイナリコーディングされたルール (Wolfram code)
RULE = 30

# CAの状態空間
state = np.zeros(SPACE_SIZE, dtype=np.int8)
next_state = np.empty(SPACE_SIZE, dtype=np.int8)

# 最初の状態を初期化
### ランダム ###
# state[:] = np.random.randint(2, size=len(state))
### 中央の１ピクセルのみ１、後は０ ###
state[len(state)//2] = 1

while visualizer:  # visualizerはウィンドウが閉じられるとFalseを返す
    # stateから計算した次の結果をnext_stateに保存
    for i in range(SPACE_SIZE):
        # left, center, right cellの状態を取得
        l = state[i-1]
        c = state[i]
        r = state[(i+1)%SPACE_SIZE]
        # neighbor_cell_codeは現在の状態のバイナリコーディング
        # ex) 現在が[1 1 0]の場合
        #     neighbor_cell_codeは 1*2^2 + 1*2^1 + 0*2^0 = 6となるので、
        #     RULEの６番目のビットが１ならば、次の状態は１となるので、
        #     RULEをneighbor_cell_code分だけビットシフトして１と論理積をとる。
        neighbor_cell_code = 2**2 * l + 2**1 * c + 2**0 * r
        if (RULE >> neighbor_cell_code) & 1:
            next_state[i] = 1
        else:
            next_state[i] = 0
    # 最後に入れ替え
    state, next_state = next_state, state
    # 表示をアップデート
    visualizer.update(1-state)
