#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.axes(xlim=(0, 10), ylim=(0, 10), aspect='equal')
circle = plt.Circle((5, 5), 0.75)
ax.add_patch(circle)

def update(frame):
    x = 5 + 3*np.sin(np.radians(frame))
    y = 5 + 3*np.cos(np.radians(frame))
    circle.center = (x, y)
    return circle,

anim = animation.FuncAnimation(fig, update, interval = 20, blit=True)
plt.show(anim)
