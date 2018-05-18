import sys
import numpy as np
import pygame
from pygame.locals import *
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
mpl.use('tkagg')

particle_shapes = None

def draw(ax, particles):
    global particle_shapes, bond_shapes
    if particle_shapes is None:
        particle_shapes = np.empty(particles.shape, dtype=object)
    for line in bond_shapes.values():
        line.remove()
    bond_shapes = {}
    for x in range(particles.shape[0]):
        for y in range(particles.shape[1]):
            p = particles[x,y]
            _draw_particle(ax, x, y, p['type'])
            for (bx, by) in p['bonds']:
                _draw_bond(ax, x, y, bx, by, particles.shape[0], particles.shape[1])


def _draw_particle(ax, x, y, particle_type):
    if particle_shapes[x, y] is not None:
        if isinstance(particle_shapes[x,y], list):
            particle_shapes[x,y][0].remove()
            particle_shapes[x,y][1].remove()
        else:
            particle_shapes[x, y].remove()

    if particle_type == 'HOLE':
        s = None
    elif particle_type is 'SUBSTRATE':
        s = plt.Circle((x, y), 0.25, facecolor='c')
        ax.add_patch(s)
    elif particle_type is 'CATALYST':
        s = plt.Circle((x, y), 0.4, facecolor='m')
        ax.add_patch(s)
    elif particle_type is 'LINK':
        s = plt.Rectangle([x - 0.35, y - 0.35], 0.7, 0.7, edgecolor='b', facecolor='w')
        ax.add_patch(s)
    elif particle_type is 'LINK_SUBSTRATE':
        s0 = plt.Rectangle([x - 0.35, y - 0.35], 0.7, 0.7, edgecolor='b', facecolor='w')
        ax.add_patch(s0)
        s1 = plt.Circle((x, y), 0.25, facecolor='c')
        ax.add_patch(s1)
        s = [s0, s1]
    particle_shapes[x, y] = s

bond_shapes = {}
def _draw_bond(ax, x0, y0, x1, y1, x_size, y_size):
    #print("draw", x0, y0, x1, y1)
    x0_n = x_size if (x0 == 0 and x1 == x_size-1) else x0
    y0_n = y_size if (y0 == 0 and y1 == y_size-1) else y0
    x1_n = x_size if (x1 == 0 and x0 == x_size-1) else x1
    y1_n = y_size if (y1 == 0 and y0 == y_size-1) else y1

    start_x = x0_n + 0.35 * (x1_n - x0_n)
    start_y = y0_n + 0.35 * (y1_n - y0_n)
    end_x = x1_n - 0.35 * (x1_n - x0_n)
    end_y = y1_n - 0.35 * (y1_n - y0_n)
    line = plt.Polygon([(start_x, start_y), (end_x, end_y)], color='b', lw=1.5)
    ax.add_patch(line)
    bond_shapes[(x0, y0, x1, y1)] = line

def clear_bond(ax, x0, y0, x1, y1):
    #print("clear", x0, y0, x1, y1)
    try:
        key = (x0, y0, x1, y1)
        if key in bond_shapes:
            bond_shapes[key].remove()
            bond_shapes.pop(key)
        else:
            key = (x1, y1, x0, y0)
            bond_shapes[key].remove()
            bond_shapes.pop(key)
    except KeyError:
        print(x0,y0,x1,y1)
        print(bond_shapes.keys())
        exit()


class SCLVisualizer(object):
    """docstring for SCLVisualizer."""
    def __init__(self, size):
        super(SCLVisualizer, self).__init__()
        #
        # Initialization
        #
        plt.figure(figsize=(8,8))
        self.axis = None

    def update(self, particles):
        if self.axis is None:
            self.axis = plt.axes(xlim=(-1,particles.shape[0]), ylim=(-1,particles.shape[1]), aspect='equal')
            self.axis.set_xticks([])
            self.axis.set_yticks([])
            self.axis.invert_yaxis()

        draw(self.axis, particles)
        plt.pause(0.001)
