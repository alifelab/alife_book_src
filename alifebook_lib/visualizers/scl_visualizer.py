from os import path
import numpy as np
from vispy import gloo, app

GLSL_PATH = path.join(path.dirname(path.abspath(__file__)), 'glsl')

class SCLVisualizer(object):
    """docstring for MatrixVisualizer."""

    PARTICLE_TYPE_INDEX_MAP = {'HOLE':0, 'SUBSTRATE':1, 'CATALYST':2, 'LINK':3, 'LINK_SUBSTRATE':4}

    def __init__(self, width=600, height=600):
        self._canvas = app.Canvas(size=(width, height), position=(0,0), keys='interactive', title="ALife book "+self.__class__.__name__)
        self._canvas.events.draw.connect(self._on_draw)
        self._canvas.events.resize.connect(self._on_resize)
        vertex_shader = open(path.join(GLSL_PATH, 'scl_visualizer_vertex.glsl'), 'r').read()
        fragment_shader = open(path.join(GLSL_PATH, 'scl_visualizer_fragment.glsl'), 'r').read()
        self._render_program = gloo.Program(vertex_shader, fragment_shader)
        gloo.set_state('translucent', clear_color='white')
        self._canvas.show()
        gloo.set_viewport(0, 0, *self._canvas.physical_size)

    def _on_resize(self, event):
        gloo.set_viewport(0, 0, *self._canvas.physical_size)

    def _on_draw(self, event):
        gloo.clear()
        self._render_program.draw(gloo.gl.GL_POINTS)

    def update(self, particle_data):
        if type(particle_data) is not np.ndarray:
            particle_data = np.array(particle_data)
        row_num, col_num = particle_data.shape
        # convert particle data format to shader data
        # check shader program for detail.
        shader_data = np.empty((particle_data.shape[0], particle_data.shape[1], 7), dtype=int)
        for i in range(row_num):
            for j in range(col_num):
                p = particle_data[i,j]
                shader_data[i,j,0] = self.PARTICLE_TYPE_INDEX_MAP[p['type']]
                shader_data[i,j,1] = j
                shader_data[i,j,2] = (row_num - i) - 1
                for k in range(2):
                    try:
                        pb = p['bonds'][k]
                        shader_data[i,j,3+k*2] = pb[1]
                        shader_data[i,j,4+k*2] = (row_num - pb[0]) - 1
                    except IndexError:
                        shader_data[i,j,[3+k*2,4+k*2]] = -1
        shader_data2 = shader_data.reshape((-1, 7))

        self._render_program['a_particle_type'] = shader_data2[:,0].astype(np.float32)
        self._render_program['a_position'] = shader_data2[:,1:3].astype(np.float32)
        self._render_program['a_bondding_positions'] = shader_data2[:,3:7].astype(np.float32)
        self._render_program['u_window_size'] = self._canvas.physical_size
        self._render_program['u_particle_num'] = [col_num, row_num]

        self._canvas.update()
        app.process_events()

    def __bool__(self):
        return not self._canvas._closed


def generate_random_data(row_num, col_num):
    data = np.empty((row_num, col_num), dtype=object)
    for i in range(row_num):
        for j in range(col_num):
            type = np.random.choice(('HOLE', 'SUBSTRATE', 'CATALYST', 'LINK', 'LINK_SUBSTRATE'))
            data[i,j] = {'type': type, 'bonds': []}

    neighbor_index = [[-1,-1], [0,-1], [1,-1], [-1,0], [1,0], [-1,1], [0,1], [1,1]]
    for i in range(row_num):
        for j in range(col_num):
            i1 = np.random.randint(row_num)
            j1 = np.random.randint(col_num)
            ni, nj = neighbor_index[np.random.randint(len(neighbor_index))]
            i2 = (i1 + ni) % row_num
            j2 = (j1 + nj) % col_num
            if data[i1, j1]['type'] in ('LINK', 'LINK_SUBSTRATE') and \
               data[i2, j2]['type'] in ('LINK', 'LINK_SUBSTRATE') and \
               np.random.rand() < 0.5:
                data[i1, j1]['bonds'].append([i2, j2])
                data[i2, j2]['bonds'].append([i1, j1])
    return data


if __name__ == '__main__':
    v = SCLVisualizer(600, 600)
    while v:
        data = generate_random_data(32, 32)
        v.update(data)
