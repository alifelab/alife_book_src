import sys
import numpy as np
import pygame
from pygame.locals import *
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
mpl.use('tkagg')


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
