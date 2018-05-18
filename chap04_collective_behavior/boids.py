#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import SwarmVisualizer

# visualizerの初期化。表示領域のサイズを与える。
WINDOW_RESOLUTION_W = 600
WINDOW_RESOLUTION_H = 600
visualizer = SwarmVisualizer((WINDOW_RESOLUTION_W, WINDOW_RESOLUTION_H))

# シミュレーションパラメタ
N = 64
COHESION_FORCE = 0.008
SEPARATION_FORCE = 0.04
ALIGNMENT_FORCE = 0.06
COHESION_DISTANCE = 0.05
SEPARATION_DISTANCE = 0.01
ALIGNMENT_DISTANCE = 0.05
COHESION_ANGLE = np.pi / 2
SEPARATION_ANGLE = np.pi / 2
ALIGNMENT_ANGLE = np.pi / 3
MIN_VEL = 0.001
MAX_VEL = 0.005

# 位置と速度
x = np.random.rand(N, 3) * 0.1
v = np.random.rand(N, 3) * MIN_VEL

while True:
    # 3 force, cohesion, separation and alignment
    dv_coh = np.zeros((N,3))
    dv_sep = np.zeros((N,3))
    dv_ali = np.zeros((N,3))

    for i in range(N):
        # xi and vi are position and velocity of target agent
        xi = x[i]
        vi = v[i]
        # xj and vj are list of position and velocity of other boids
        xj = np.delete(x, i, axis=0)
        vj = np.delete(v, i, axis=0)
        # list of distance and angle
        dist = np.linalg.norm(xj - xi, axis=1)
        angle = np.arccos(np.dot(vi, (xj-xi).T) / (np.linalg.norm(vi) * np.linalg.norm((xj-xi), axis=1)))
        # extract agents in interaction area.
        coh_agents_x = xj[ (dist < COHESION_DISTANCE) & (angle < COHESION_ANGLE) ]
        sep_agents_x = xj[ (dist < SEPARATION_DISTANCE) & (angle < SEPARATION_ANGLE) ]
        ali_agents_v = vj[ (dist < ALIGNMENT_DISTANCE) & (angle < ALIGNMENT_ANGLE) ]
        # calculate several forces.
        if (len(coh_agents_x) > 0):
            dv_coh[i] = COHESION_FORCE * (np.average(coh_agents_x, axis=0) - xi)
        if (len(sep_agents_x) > 0):
            dv_sep[i] = SEPARATION_FORCE * np.sum(xi - sep_agents_x, axis=0)
        if (len(ali_agents_v) > 0):
            dv_ali[i] = ALIGNMENT_FORCE * (np.average(ali_agents_v, axis=0) - vi)
    v += dv_coh + dv_sep + dv_ali

    # check min/max velocity.
    for i in range(N):
        v_abs = np.linalg.norm(v[i])
        if (v_abs < MIN_VEL):
            v[i] = MIN_VEL * v[i] / v_abs
        elif (v_abs > MAX_VEL):
            v[i] = MAX_VEL * v[i] / v_abs

    # update
    x += v

    visualizer.update(x, v, range=(-0.1, 0.1), focus_center_of_mass=True)
