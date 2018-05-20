#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer

# visualizerの初期化。表示領域のサイズを与える。
visualizer = MatrixVisualizer(600, 600)

# シミュレーションの各パラメタ
VISUALIZATION_TIME = 256  # size of visualized time duration = visualization height
SPACE_SIZE = 256  # size of 1D space = visualization width
dx = 0.01
dt = 1
visualization_step = 1

# モデルの各パラメタ
Du = 2e-5
Dv = 1e-5
f, k = 0.018, 0.077

# 初期化
u = np.zeros((VISUALIZATION_TIME, SPACE_SIZE))
v = np.zeros((VISUALIZATION_TIME, SPACE_SIZE))
INIT_PATTERN_SIZE = 20
u[0,:] = 1.0
v[0,:] = 0.0
u[0, SPACE_SIZE//2-INIT_PATTERN_SIZE//2:SPACE_SIZE//2+INIT_PATTERN_SIZE//2] = 0.5
v[0, SPACE_SIZE//2-INIT_PATTERN_SIZE//2:SPACE_SIZE//2+INIT_PATTERN_SIZE//2] = 0.25
# 対称性を壊すために、少しノイズを入れる
u[0,:] += np.random.rand(SPACE_SIZE)*0.01
v[0,:] += np.random.rand(SPACE_SIZE)*0.01

t = 0
while visualizer:  # visualizerはウィンドウが閉じられるとFalseを返す
    for i in range(visualization_step):
        current_line = (t * visualization_step + i) % VISUALIZATION_TIME
        next_line = (current_line + 1) % VISUALIZATION_TIME
        current_u = u[current_line]
        current_v = v[current_line]
        # ラプラシアンの計算
        laplacian_u = (np.roll(current_u, 1) + np.roll(current_u, -1) - 2*current_u) / (dx*dx)
        laplacian_v = (np.roll(current_v, 1) + np.roll(current_v, -1) - 2*current_v) / (dx*dx)
        # Gray-Scottモデル方程式
        dudt = Du*laplacian_u - current_u*current_v*current_v + f*(1.0-current_u)
        dvdt = Dv*laplacian_v + current_u*current_v*current_v - (f+k)*current_v
        u[next_line] = current_u + dt * dudt
        v[next_line] = current_v + dt * dvdt
        t += 1
    # 表示をアップデート。uは0-1なので、255階調に変換する。
    visualizer.update(u*256)
