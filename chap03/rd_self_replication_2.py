#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Virgo, Nathaniel David. 2011
Thermodynamics and the structure of living systems
"""
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
from alifebook_lib.visualizers import MatrixVisualizer

# visualizerの初期化 (Appendix参照)
visualizer = MatrixVisualizer()

# シミュレーションの各パラメタ
X_SIZE = 200
Y_SIZE = 200
dx = 0.01
dt = 1
visualization_step = 16

# モデルの各パラメタ
Da = 2e-5
Db = 1e-5
Dc = 1e-6
r = 0.0347
k_1 = 0.1
k_2 = 0.7
k_3 = 0.003
# 上記論文のオリジナルパラメタセット
# k_1 = 0.2
# k_2 = 0.8
# k_3 = 0.005

# パラメタa_resはシミュレーション開始時に1.02として、2000ステップかけて1.0まで減少させる。
# (良いパターンを作るための工夫。冒頭の論文のp104に記載あり。）
a_res = 1.02
a_res_end = 1.0
a_res_step = (a_res - a_res_end) / 2000

# 初期化
# (ここで行っている初期配置に関しては、冒頭の論文のp104に記載あり。）
a = np.ones((X_SIZE, Y_SIZE))
b = np.zeros((X_SIZE, Y_SIZE))
c = np.zeros((X_SIZE, Y_SIZE))

square_size_real = 0.1
a[100:110,100:110] = 0.45 + np.random.rand(10, 10)*0.1
b[100:110,100:110] = 0.45 + np.random.rand(10, 10)*0.1
c[101:108,112:119] = 1.5

while visualizer:
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
        # a_resを減らす（a_res_endよりは減らさない）
        a_res = max(a_res - a_res_step, a_res_end)
    # ここでは、b + c をグレースケールで表示。見たいものに変更してみましょう。
    visualizer.update(b+c)
