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
SEPARATION_FORCE = 0.04
ALIGNMENT_FORCE = 0.06
# 力の働く距離
COHESION_DISTANCE = 0.05
SEPARATION_DISTANCE = 0.01
ALIGNMENT_DISTANCE = 0.05
# 力の働く角度
COHESION_ANGLE = np.pi / 2
SEPARATION_ANGLE = np.pi / 2
ALIGNMENT_ANGLE = np.pi / 3
MIN_VEL = 0.001
MAX_VEL = 0.005
# 中心力
# CENTRAL_FORCE = 0.0001
# CENTER_POSITION = np.zeros(3)

# 位置と速度
x = np.random.rand(N, 3) * 2 - 1
v = np.random.rand(N, 3) * MIN_VEL

while visualizer:
    # cohesion, separation, alignmentの３つの力を代入する変数
    dv_coh = np.zeros((N,3))
    dv_sep = np.zeros((N,3))
    dv_ali = np.zeros((N,3))

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
        if (len(coh_agents_x) > 0):
            dv_coh[i] = COHESION_FORCE * (np.average(coh_agents_x, axis=0) - x_this)
        if (len(sep_agents_x) > 0):
            dv_sep[i] = SEPARATION_FORCE * np.sum(x_this - sep_agents_x, axis=0)
        if (len(ali_agents_v) > 0):
            dv_ali[i] = ALIGNMENT_FORCE * (np.average(ali_agents_v, axis=0) - v_this)
    # 速度のアップデートと上限/下限のチェック
    v += dv_coh + dv_sep + dv_ali
    # v += CENTRAL_FORCE * (CENTER_POSITION - x)
    for i in range(N):
        v_abs = np.linalg.norm(v[i])
        if (v_abs < MIN_VEL):
            v[i] = MIN_VEL * v[i] / v_abs
        elif (v_abs > MAX_VEL):
            v[i] = MAX_VEL * v[i] / v_abs
    # 位置のアップデート
    x += v
    visualizer.update(x, v)
