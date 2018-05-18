import sys
import numpy as np
import pygame
from pygame.locals import *
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D


class MatrixVisualizer(object):
    """docstring for MatrixVisualizer."""
    def __init__(self, size):
        super(MatrixVisualizer, self).__init__()
        pygame.init()
        self.width = size[0]
        self.height = size[1]
        self.screen = pygame.display.set_mode(size)
        #pygame.display.set_caption("title")
        #self.pixels = np.empty((self.width, self.height, 3), dtype=np.uint8)

    def update(self, matrix):
        matrix = np.repeat(matrix.T[:,:,np.newaxis], 3, axis=2)
        matrix[matrix<0] = 0
        matrix[matrix>255] = 255
        pixels = matrix.astype(np.uint8)
        img = pygame.surfarray.make_surface(pixels)
        if self.screen.get_size() != img.get_size():
            img = pygame.transform.scale(img, self.screen.get_size())
        self.screen.blit(img, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


class SwarmVisualizer(object):
    """docstring for SwarmVisualizer."""
    def __init__(self, size):
        super(SwarmVisualizer, self).__init__()
        # Animation setup
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')
        self.plot = None
        self.marker_plot = None


    def update(self, x, v, markers_x=None, range=(0, 0.5), focus_center_of_mass=False):
        if self.plot is None:
            self.plot = self.ax.scatter(x[:,0], x[:,1], x[:,2])

        if self.marker_plot is None and markers_x is not None:
            self.marker_plot = self.ax.scatter(markers_x[:,0], markers_x[:,1], markers_x[:,2])

        self.plot._offsets3d = (x[:,0], x[:,1], x[:,2])

        if self.marker_plot is not None:
            self.marker_plot._offsets3d = (markers_x[:,0], markers_x[:,1], markers_x[:,2])

        # show only around the center of gravity
        if focus_center_of_mass:
            l = (range[1] - range[0]) / 2
            self.ax.set_xlim(np.average(x[:,0])-l, np.average(x[:,0])+l)
            self.ax.set_ylim(np.average(x[:,1])-l, np.average(x[:,1])+l)
            self.ax.set_zlim(np.average(x[:,2])-l, np.average(x[:,2])+l)
        else:
            self.ax.set_xlim(range[0], range[1])
            self.ax.set_ylim(range[0], range[1])
            self.ax.set_zlim(range[0], range[1])

        plt.pause(0.001)
