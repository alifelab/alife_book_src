# -*- coding: utf-8 -*-
from os import path
import numpy as np
from vispy import app, gloo, visuals
from vispy.visuals import transforms
from vispy.util.transforms import perspective
import ipdb

GLSL_PATH = path.dirname(path.abspath(__file__))

DEBUG_ENV = False

def mnd(_x, _mu, _sig):
    x = np.matrix(_x)
    mu = np.matrix(_mu)
    sig = np.matrix(_sig)
    a = np.sqrt(np.linalg.det(sig)*(2*np.pi)**sig.ndim)
    b = np.linalg.det(-0.5*(x-mu)*sig.I*(x-mu).T)
    return np.exp(b)/a



class AntSimulator(app.Canvas):

    def __init__(self, N):
        super(AntSimulator, self).__init__(title='Title', size=(600, 600), resizable=False, position=(0, 0), keys='interactive')

        self._N = N
        self._potential_grid_size = np.array([128, 128])
        #self._potential_grid_size = np.array([20, 20])

        self._setup_initstate()


        vert = open(path.join(GLSL_PATH, 'color_map_vert.glsl'), 'r').read()
        frag = open(path.join(GLSL_PATH, 'color_map_frag.glsl'), 'r').read()
        self.potential_render = gloo.Program(vert, frag)
        self.potential_render["a_position"] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.potential_render["a_texcoord"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.potential_render["u_texture"] = self._get_current_potential()
        self.potential_render["u_texture"].interpolation = 'nearest'

        self.agents_visuals = []
        self.agents_head_visuals = []
        #for pos, vel in zip(self._agents_pos, self._agents_vel):
        for pos in self._agents_pos:
            v = visuals.EllipseVisual((pos[0], pos[1], 0), radius=self._agents_radius,
                                      color=(0, 0, 0, 0), border_color="red", border_width=3)
            v.transform = transforms.NullTransform()
            self.agents_visuals.append(v)
            #visuals.LineVisual([self._agents_pos, )
            #self.agents_head_visuals.append(v)

        #gloo.set_state('translucent', clear_color='white')
        gloo.set_state(clear_color='black', blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

        #self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.show()
        #self.app.run()

    def _setup_initstate(self, seed=12345):
        np.random.seed(seed)
        self._potential = np.zeros((self._potential_grid_size[1], self._potential_grid_size[1])).astype(np.float32)
        #for i in range(50):
        for i in range(8):
            #gain = 1000
            mean = np.random.random(2)
            cov = np.eye(2) * np.random.rand() * 0.05
            #sample = np.random.multivariate_normal(mean, cov, gain)
            #d, _, _ = np.histogram2d(sample[:,0], sample[:,1], bins=self._potential_grid_size, range=[[0,1],[0,1]])
            d = np.array([[mnd([x,y], mean, cov) for x in np.linspace(0, 1, self._potential_grid_size[0], endpoint=False)] for y in np.linspace(0, 1, self._potential_grid_size[0], endpoint=False)])
            #print(d)
            self._potential += d

        self._potential += np.random.random(self._potential.shape)
        self._potential /= np.max(self._potential)
        self.reset()

    def reset(self, seed=1234):
        np.random.seed(seed)
        self._potential_neg = np.zeros(self._potential.shape).astype(np.float32)
        #print(self._potential.shape, self._potential_neg.shape, self._get_current_potential().shape)

        #self._potential = np.random.random((self._potential_grid_size[1], self._potential_grid_size[1])).astype(np.float32)
        #self._potential = np.ones((self._potential_grid_size[1], self._potential_grid_size[1])).astype(np.float32) * 0.5

        # debug environment
        if DEBUG_ENV:
            self._potential = np.zeros((self._potential_grid_size[1], self._potential_grid_size[1])).astype(np.float32)
            self._potential[100:, 100:] = 1
            self._potential[:100, :100] = 0.5

        self._agents_pos = np.random.random((self._N, 2)).astype(np.float32)
        self._agents_th = np.random.random(self._N).astype(np.float32) * np.pi * 2
        self._agents_vel = np.ones(self._N).astype(np.float32) * 0.001
        self._agents_ang_vel = (np.random.random(self._N).astype(np.float32) * 0.1 - 0.05) * np.pi
        self._agents_radius = 0.05
        self._sensor_angle = np.linspace(0, 2*np.pi, 7, endpoint=False)
        self._agents_fitness = np.zeros(self._N)

        return self.__get_observations()

    def on_timer(self, event):
        self.update()

    def _get_current_potential(self):
        return self._potential - self._potential_neg

    def on_draw(self, event):
        gloo.clear()
        self.potential_render["u_texture"] = self._get_current_potential()
        self.potential_render.draw('triangle_strip')
        #for v, pos, vel in zip(self.agents_visuals, self._agents_pos, self._agents_vel):
        for v, pos in zip(self.agents_visuals, self._agents_pos):
            v.center = pos[0]*2-1, pos[1]*2-1, 0
            v.draw()

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *self.physical_size)

    def __get_observations(self):
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
                obs[ai, si] = self._get_current_potential()[yi, xi]
                #ipdb.set_trace()
        return obs


    def step(self, action):
        # v_dot = action[:,0]
        # av_dot = action[:,1]
        # self._agents_vel += v_dot
        # self._agents_ang_vel += av_dot
        # self._agents_pos += (self._agents_vel * [np.cos(self._agents_th), np.sin(self._agents_th)]).T
        # self._agents_th += self._agents_ang_vel

        # action take 0-1 value
        v = action[:,0] * 0.0005 + 0.0005
        av = (action[:,1] - 0.5) * 2 * np.pi * 0.05
        self._agents_pos += (v * [np.cos(self._agents_th), np.sin(self._agents_th)]).T
        self._agents_th += av

        self._agents_pos %= 1.0
        self._agents_th %= (2.0 * np.pi)

        grid_idx = (self._agents_pos * self._potential_grid_size).astype(int)
        self._agents_fitness += [self._get_current_potential()[y,x] for x,y in grid_idx]
        for x, y in grid_idx:
            self._potential_neg[y,x] = self._potential[y,x]

        self.update()
        self.app.process_events()

        return self.__get_observations()

    def get_fitness(self):
        return self._agents_fitness



def action(observation):
    N = len(observation)
    # go forward
    # v = np.ones(N)
    # av = np.ones(N) * 0.5
    # random motion
    v = np.random.random(N)
    av = np.random.random(N)
    act = np.c_[v, av]
    return act


if __name__ == '__main__':
    sim = AntSimulator(1)
    obs = sim.reset()
    while True:
        act = action(obs)
        obs = sim.step(act)
