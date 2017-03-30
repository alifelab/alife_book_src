#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()

ax = plt.axes(xlim=(0, 10), ylim=(0, 10), aspect='equal')

circle = plt.Circle((5, 5), 0.75)


def init():
    circle.center = (5,5)
    ax.add_patch(circle)
    return circle,

def animate(i):
    x, y = circle.center
    x = 5 + np.sin(np.radians(i))
    y = 5 + np.cos(np.radians(i))
    circle.center = (x, y)
    return circle,

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames = 360,
                               interval = 20,
                               blit=True)
plt.show()
