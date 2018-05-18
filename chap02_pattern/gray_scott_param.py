#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer


# シミュレーションの各パラメタ
SPACE_GRID_SIZE = 256
dx = 0.01
dt = 1
VISUALIZATION_STEP = 8  # 何ステップごとに画面を更新するか。

# モデルの各パラメタ
Du = 2e-5
Dv = 1e-5
f_min = 0.01
f_max = 0.05
k_min = 0.05
k_max = 0.07

visualizer = MatrixVisualizer((600, 600))

f_lin = np.linspace(f_min, f_max, SPACE_GRID_SIZE)
k_lin = np.linspace(k_min, k_max, SPACE_GRID_SIZE)
f, k = np.meshgrid(f_lin, k_lin)

# Initialization
u = np.ones((SPACE_GRID_SIZE, SPACE_GRID_SIZE))
v = np.zeros((SPACE_GRID_SIZE, SPACE_GRID_SIZE))
# set initiale square pattern on center
SQUARE_SIZE = 20
u[SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE//2,
  SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE//2] = 0.5
v[SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE//2,
  SPACE_GRID_SIZE//2-SQUARE_SIZE//2:SPACE_GRID_SIZE//2+SQUARE_SIZE//2] = 0.25
# add random noize in order to break the square symmetry
u = u + u*np.random.rand(SPACE_GRID_SIZE, SPACE_GRID_SIZE)*0.01
v = v + u*np.random.rand(SPACE_GRID_SIZE, SPACE_GRID_SIZE)*0.01

while True:
    for i in range(VISUALIZATION_STEP):
        # ラプラシアンの計算
        # periodic boundary condition is not suitable for parameter space.
        # so we extend u,v matrix with same value of edge and calculate laplacian.
        u_pad = np.pad(u, 1, 'edge')
        v_pad = np.pad(v, 1, 'edge')
        laplacian_u = (np.roll(u_pad, 1, axis=0) + np.roll(u_pad, -1, axis=0) +
                       np.roll(u_pad, 1, axis=1) + np.roll(u_pad, -1, axis=1) - 4*u_pad) / (dx*dx)
        laplacian_v = (np.roll(v_pad, 1, axis=0) + np.roll(v_pad, -1, axis=0) +
                       np.roll(v_pad, 1, axis=1) + np.roll(v_pad, -1, axis=1) - 4*v_pad) / (dx*dx)
        # next, remove edge value that extended before.
        laplacian_u = laplacian_u[1:-1,1:-1]
        laplacian_v = laplacian_v[1:-1,1:-1]
        # Gray-Scott model equation
        dudt = Du*laplacian_u - u*v*v + f*(1.0-u)
        dvdt = Dv*laplacian_v + u*v*v - (f+k)*v
        u += dt * dudt
        v += dt * dvdt
    visualizer.update(u*255)
