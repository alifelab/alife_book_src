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
PREY_FORCE = 0.0001
COHESION_FORCE = 0.01
SEPARATION_FORCE = 0.01
ALIGNMENT_FORCE = 0.1
# all interaction distance and angle take same value for simplify.
INTERACTION_DISTANCE = 0.05
INTERACTION_ANGLE = np.pi / 3
MIN_VEL = 0.001
MAX_VEL = 0.005
PREY_MOVEMENT_STEP = 50

# 位置と速度
x = np.random.rand(N, 3) * 0.1
v = np.random.rand(N, 3) * MIN_VEL
# preyの位置
prey_x = np.random.rand(1, 3) * 0.5

t = 0
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
        interact_agents_x = xj[ (dist < INTERACTION_DISTANCE) & (angle < INTERACTION_ANGLE) ]
        interact_agents_v = vj[ (dist < INTERACTION_DISTANCE) & (angle < INTERACTION_ANGLE) ]
        # calculate several forces.
        if (len(interact_agents_x) > 0):
            dv_coh[i] = COHESION_FORCE * (np.average(interact_agents_x, axis=0) - xi)
        if (len(interact_agents_x) > 0):
            dv_sep[i] = SEPARATION_FORCE * np.sum(xi - interact_agents_x, axis=0)
        if (len(interact_agents_v) > 0):
            dv_ali[i] = ALIGNMENT_FORCE * (np.average(interact_agents_v, axis=0) - vi)
    v += dv_coh + dv_sep + dv_ali

    # PREY MODEL
    v += PREY_FORCE * (prey_x - x) / np.linalg.norm((prey_x - x), axis=1, keepdims=True)**2
    if t % PREY_MOVEMENT_STEP == 0:
        prey_x = np.random.rand(1, 3) * 0.5
    t += 1

    # check min/max velocity.
    for i in range(N):
        v_abs = np.linalg.norm(v[i])
        if (v_abs < MIN_VEL):
            v[i] = MIN_VEL * v[i] / v_abs
        elif (v_abs > MAX_VEL):
            v[i] = MAX_VEL * v[i] / v_abs

    # update
    x += v

    visualizer.update(x, v, markers_x=prey_x, range=(0, 0.5))
