import numpy as np
import vispy
from vispy import gloo, app

vispy.use('Glfw')

VERTEX_SHADER = """
    attribute vec2 a_position;
    attribute vec2 a_texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(a_position, 0.0, 1.0);
        v_texcoord = a_texcoord;
    }
"""

FRAGMENT_SHADER = """
    uniform sampler2D u_texture;
    varying vec2 v_texcoord;
    void main()
    {
        float r = texture2D(u_texture, v_texcoord).r;
        gl_FragColor = vec4(r,r,r,1);
    }
"""

class MatrixVisualizer(object):
    """docstring for MatrixVisualizer."""
    def __init__(self, width, height):
        self._canvas = app.Canvas(size=(width, height), position=(0,0), title="ALife book "+self.__class__.__name__)
        self._canvas.events.draw.connect(self.on_draw)
        self._render_program = gloo.Program(VERTEX_SHADER, FRAGMENT_SHADER)
        self._render_program['a_position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
        self._render_program['a_texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
        self._render_program['u_texture'] = np.zeros((1,1)).astype(np.uint8)
        self._canvas.show()

    def on_draw(self, event):
        gloo.clear()
        self._render_program.draw(gloo.gl.GL_TRIANGLE_STRIP)

    def update(self, matrix):
        matrix[matrix<0] = 0
        matrix[matrix>=256] = 255
        self._render_program['u_texture'] = matrix.astype(np.uint8)
        self._canvas.update()
        app.process_events()

    def __bool__(self):
        return not self._canvas._closed

if __name__ == '__main__':
    v = MatrixVisualizer(600, 600)
    data = np.repeat(np.arange(0, 256, dtype=np.uint8)[np.newaxis,:], 3, axis=0)
    while v:
        data = np.roll(data, 1, axis=1)
        v.update(data)
