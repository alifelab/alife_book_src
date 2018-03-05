#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# Simulation Parameters
X_SIZE = 256
Y_SIZE = 256
dx = 0.01
dt = 1
visualization_step = 64

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
f_min = 0.01
f_max = 0.05
k_min = 0.05
k_max = 0.07

f_lin = np.linspace(f_min, f_max, X_SIZE)
k_lin = np.linspace(k_min, k_max, Y_SIZE)
f, k = np.meshgrid(f_lin, k_lin)

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
# setup axis label and ticks
# show only min and max values of parameters.
ax.set_xlabel("F")
ax.set_ylabel("K")
ax.set_xticks([0,X_SIZE])
ax.set_xticklabels([f_min,f_max])
ax.set_yticks([0,Y_SIZE])
ax.set_yticklabels([k_min,k_max])

def update(frame):
    global u, v
    for i in range(visualization_step):
        # calculate laplacian
        # periodic boundary condition is not suitable for parameter space.
        # so we extend u,v matrix with same value of edge and calculate laplacian.
        u_pad = np.pad(u, 1, 'edge')
        v_pad = np.pad(v, 1, 'edge')
        laplacian_u = (np.roll(u_pad, 1, axis=0) + np.roll(u_pad, -1, axis=0) + np.roll(u_pad, 1, axis=1) + np.roll(u_pad, -1, axis=1) - 4*u_pad) / (dx*dx)
        laplacian_v = (np.roll(v_pad, 1, axis=0) + np.roll(v_pad, -1, axis=0) + np.roll(v_pad, 1, axis=1) + np.roll(v_pad, -1, axis=1) - 4*v_pad) / (dx*dx)
        # next, remove edge value that extended before.
        laplacian_u = laplacian_u[1:-1,1:-1]
        laplacian_v = laplacian_v[1:-1,1:-1]
        # Gray-Scott model equation
        dudt = Du*laplacian_u - u*v*v + f*(1.0-u)
        dvdt = Dv*laplacian_v + u*v*v - (f+k)*v
        u += dt * dudt
        v += dt * dvdt
    #hmap.set_array(u.T)
    hmap.set_array(u)
    return hmap,

anim = animation.FuncAnimation(fig, update, interval=100, blit=True)
plt.show(anim)
