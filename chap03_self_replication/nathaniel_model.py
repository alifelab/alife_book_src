#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer

# visualizerの初期化。表示領域のサイズを与える。
WINDOW_RESOLUTION_W = 600
WINDOW_RESOLUTION_H = 600
visualizer = MatrixVisualizer((WINDOW_RESOLUTION_W, WINDOW_RESOLUTION_H))

# Simulation Parameters
X_SIZE = 200
Y_SIZE = 200
dx = 0.01
dt = 1
visualization_step = 16

# Model Parameters
Da = 2e-5
Db = 1e-5
Dc = 1e-6

# original parameter on article
# r = 0.0347
# k_1 = 0.2
# k_2 = 0.8
# k_3 = 0.005

r = 0.0347
k_1 = 0.1
k_2 = 0.7
k_3 = 0.003

# parameter a_res start from 1.02 and decay to 1.0 in 2000 time unit
# this is trick to make good patern by Nathaniel's thesis pp104
a_res = 1.02
a_res_end = 1.0
a_res_step = (a_res - a_res_end) * dt / 2000

# Initialization
# this initial setup is by Nathaniel's thesis pp104
# 10x10 square A and B concentrated area and 7x7 C area
a = np.ones((X_SIZE, Y_SIZE))
b = np.zeros((X_SIZE, Y_SIZE))
c = np.zeros((X_SIZE, Y_SIZE))

square_size_real = 0.1
a[100:110,100:110] = 0.45 + np.random.rand(10, 10)*0.1
b[100:110,100:110] = 0.45 + np.random.rand(10, 10)*0.1
c[101:108,112:119] = 1.5

while True:
    for i in range(visualization_step):
        laplacian_a = (np.roll(a, 1, axis=0) + np.roll(a, -1, axis=0) + np.roll(a, 1, axis=1) + np.roll(a, -1, axis=1) - 4*a) / (dx*dx)
        laplacian_b = (np.roll(b, 1, axis=0) + np.roll(b, -1, axis=0) + np.roll(b, 1, axis=1) + np.roll(b, -1, axis=1) - 4*b) / (dx*dx)
        laplacian_c = (np.roll(c, 1, axis=0) + np.roll(c, -1, axis=0) + np.roll(c, 1, axis=1) + np.roll(c, -1, axis=1) - 4*c) / (dx*dx)

        dadt = Da * laplacian_a - a*b*b + r*(a_res - a)
        dbdt = Db * laplacian_b + a*b*b - k_2*b*c*c - k_1*b
        dcdt = Dc * laplacian_c + k_2*b*c*c - k_3*c

        a += dt * dadt
        b += dt * dbdt
        c += dt * dcdt

        # decay of a_res
        if a_res > a_res_end:
            a_res -= a_res_step
        else:
            a_res = a_res_end
    visualizer.update((b+c)*255)
