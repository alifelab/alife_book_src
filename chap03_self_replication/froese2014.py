#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer

# Simulation Parameters
X_SIZE = 256
Y_SIZE = 256
#dx = 0.01
dx = 1
dt = 0.5
visualization_step = 32

# Model Parameters
Da = 0.3
Db = 0.15
k = 0.0942
k_p = 0.0002
w = 0.015
r = 0.032

# Initialization
a = np.ones((X_SIZE, Y_SIZE))
b = np.zeros((X_SIZE, Y_SIZE))
p = np.zeros((X_SIZE, Y_SIZE))

# set initiale square pattern on center
square_size = 10
a[X_SIZE//2-square_size//2:X_SIZE//2+square_size//2, Y_SIZE//2-square_size//2:Y_SIZE//2+square_size//2] = 0
b[X_SIZE//2-square_size//2:X_SIZE//2+square_size//2, Y_SIZE//2-square_size//2:Y_SIZE//2+square_size//2] = 1

a += np.random.rand(X_SIZE, Y_SIZE)*0.1
b += np.random.rand(X_SIZE, Y_SIZE)*0.1
p += np.random.rand(X_SIZE, Y_SIZE)*0.1

visualizer = MatrixVisualizer((600, 600))

while True:
    for i in range(visualization_step):
        # calculate laplacian
        laplacian_a = (np.roll(a, 1, axis=0) + np.roll(a, -1, axis=0) + np.roll(a, 1, axis=1) + np.roll(a, -1, axis=1) - 4*a) / (dx*dx)
        laplacian_b = (np.roll(b, 1, axis=0) + np.roll(b, -1, axis=0) + np.roll(b, 1, axis=1) + np.roll(b, -1, axis=1) - 4*b) / (dx*dx)

        dadt = Da * laplacian_a - np.exp(-w*p)*a*b*b + r*(1.0-a);
        dbdt = Db * laplacian_b + np.exp(-w*p)*a*b*b - k*b;
        dpdt = k*b - k_p*p;

        a += dt * dadt
        b += dt * dbdt
        p += dt * dpdt
    img_matrix = (b + p / 50) * 255
    visualizer.update(img_matrix)
