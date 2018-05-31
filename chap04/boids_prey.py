#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import SwarmVisualizer

# visualizerの初期化 (Appendix参照)
visualizer = SwarmVisualizer()

# シミュレーションパラメタ
N = 256
# 力の強さ
COHESION_FORCE = 0.008
SEPARATION_FORCE = 0.4
ALIGNMENT_FORCE = 0.06
# 力の働く距離
COHESION_DISTANCE = 0.5
SEPARATION_DISTANCE = 0.05
ALIGNMENT_DISTANCE = 0.1
# 力の働く角度
COHESION_ANGLE = np.pi / 2
SEPARATION_ANGLE = np.pi / 2
ALIGNMENT_ANGLE = np.pi / 3
# 速度の上限/下限
MIN_VEL = 0.005
MAX_VEL = 0.03
# 境界で働く力（0にすると自由境界）
BOUNDARY_FORCE = 0.001
# エサに吸引される力と動かす間隔
PREY_FORCE = 0.0005
PREY_MOVEMENT_STEP = 150

# 位置と速度
x = np.random.rand(N, 3) * 2 - 1
v = (np.random.rand(N, 3) * 2 - 1 ) * MIN_VEL
# エサの位置
prey_x = np.random.rand(1, 3) * 2 - 1

# cohesion, separation, alignmentの３つの力を代入する変数
dv_coh = np.empty((N,3))
dv_sep = np.empty((N,3))
dv_ali = np.empty((N,3))
# 境界で働く力を代入する変数
dv_boundary = np.empty((N,3))

t = 0
while visualizer:
    for i in range(N):
        # ここで計算する個体の位置と速度
        x_this = x[i]
        v_this = v[i]
        # それ以外の個体の位置と速度の配列
        x_that = np.delete(x, i, axis=0)
        v_that = np.delete(v, i, axis=0)
        # 個体間の距離と角度
        distance = np.linalg.norm(x_that - x_this, axis=1)
        angle = np.arccos(np.dot(v_this, (x_that-x_this).T) / (np.linalg.norm(v_this) * np.linalg.norm((x_that-x_this), axis=1)))
        # 各力が働く範囲内の個体のリスト
        coh_agents_x = x_that[ (distance < COHESION_DISTANCE) & (angle < COHESION_ANGLE) ]
        sep_agents_x = x_that[ (distance < SEPARATION_DISTANCE) & (angle < SEPARATION_ANGLE) ]
        ali_agents_v = v_that[ (distance < ALIGNMENT_DISTANCE) & (angle < ALIGNMENT_ANGLE) ]
        # 各力の計算
        dv_coh[i] = COHESION_FORCE * (np.average(coh_agents_x, axis=0) - x_this) if (len(coh_agents_x) > 0) else 0
        dv_sep[i] = SEPARATION_FORCE * np.sum(x_this - sep_agents_x, axis=0) if (len(sep_agents_x) > 0) else 0
        dv_ali[i] = ALIGNMENT_FORCE * (np.average(ali_agents_v, axis=0) - v_this) if (len(ali_agents_v) > 0) else 0
        dist_center = np.linalg.norm(x_this) # 原点からの距離
        dv_boundary[i] = - BOUNDARY_FORCE * x_this * (dist_center - 1) / dist_center if (dist_center > 1) else 0
    # 速度のアップデートと上限/下限のチェック
    v += dv_coh + dv_sep + dv_ali + dv_boundary
    # エサへの吸引力を加える
    v += PREY_FORCE * (prey_x - x) / np.linalg.norm((prey_x - x), axis=1, keepdims=True)**2
    if t % PREY_MOVEMENT_STEP == 0:
        prey_x = np.random.rand(1, 3) * 2 - 1
        visualizer.set_markers(prey_x) # エサの位置を表示する（Appendix参照）
    t += 1
    for i in range(N):
        v_abs = np.linalg.norm(v[i])
        if (v_abs < MIN_VEL):
            v[i] = MIN_VEL * v[i] / v_abs
        elif (v_abs > MAX_VEL):
            v[i] = MAX_VEL * v[i] / v_abs
    # 位置のアップデート
    x += v
    visualizer.update(x, v)
