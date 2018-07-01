#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from t3 import T3

"""
t3.pyの出力をプロットします.
実行するにはmatplotlibが必要です.
インストール方法
$ pip install matplotlib
"""

fig = plt.figure()
ax = plt.axes(xlim=(0, 1), ylim=(0, 1))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

t3 = T3()

def update(frame):
    ax.clear()
    d = np.array([t3.next() for i in range(1000)])
    ax.scatter(d[:,0], d[:,1], s=1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return

anim = animation.FuncAnimation(fig, update, interval = 20, blit=False)
plt.show(anim)
