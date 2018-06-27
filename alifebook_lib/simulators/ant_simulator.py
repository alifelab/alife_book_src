# -*- coding: utf-8 -*-
from os import path
import numpy as np
from vispy import app
from vispy.scene import SceneCanvas, PanZoomCamera, MatrixTransform
from vispy.scene.visuals import Image, Polygon
from PIL.Image import open as open_image

ENV_MAP_PATH = path.join(path.dirname(path.abspath(__file__)), 'img')

class AntSimulator(object):
    """docstring for AntSimulator."""
    def __init__(self, N, width=600, height=600, decay_rate=1.0, hormone_secretion=None):
        # setup simulation
        self._N = N
        self._potential_init = np.array(open_image(path.join(ENV_MAP_PATH, 'envmap01.png'))).astype(np.float32) / 255.
        self._potential = self._potential_init.copy()
        self._potential_grid_size = self._potential_init.shape
        self._potential_decay_rate = decay_rate
        self._hormone_secretion = hormone_secretion
        self.reset()

        # setup display
        self._canvas = SceneCanvas(size=(width, height), position=(0,0), keys='interactive', title="ALife book "+self.__class__.__name__)
        self._canvas.events.mouse_double_click.connect(self._on_mouse_double_click)
        self._view = self._canvas.central_widget.add_view()
        self._view.camera = PanZoomCamera((0, 0, self._potential_grid_size[1], self._potential_grid_size[0]), aspect=1)
        self._potential_image = Image(self._potential, interpolation='nearest', parent=self._view.scene, method='subdivide', clim=(0,1))
        self._agent_polygon = []
        for i in range(self._N):
            p = AntSimulator._generate_agent_visual_polygon()
            p.parent = self._potential_image
            self._agent_polygon.append(p)
        self._canvas.show()

    def reset(self, seed=1234):
        np.random.seed(seed)
        self._potential =  self._potential_init.copy()
        self._agents_pos = np.random.random((self._N, 2)).astype(np.float32)
        self._agents_th = np.random.random(self._N).astype(np.float32) * np.pi * 2
        self._agents_vel = np.ones(self._N).astype(np.float32) * 0.001
        self._agents_ang_vel = (np.random.random(self._N).astype(np.float32) * 0.1 - 0.05) * np.pi
        self._agents_radius = 0.05
        #self._agents_radius = 0.025
        self._sensor_angle = np.linspace(0, 2*np.pi, 7, endpoint=False)
        self._agents_fitness = np.zeros(self._N)

    def get_sensor_data(self):
        obs = np.empty((self._N, 7))
        for ai in range(self._N):
            for si in range(7):
                th = self._agents_th[ai] + self._sensor_angle[si]
                x = self._agents_pos[ai][0] + self._agents_radius * np.cos(th)
                y = self._agents_pos[ai][1] + self._agents_radius * np.sin(th)
                x %= 1.0
                y %= 1.0
                xi = int(x * self._potential_grid_size[1])
                yi = int(y * self._potential_grid_size[0])
                obs[ai, si] = self._potential[yi, xi]
        return obs

    def set_agent_color(self, index, color):
        self._agent_polygon[index].border_color = color

    def update(self, action):
        # action take 0-1 value
        v = action[:,0] * 0.0005 + 0.0005
        av = (action[:,1] - 0.5) * 2 * np.pi * 0.05
        self._agents_pos += (v * [np.cos(self._agents_th), np.sin(self._agents_th)]).T
        self._agents_th += av

        self._agents_pos %= 1.0
        self._agents_th %= (2.0 * np.pi)

        grid_idx = (self._agents_pos * self._potential_grid_size).astype(int)
        self._agents_fitness += [self._potential[y,x] for x,y in grid_idx]
        if self._hormone_secretion is None:
            for x, y in grid_idx:
                self._potential[y,x] = 0
        else:
            for x, y in grid_idx:
                for i in list(range(-1, 2)):
                    for j in list(range(-1, 2)):
                        self._potential[(y+i)%self._potential_grid_size[0],(x+j)%self._potential_grid_size[1]] += self._hormone_secretion
            self._potential.clip(0, 1)
        self._potential *= self._potential_decay_rate

        self._potential_image.set_data(self._potential)
        for polygon, pos, th in zip(self._agent_polygon, self._agents_pos, self._agents_th):
            polygon.transform.reset()
            # polygon.transform.scale((self._agents_radius, self._agents_radius))
            # polygon.transform.rotate(180 * th / np.pi, (0,0,1))
            # polygon.transform.translate(pos)
            # polygon.transform.scale((self._potential_grid_size[1], self._potential_grid_size[0]))
            polygon.transform.scale((self._agents_radius*self._potential_grid_size[1], self._agents_radius*self._potential_grid_size[0]))
            polygon.transform.rotate(180 * th / np.pi, (0,0,1))
            polygon.transform.translate((pos[0]*self._potential_grid_size[1], pos[1]*self._potential_grid_size[0]))

        self._canvas.update()
        app.process_events()

    def get_fitness(self):
        return self._agents_fitness

    def _on_mouse_double_click(self, event):
        self._view.camera.set_range(x = (0,self._potential_grid_size[1]),
                                    y = (0,self._potential_grid_size[0]),
                                    margin=0)

    def __bool__(self):
        return not self._canvas._closed

    @staticmethod
    def _generate_agent_visual_polygon():
        th = np.linspace(0, 2*np.pi, 64)
        points = np.c_[np.cos(th), np.sin(th)]
        points = np.r_[[[0,0]], points]
        #polygon = Polygon(points, color=(0, 0, 0, 0), border_color=(1, 0, 0), border_method='agg', border_width=2)
        polygon = Polygon(points, color=(0, 0, 0, 0), border_color=(1, 0, 0))
        polygon.transform = MatrixTransform()
        return polygon



if __name__ == '__main__':
    N = 3
    simulator = AntSimulator(N)
    #simulator.reset()
    while simulator:
        observation = simulator.get_sensor_data()
        # go forward
        # action = np.c_[np.ones(N), np.ones(N) * 0.5]
        # random motion
        action = np.c_[np.random.random(N), np.random.random(N)]
        simulator.update(action)
