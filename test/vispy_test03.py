# -*- coding: utf-8 -*-
import numpy as np
from vispy import app, gloo
from vispy.util.transforms import perspective


VERT_SHADER = """
attribute vec2 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    v_texcoord = texcoord;
}
"""

FRAG_SHADER = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    float v;
    v = texture2D(texture, v_texcoord).r;
    gl_FragColor = vec4(v, v, v, 1);
}
"""

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, title='Title', size=(512, 512), keys='interactive')

        self._field_width = 800
        self._field_height = 600
        self._potential = np.random.random((self._field_height, self._field_width)).astype(np.float32)

        self.render = gloo.Program(VERT_SHADER, FRAG_SHADER, 4)
        self.render["position"] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.render["texcoord"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.render["texture"] = self._potential
        self.render["texture"].interpolation = 'nearest'
        #self.render["texture"].interpolation = 'linear'

        gloo.set_state('translucent', clear_color='white')
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.show()


    def on_timer(self, event):
        self._potential = np.random.random((self._field_height, self._field_width)).astype(np.float32)
        self.render["texture"] = self._potential
        self.update()


    def on_draw(self, event):
        gloo.clear(color=True)
        self.render.draw('triangle_strip')


    def on_resize(self, event):
        gloo.set_viewport(0, 0, *self.physical_size)


if __name__ == '__main__':
    canvas = Canvas()
    app.run()
