# -*- coding: utf-8 -*-
from os import path
import numpy as np
from vispy import app, gloo, visuals
from vispy.visuals import transforms
from vispy.util.transforms import perspective
from PIL import Image

GLSL_PATH = path.join(path.dirname(path.abspath(__file__)), 'glsl')
ENV_MAP_PATH = path.join(path.dirname(path.abspath(__file__)), 'img')

DEBUG_ENV = False

#class AntSimulator(app.Canvas):
class AntSimulator(object):
    """docstring for AntSimulator."""
    def __init__(self, N, width=600, height=600, decay_rate=1.0, secretion=False):
        #super(AntSimulator, self).__init__(title='Title', size=(600, 600), resizable=True, position=(0, 0), keys='interactive')

        #app.Canvas(title='Title', size=(600, 600), resizable=True, position=(0, 0), keys='interactive')
        self._canvas = app.Canvas(size=(width, height), position=(0,0), title="ALife book "+self.__class__.__name__)
        self._canvas.events.draw.connect(self.on_draw)
        # simulation settings
        self._N = N
        self._potential_init = np.array(Image.open(path.join(ENV_MAP_PATH, 'envmap01.png'))).astype(np.float32) / 255.
        self._potential_grid_size = self._potential_init.shape
        self._potential_decay_rate = decay_rate
        self._hormone_secretion = secretion

        self.reset()

        vert = open(path.join(GLSL_PATH, 'color_map_vert.glsl'), 'r').read()
        frag = open(path.join(GLSL_PATH, 'color_map_frag.glsl'), 'r').read()
        self.potential_render = gloo.Program(vert, frag)
        self.potential_render["a_position"] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.potential_render["a_texcoord"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.potential_render["u_texture"] = self._potential
        self.potential_render["u_texture"].interpolation = 'nearest'

        self.agents_visuals = []
        self.agents_head_visuals = []
        #for pos, vel in zip(self._agents_pos, self._agents_vel):
        for pos, th in zip(self._agents_pos, self._agents_th):
            v = visuals.EllipseVisual((pos[0], pos[1], 0), radius=self._agents_radius,
                                      color=(0, 0, 0, 0), border_color="red", border_width=3)
            v.transform = transforms.NullTransform()
            self.agents_visuals.append(v)
            line = [
                pos,
                [pos[0] + self._agents_radius * np.cos(th), pos[1] + self._agents_radius * np.sin(th)]
            ]
            visuals.LineVisual(line, color='red')
            self.agents_head_visuals.append(v)

        #gloo.set_state('translucent', clear_color='white')
        gloo.set_state(clear_color='black', blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

        #self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        self._canvas.show()
        #self.app.run()

    def reset(self, seed=1234):
        np.random.seed(seed)
        if DEBUG_ENV:
            self._potential = np.zeros((self._potential_grid_size[1], self._potential_grid_size[1])).astype(np.float32)
            self._potential[100:, 100:] = 1
            self._potential[:100, :100] = 0.5
        else:
            self._potential =  self._potential_init.copy()
        self._agents_pos = np.random.random((self._N, 2)).astype(np.float32)
        self._agents_th = np.random.random(self._N).astype(np.float32) * np.pi * 2
        self._agents_vel = np.ones(self._N).astype(np.float32) * 0.001
        self._agents_ang_vel = (np.random.random(self._N).astype(np.float32) * 0.1 - 0.05) * np.pi
        self._agents_radius = 0.05
        self._sensor_angle = np.linspace(0, 2*np.pi, 7, endpoint=False)
        self._agents_fitness = np.zeros(self._N)

    # def on_timer(self, event):
    #     self.update()

    def on_draw(self, event):
        gloo.clear()
        self.potential_render["u_texture"] = self._potential
        self.potential_render.draw('triangle_strip')
        #for v, pos, vel in zip(self.agents_visuals, self._agents_pos, self._agents_vel):
        for v, hv, pos, th in zip(self.agents_visuals, self.agents_head_visuals, self._agents_pos, self._agents_th):
            ps = [pos[0]*2-1, pos[1]*2-1, 0]
            v.center = ps
            v.draw()
            line = [
                ps[:2],
                [ps[0] + self._agents_radius * np.cos(th), ps[1] + self._agents_radius * np.sin(th)]
            ]
            hv.pos = line
            hv.draw()

#    def on_resize(self, event):
#        gloo.set_viewport(0, 0, *self.physical_size)

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
        if len(color) == 4:
            c = color
        elif len(color) == 3:
            c = (color[0], color[1], color[2], 1)
        else:
            # TODO: warning
            c = (1, 0, 0, 1)
        self.agents_visuals[index].border_color = c

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
        if self._hormone_secretion:
            for x, y in grid_idx:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        self._potential[(y+i)%self._potential_grid_size[0],(x+j)%self._potential_grid_size[1]] = 1
        else:
            for x, y in grid_idx:
                self._potential[y,x] = 0
        self._potential *= self._potential_decay_rate
        self._canvas.update()
        app.process_events()

    def get_fitness(self):
        return self._agents_fitness

    def __bool__(self):
        return not self._canvas._closed

if __name__ == '__main__':
    N = 3
    simulator = AntSimulator(N)
    #simulator.reset()

    while simulator:
        observation = simulator.get_sensor_data()
        # go forward
        # v = np.ones(N)
        # av = np.ones(N) * 0.5
        # random motion
        v = np.random.random(N)
        av = np.random.random(N)
        action = np.c_[v, av]
        simulator.update(action)
