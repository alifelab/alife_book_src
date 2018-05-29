import sys
import numpy as np
import pygame
from pygame.locals import *
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import vispy
from vispy.scene import SceneCanvas
from vispy.scene import visuals

class SwarmVisualizer(object):
    """docstring for SwarmVisualizer."""
    ARROW_SIZE = 20

    def __init__(self, width=600, height=600):
        self._canvas = SceneCanvas(size=(width, height), position=(0,0), title="ALife book "+self.__class__.__name__)
        self._view = self._canvas.central_widget.add_view()
        self._view.camera = 'arcball'
        #self._view.camera = 'turntable'
        self._axis = visuals.XYZAxis(parent=self._view.scene)
        self._arrows = None
        self._canvas.show()

    def update(self, position, direction):
        assert position.shape[1] == 3
        assert direction.shape[1] == 3
        assert position.shape[0] == direction.shape[0]
        if self._arrows is None:
            self._arrows = visuals.Arrow(arrow_size=self.ARROW_SIZE, parent=self._view.scene)
            #self._view.add(arrows)
        # arrow_coordinate[0::2] is position of arrow and [1::2] is tail direction
        arrow_coordinate = np.repeat(position, 2, axis=0)
        arrow_coordinate[::2] -=  direction
        self._arrows.set_data(arrows=arrow_coordinate.reshape((-1, 6)))
        self._canvas.update()
        vispy.app.process_events()

    def __bool__(self):
        return not self._canvas._closed


class SwarmVisualizer_regacy(object):
    """docstring for SwarmVisualizer_regacy."""
    def __init__(self, width=600, height=600):
        super(SwarmVisualizer_regacy, self).__init__()
        # Animation setup
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')
        self.plot = None
        self.marker_plot = None


    def update(self, x, v, markers_x=None, range=(-1, 1), focus_center_of_mass=False):
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

    def __bool__(self):
        return True

if __name__ == '__main__':
    N = 10
    v = SwarmVisualizer_regacy()
    #v = SwarmVisualizer()
    pos = np.random.normal(size=(N, 3), scale=0.2)
    vel = np.random.normal(size=(N, 3), scale=0.2) * 0.01
    while True:
        vel -= pos * 0.0001
        pos +=  vel
        v.update(pos, vel)
