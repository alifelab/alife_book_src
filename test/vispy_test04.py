# -*- coding: utf-8 -*-
from os import path
import numpy as np
from vispy import app, gloo
from vispy.util.transforms import perspective


GLSL_PATH = path.dirname(path.abspath(__file__))

class Canvas(app.Canvas):

    def __init__(self):
        super(Canvas, self).__init__(title='Title', size=(600, 600), keys='interactive')

        vert = open(path.join(GLSL_PATH, 'color_map_vert.glsl'), 'r').read()
        frag = open(path.join(GLSL_PATH, 'color_map_frag.glsl'), 'r').read()
        self.potential_render = gloo.Program(vert, frag)
        self.potential_render["a_position"] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.potential_render["a_texcoord"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.potential_render["u_texture"] = []
        self.potential_render["u_texture"].interpolation = 'nearest'

        vert = open(path.join(GLSL_PATH, 'agents_vert.glsl'), 'r').read()
        frag = open(path.join(GLSL_PATH, 'agents_frag.glsl'), 'r').read()
        self.agents_render = gloo.Program(vert, frag)
        self.agents_render["u_radius"] = 25
        self.agents_render["u_linewidth"] = 3

        #gloo.set_state('translucent', clear_color='white')
        gloo.set_state(clear_color='black', blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

        #self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.show()


    def set_potential(self, potential):
        self.potential_render["u_texture"] = potential


    def set_agents_state(self, agents_pos, agents_vel):
        self.agents_render["a_position"] = agents_pos
        self.agents_render["a_orientation"] = agents_vel


    def on_timer(self, event):
        self._potential = np.random.random((self._field_height, self._field_width)).astype(np.float32)
        self.update()


    def on_draw(self, event):
        gloo.clear()
        #self.potential_render["u_texture"] = self._potential
        self.potential_render.draw('triangle_strip')
        #self.agents_render["a_position"] = self._agents_pos
        #self.agents_render["a_orientation"] = self._agents_vel
        self.agents_render.draw('points')


    def on_resize(self, event):
        gloo.set_viewport(0, 0, *self.physical_size)



class AntSimulator(object):

    def __init__(self, N):
        super(AntSimulator, self).__init__()
        self._N = N

        self._field_width = 200
        self._field_height = 200
        self._field_size = np.array([200, 200])
        self._potential = np.random.random((self._field_height, self._field_width)).astype(np.float32)
        self._agents_pos = np.random.random((self._N, 2)).astype(np.float32) * 2 - 1
        self._agents_vel = np.random.random((self._N, 2)).astype(np.float32) * 0.1 - 0.05

        self._app_canvas = Canvas()
        self._app_canvas.set_potential(self._potential)
        self._app_canvas.set_agents_state(self._agents_pos, self._agents_vel)

        self._app_canvas.app.run()

    def step(self, arg):
        self._potential = np.roll(self._potential, 1)
        self._agents_pos += self._agents_vel
        self._agents_pos += (self._agents_pos + self._field_size) % self._field_size


if __name__ == '__main__':
    c = AntSimulator(10)
    print("test")
