# -*- coding: utf-8 -*-
from os import path
import numpy as np
from vispy import app
from vispy.scene import SceneCanvas, PanZoomCamera, MatrixTransform
from vispy.scene.visuals import Image, Polygon

ENV_MAP_PATH = path.join(path.dirname(path.abspath(__file__)), 'img')

class AntSimulator(object):
    MIN_VELOCITY = 0.2
    MAX_VELOCITY = 0.8
    # MIN_VELOCITY = 0.128 # 0.0005 * self._FIELD_WIDTH #original on legacy program
    # MAX_VELOCITY = 0.256 # 0.001 * self._FIELD_WIDTH #original on legacy program
    MAX_ANGULAR_VELOCITY = 0.05 * np.pi
    SENSOR_NUM = 7
    AGENT_RADIUS = 12.8 # 0.05 * self._FIELD_WIDTH  #original on legacy program
    SENSOR_NOISE = 0.1

    def __init__(self, N, width=600, height=600, decay_rate=1.0, hormone_secretion=None):
        from PIL.Image import open as open_image
        # setup simulation
        self._N = N
        self._INITIAL_FIELD = np.array(open_image(path.join(ENV_MAP_PATH, 'envmap01.png'))).astype(np.float32) / 255.
        #self._INITIAL_FIELD = np.zeros(self._INITIAL_FIELD.shape)
        self._FIELD_WIDTH = self._INITIAL_FIELD.shape[1]
        self._FIELD_HEIGHT = self._INITIAL_FIELD.shape[0]
        self._FIELD_DECAY_RATE = decay_rate
        self._SECRATION = hormone_secretion
        sensor_th = np.linspace(0, 2*np.pi, self.SENSOR_NUM, endpoint=False)
        self._SENSOR_POSITION = self.AGENT_RADIUS * np.array([np.cos(sensor_th), np.sin(sensor_th)]).T
        self.reset()  # initialize all variables, position, velocity and field status

        # setup display
        self._canvas = SceneCanvas(size=(width, height), position=(0,0), keys='interactive', title="ALife book "+self.__class__.__name__)
        self._canvas.events.mouse_double_click.connect(self._on_mouse_double_click)
        self._view = self._canvas.central_widget.add_view()
        self._view.camera = PanZoomCamera((0, 0, self._FIELD_WIDTH, self._FIELD_HEIGHT), aspect=1)
        self._field_image = Image(self._field, interpolation='nearest', parent=self._view.scene, method='subdivide', clim=(0,1))
        self._agent_polygon = []
        for i in range(self._N):
            p = AntSimulator._generate_agent_visual_polygon(self.AGENT_RADIUS)
            p.parent = self._field_image
            self._agent_polygon.append(p)
        self._canvas.show()

    def reset(self, random_seed=None):
        np.random.seed(random_seed)
        self._field =  self._INITIAL_FIELD.copy()
        self._agents_pos = np.random.random((self._N, 2)).astype(np.float32) * self._FIELD_WIDTH
        self._agents_th = np.random.random(self._N).astype(np.float32) * np.pi * 2
        self._agents_vel = np.ones(self._N).astype(np.float32) * 0.001
        self._agents_ang_vel = (np.random.random(self._N).astype(np.float32) * 0.1 - 0.05) * np.pi
        self._agents_fitness = np.zeros(self._N)

    def get_sensor_data(self):
        sensor_data = np.empty((self._N, 7))
        for ai in range(self._N):
            th = self._agents_th[ai]
            rot_mat = np.array([[np.cos(th), -np.sin(th)],[np.sin(th), np.cos(th)]])
            for si, sensor_pos in enumerate(self._SENSOR_POSITION):
                sx, sy = rot_mat @ sensor_pos
                xi = int((sx + self._agents_pos[ai][0] + self._FIELD_WIDTH) % self._FIELD_WIDTH)
                yi = int((sy + self._agents_pos[ai][1] + self._FIELD_HEIGHT) % self._FIELD_HEIGHT)
                sensor_data[ai, si] = self._field[yi, xi] + np.random.randn() * self.SENSOR_NOISE
        return sensor_data

    def set_agent_color(self, index, color):
        self._agent_polygon[index].border_color = color

    def update(self, action):
        # action take 0-1 value
        v = action[:,0] * (self.MAX_VELOCITY - self.MIN_VELOCITY) + self.MIN_VELOCITY
        av = (action[:,1] - 0.5) * 2 * self.MAX_ANGULAR_VELOCITY
        self._agents_pos += (v * [np.cos(self._agents_th), np.sin(self._agents_th)]).T
        self._agents_th += av

        self._agents_pos[:,0] = (self._agents_pos[:,0] + self._FIELD_WIDTH) % self._FIELD_WIDTH
        self._agents_pos[:,1] = (self._agents_pos[:,1] + self._FIELD_HEIGHT) % self._FIELD_HEIGHT
        self._agents_th = (self._agents_th + 2.0 * np.pi) % (2.0 * np.pi)

        for x, y in self._agents_pos.astype(int):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    xi = (x + i + self._FIELD_WIDTH) % self._FIELD_WIDTH
                    yi = (y + j + self._FIELD_HEIGHT) % self._FIELD_HEIGHT
                    self._agents_fitness += self._field[yi,xi]
                    if self._SECRATION is None:
                        #self._field[yi,xi] *= 0.5 # current running
                        self._field[yi,xi] *= 0.9 # sampledata_last2
                    else:
                        self._field[yi, xi] += self._SECRATION
        self._field.clip(0, 1)

        self._field *= self._FIELD_DECAY_RATE

        self._field_image.set_data(self._field)
        for polygon, (x, y), th in zip(self._agent_polygon, self._agents_pos, self._agents_th):
            polygon.transform.reset()
            polygon.transform.rotate(180 * th / np.pi, (0,0,1))
            polygon.transform.translate((x, y))

        self._canvas.update()
        app.process_events()

    def get_fitness(self):
        return self._agents_fitness

    def _on_mouse_double_click(self, event):
        self._view.camera.set_range(x = (0, self._FIELD_WIDTH), y = (0, self._FIELD_HEIGHT), margin=0)

    def __bool__(self):
        return not self._canvas._closed

    @staticmethod
    def _generate_agent_visual_polygon(radius):
        th = np.linspace(0, 2*np.pi, 16)
        points = np.c_[np.cos(th), np.sin(th)]
        points = np.r_[[[0,0]], points] * radius
        polygon = Polygon(points, color=(0, 0, 0, 0), border_color=(1, 0, 0), border_method='agg', border_width=2)
        #polygon = Polygon(points, color=(0, 0, 0, 0), border_color=(1, 0, 0))  # more fast, but agents visual is hard to seee
        polygon.transform = MatrixTransform()
        return polygon


if __name__ == '__main__':
    N = 3
    simulator = AntSimulator(N)
    simulator.reset(1234)
    while simulator:
        observation = simulator.get_sensor_data()
        # go forward
        # action = np.c_[np.ones(N), np.ones(N) * 0.5]
        # random motion
        action = np.c_[np.random.random(N), np.random.random(N)]
        simulator.update(action)
