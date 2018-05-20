import numpy as np
from glumpy import app, gloo, gl

VERT = """
    attribute vec2 a_position;
    attribute vec2 a_texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(a_position, 0.0, 1.0);
        v_texcoord = a_texcoord;
    }
"""

FRAG = """
    uniform sampler2D u_texture;
    varying vec2 v_texcoord;
    void main()
    {
        float r = texture2D(u_texture, v_texcoord).r;
        gl_FragColor = vec4(r,r,r,1);
    }
"""

class Visualizer(object):
    """docstring for Visualizer."""
    def __init__(self, width, height):
        super(Visualizer, self).__init__()
        self._window = app.Window(width, height, title="ALife book "+self.__class__.__name__)

        @self._window.event
        def on_draw(dt):
            self._window.clear()
            self._render_program.draw(gl.GL_TRIANGLE_STRIP)

        self._render_program = gloo.Program(VERT, FRAG)
        self._render_program['a_position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
        self._render_program['a_texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
        #self._render_program['u_texture'] = np.zeros((1,1)).astype(np.uint8)

    def update(self, matrix):
        self._render_program['u_texture'] = matrix
        backend = app.__backend__
        if not hasattr(self, 'clock'):
            self.clock = app.__init__(backend=backend)
        count = backend.process(self.clock.tick())
        return(bool(count))

if __name__ == '__main__':
    v = Visualizer(600, 600)
    data = np.repeat(np.arange(0, 256, dtype=np.uint8)[np.newaxis,:], 3, axis=0)
    while v.update(data):
        data = np.roll(data, 1, axis=1)
