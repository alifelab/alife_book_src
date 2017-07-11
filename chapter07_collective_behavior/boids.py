#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

# simulation parameters
N = 64
COHISION_FORCE = 0.008
SEPARATIN_FORCE = 0.04
ALIGNMENT_FORCE = 0.06
COHISION_DISTANCE = 0.05
SEPARATIN_DISTANCE = 0.01
ALIGNMENT_DISTANCE = 0.05
COHISION_ANGLE = np.pi / 2
SEPARATIN_ANGLE = np.pi / 2
ALIGNMENT_ANGLE = np.pi / 3
MIN_VEL = 0.001
MAX_VEL = 0.005

x = np.random.rand(N, 3) * 0.1
v = np.random.rand(N, 3) * MIN_VEL

# Animation setup
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plots = ax.scatter(x[:,0], x[:,1], x[:,2])

def update(frame):
    global x, v
    # 3 force, cohesion, separation and alignment
    dv_coh = np.zeros((N,3))
    dv_sep = np.zeros((N,3))
    dv_ali = np.zeros((N,3))

    for i in range(N):
        # xi and vi are position and velocity of target agent
        xi = x[i]
        vi = v[i]
        # xj and vj are list of position and velocity of other boids
        xj = np.delete(x, i, axis=0)
        vj = np.delete(v, i, axis=0)
        # list of distance and angle
        dist = np.linalg.norm(xj - xi, axis=1)
        angle = np.arccos(np.dot(vi, (xj-xi).T) / (np.linalg.norm(vi) * np.linalg.norm((xj-xi), axis=1)))
        # extract agents in interaction area.
        coh_agents_x = xj[ (dist < COHISION_DISTANCE) & (angle < COHISION_ANGLE) ]
        sep_agents_x = xj[ (dist < SEPARATIN_DISTANCE) & (angle < SEPARATIN_ANGLE) ]
        ali_agents_v = vj[ (dist < ALIGNMENT_DISTANCE) & (angle < ALIGNMENT_ANGLE) ]
        # calculate several forces.
        if (len(coh_agents_x) > 0):
            dv_coh[i] = COHISION_FORCE * (np.average(coh_agents_x, axis=0) - xi)
        if (len(sep_agents_x) > 0):
            dv_sep[i] = SEPARATIN_FORCE * np.sum(xi - sep_agents_x, axis=0)
        if (len(ali_agents_v) > 0):
            dv_ali[i] = ALIGNMENT_FORCE * (np.average(ali_agents_v, axis=0) - vi)
    v += dv_coh + dv_sep + dv_ali
    
    # check min/max velocity.
    for i in range(N):
        v_abs = np.linalg.norm(v[i])
        if (v_abs < MIN_VEL):
            v[i] = MIN_VEL * v[i] / v_abs
        elif (v_abs > MAX_VEL):
            v[i] = MAX_VEL * v[i] / v_abs

    # update
    x += v
    
    plots._offsets3d = (x[:,0], x[:,1], x[:,2])

    # show only around the center of gravity
    ax.set_xlim(np.average(x[:,0])-0.1, np.average(x[:,0])+0.1)
    ax.set_ylim(np.average(x[:,1])-0.1, np.average(x[:,1])+0.1)
    ax.set_zlim(np.average(x[:,2])-0.1, np.average(x[:,2])+0.1)

#anim = animation.FuncAnimation(fig, update, interval=100, blit=True)
anim = animation.FuncAnimation(fig, update, interval=100)
plt.show(anim)
