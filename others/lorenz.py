#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import ipdb


# Parameters
p = 10
r = 28
b = 8/3
dt = 0.01
display_time = 15.0
visualization_step = 8

# Initialization of variables
T = np.arange(0, display_time, dt)
X = np.zeros(int(display_time/dt))
Y = np.zeros(int(display_time/dt))
Z = np.zeros(int(display_time/dt))
X[-1] = 2.0 * np.random.rand() - 1.0
Y[-1] = 2.0 * np.random.rand() - 1.0
Z[-1] = 2.0 * np.random.rand() - 1.0

fig = plt.figure()

ax_0 = fig.add_subplot(3,1,1, xlim=(T[0], T[-1]), ylim=(-80, 80))
ax_1 = fig.add_subplot(3,1,2, xlim=(T[0], T[-1]), ylim=(-80, 80))
ax_2 = fig.add_subplot(3,1,3, xlim=(T[0], T[-1]), ylim=(-80, 80))

line_x, = ax_0.plot(T, X)
line_y, = ax_1.plot(T, Y)
line_z, = ax_2.plot(T, Z)

ax_0.set_ylabel("x")
ax_1.set_ylabel("y")
ax_2.set_ylabel("z")

def update(frame):
    global X, Y, Z
    for i in range(visualization_step):
        x = X[-1]
        y = Y[-1]
        z = Z[-1]
        dxdt = -p*x + p*y
        dydt = -x*z + r*x - y
        dzdt = x*y - b*z
        x += dxdt * dt
        y += dydt * dt
        z += dzdt * dt
        X = np.roll(X, -1)
        X[-1] = x
        Y = np.roll(Y, -1)
        Y[-1] = y
        Z = np.roll(Z, -1)
        Z[-1] = z
    line_x.set_data(T, X)
    line_y.set_data(T, Y)
    line_z.set_data(T, Z)
    return line_x, line_y, line_z

anim = animation.FuncAnimation(fig, update, interval = 100, blit=True)
plt.show(anim)
