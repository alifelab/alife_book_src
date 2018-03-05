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
visualization_step = 16
perturbation = 0.00001

# Initialization of variables
# X0, Y0 and Z0 are original trajectory
# X1, Y1 and Z1 are perturbated trajectory
T = np.arange(0, display_time, dt)
X0 = np.zeros(int(display_time/dt))
Y0 = np.zeros(int(display_time/dt))
Z0 = np.zeros(int(display_time/dt))
X0[-1] = 2.0 * np.random.rand() - 1.0
Y0[-1] = 2.0 * np.random.rand() - 1.0
Z0[-1] = 2.0 * np.random.rand() - 1.0

X1 = np.zeros(int(display_time/dt))
Y1 = np.zeros(int(display_time/dt))
Z1 = np.zeros(int(display_time/dt))
# set variables that added perturbation to original variables.
X1[-1] = X0[-1] + np.random.rand() * perturbation
Y1[-1] = Y0[-1] + np.random.rand() * perturbation
Z1[-1] = Z0[-1] + np.random.rand() * perturbation


# visualization setup
fig = plt.figure()

ax_0 = fig.add_subplot(3,1,1, xlim=(T[0], T[-1]), ylim=(-40, 40))
ax_1 = fig.add_subplot(3,1,2, xlim=(T[0], T[-1]), ylim=(-40, 40))
ax_2 = fig.add_subplot(3,1,3, xlim=(T[0], T[-1]), ylim=(0, 60))

# plot original and perturbated trajectory
# line_x[0] is original and line_x[1] is perturbated.
line_x = ax_0.plot(T, X0, T, X1)
line_y = ax_1.plot(T, Y0, T, Y1)
line_z = ax_2.plot(T, Z0, T, Z1)

ax_0.set_ylabel("x")
ax_1.set_ylabel("y")
ax_2.set_ylabel("z")

# calculate next step of variables
def lorenz(x, y, z):
    dxdt = -p*x + p*y
    dydt = -x*z + r*x - y
    dzdt = x*y - b*z
    new_x = x + dxdt * dt
    new_y = y + dydt * dt
    new_z = z + dzdt * dt
    return new_x, new_y, new_z


def update(frame):
    global X0, Y0, Z0, X1, Y1, Z1
    for i in range(visualization_step):
        new_x0, new_y0, new_z0 = lorenz(X0[-1], Y0[-1], Z0[-1])
        X0 = np.roll(X0, -1)
        Y0 = np.roll(Y0, -1)
        Z0 = np.roll(Z0, -1)
        X0[-1] = new_x0
        Y0[-1] = new_y0
        Z0[-1] = new_z0
        new_x1, new_y1, new_z1 = lorenz(X1[-1], Y1[-1], Z1[-1])
        X1 = np.roll(X1, -1)
        Y1 = np.roll(Y1, -1)
        Z1 = np.roll(Z1, -1)
        X1[-1] = new_x1
        Y1[-1] = new_y1
        Z1[-1] = new_z1
    line_x[0].set_data(T, X0)
    line_y[0].set_data(T, Y0)
    line_z[0].set_data(T, Z0)
    line_x[1].set_data(T, X1)
    line_y[1].set_data(T, Y1)
    line_z[1].set_data(T, Z1)
    return line_x[0], line_y[0], line_z[0],line_x[1], line_y[1], line_z[1]

anim = animation.FuncAnimation(fig, update, interval = 100, blit=True)
plt.show(anim)
