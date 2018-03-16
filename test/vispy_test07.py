import numpy as np
from vispy import gloo, app

VERT_SHADER = """
#version 120

attribute vec2 a_position;
//attribute vec2 a_texcoord;
void main()
{
    gl_Position = vec4(a_position, 0.0, 1.0);
    gl_PointSize = 30;
}
"""

FRAG_SHADER = """
void main()
{
    gl_FragColor = vec4(1,0,0,1);
}
"""

N = 10
data = np.zeros(N, [('a_position', np.float32, 2)])


class Canvas(app.Canvas):

    def __init__(self):
        app.Canvas.__init__(self, keys='interactive', size=(800, 600), position=(0,0))

        # Create program
        self._program = gloo.Program(VERT_SHADER, FRAG_SHADER)
        self._program.bind(gloo.VertexBuffer(data))

        #self._program['a_position'] = data
        data['a_position'][0] = [0,0]
        data['a_position'][1] = [0,0.5]
        data['a_position'][2] = [0.5,0]
        data['a_position'][3] = [0.5,0.5]
        data['a_position'][4] = [0.5,0.5]
        data['a_position'][5] = [-0.2,-0.2]
        data['a_position'][6] = [-0.2,-0.2]
        data['a_position'][7] = [-0.2,-0.5]
        data['a_position'][8] = [-0.5,-0.2]
        data['a_position'][9] = [-0.5,-0.5]


        #print(data['a_position'])
        #print(data)

        gloo.set_state(blend=True, clear_color='black', blend_func=('src_alpha', 'one'))

        #gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])

        #self._timer = app.Timer('auto', connect=self.update, start=True)

        self.show()

    def on_resize(self, event):
        #width, height = event.physical_size
        gloo.set_viewport(0, 0, *event.physical_size)
        #pass

    def on_draw(self, event):
        gloo.clear()
        self._program.draw('triangle_strip')
        #self._program.draw('points')


if __name__ == '__main__':
    c = Canvas()
    app.run()
