#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# Simulation Parameters
X_SIZE = 256
Y_SIZE = 256
dx = 0.01
dt = 1
visualization_step = 16

# Model Parameters
Du = 2e-5
Dv = 1e-5
# amorphous
# f, k = 0.04, 0.06
# spots
# f, k = 0.035, 0.065
# wandering bubbles
# f, k = 0.012, 0.05
# waves
f, k = 0.025, 0.05

# Initialization
u = np.ones((X_SIZE, Y_SIZE))
v = np.zeros((X_SIZE, Y_SIZE))
# set initiale square pattern on center
square_size = 20
u[X_SIZE//2-square_size//2:X_SIZE//2+square_size//2, Y_SIZE//2-square_size//2:Y_SIZE//2+square_size//2] = 0.5
v[X_SIZE//2-square_size//2:X_SIZE//2+square_size//2, Y_SIZE//2-square_size//2:Y_SIZE//2+square_size//2] = 0.25
# add random noize in order to break the square symmetry
u = u + u*np.random.rand(X_SIZE, Y_SIZE)*0.01
v = v + u*np.random.rand(X_SIZE, Y_SIZE)*0.01

# Animation setup
fig = plt.figure()
ax = plt.axes()
hmap = ax.imshow(u, vmin=0, vmax=1)
fig.colorbar(hmap)

def update(frame):
    global u, v
    for i in range(visualization_step):
        # calculate laplacian
        laplacian_u = (np.roll(u, 1, axis=0) + np.roll(u, -1, axis=0) + np.roll(u, 1, axis=1) + np.roll(u, -1, axis=1) - 4*u) / (dx*dx)
        laplacian_v = (np.roll(v, 1, axis=0) + np.roll(v, -1, axis=0) + np.roll(v, 1, axis=1) + np.roll(v, -1, axis=1) - 4*v) / (dx*dx)
        # Gray-Scott model equation
        dudt = Du*laplacian_u - u*v*v + f*(1.0-u)
        dvdt = Dv*laplacian_v + u*v*v - (f+k)*v
        u += dt * dudt
        v += dt * dvdt
    hmap.set_array(u)
    return hmap,

anim = animation.FuncAnimation(fig, update, interval=1, blit=True)
plt.show(anim)
