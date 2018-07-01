import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('tkagg')

particle_shapes = None

def draw(ax, particles):
    global particle_shapes, bond_shapes
    if particle_shapes is None:
        particle_shapes = np.empty(particles.shape, dtype=object)
    for line in bond_shapes.values():
        line.remove()
    bond_shapes = {}
    for x in range(particles.shape[0]):
        for y in range(particles.shape[1]):
            p = particles[x,y]
            _draw_particle(ax, x, y, p['type'])
            for (bx, by) in p['bonds']:
                _draw_bond(ax, x, y, bx, by, particles.shape[0], particles.shape[1])


def _draw_particle(ax, x, y, particle_type):
    if particle_shapes[x, y] is not None:
        if isinstance(particle_shapes[x,y], list):
            particle_shapes[x,y][0].remove()
            particle_shapes[x,y][1].remove()
        else:
            particle_shapes[x, y].remove()

    if particle_type == 'HOLE':
        s = None
    elif particle_type == 'SUBSTRATE':
        s = plt.Circle((x, y), 0.25, facecolor='c')
        ax.add_patch(s)
    elif particle_type == 'CATALYST':
        s = plt.Circle((x, y), 0.4, facecolor='m')
        ax.add_patch(s)
    elif particle_type == 'LINK':
        s = plt.Rectangle([x - 0.35, y - 0.35], 0.7, 0.7, edgecolor='b', facecolor='w')
        ax.add_patch(s)
    elif particle_type == 'LINK_SUBSTRATE':
        s0 = plt.Rectangle([x - 0.35, y - 0.35], 0.7, 0.7, edgecolor='b', facecolor='w')
        ax.add_patch(s0)
        s1 = plt.Circle((x, y), 0.25, facecolor='c')
        ax.add_patch(s1)
        s = [s0, s1]
    particle_shapes[x, y] = s

bond_shapes = {}
def _draw_bond(ax, x0, y0, x1, y1, x_size, y_size):
    #print("draw", x0, y0, x1, y1)
    x0_n = x_size if (x0 == 0 and x1 == x_size-1) else x0
    y0_n = y_size if (y0 == 0 and y1 == y_size-1) else y0
    x1_n = x_size if (x1 == 0 and x0 == x_size-1) else x1
    y1_n = y_size if (y1 == 0 and y0 == y_size-1) else y1

    start_x = x0_n + 0.35 * (x1_n - x0_n)
    start_y = y0_n + 0.35 * (y1_n - y0_n)
    end_x = x1_n - 0.35 * (x1_n - x0_n)
    end_y = y1_n - 0.35 * (y1_n - y0_n)
    line = plt.Polygon([(start_x, start_y), (end_x, end_y)], color='b', lw=1.5)
    ax.add_patch(line)
    bond_shapes[(x0, y0, x1, y1)] = line

def clear_bond(ax, x0, y0, x1, y1):
    #print("clear", x0, y0, x1, y1)
    try:
        key = (x0, y0, x1, y1)
        if key in bond_shapes:
            bond_shapes[key].remove()
            bond_shapes.pop(key)
        else:
            key = (x1, y1, x0, y0)
            bond_shapes[key].remove()
            bond_shapes.pop(key)
    except KeyError:
        print(x0,y0,x1,y1)
        print(bond_shapes.keys())
        exit()


class SCLVisualizer_legacy(object):
    """docstring for SCLVisualizer."""
    def __init__(self, width=600, height=600):
        super(SCLVisualizer_legacy, self).__init__()
        #
        # Initialization
        #
        plt.figure(figsize=(8,8))
        self.axis = None

    def update(self, particles):
        if self.axis is None:
            self.axis = plt.axes(xlim=(-1,particles.shape[0]), ylim=(-1,particles.shape[1]), aspect='equal')
            self.axis.set_xticks([])
            self.axis.set_yticks([])
            self.axis.invert_yaxis()

        draw(self.axis, particles)
        plt.pause(0.001)

    def __bool__(self):
        return True


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
        vertex_shader = open(path.join(GLSL_PATH, 'scl_visualizer_vertex.glsl'), 'r').read()
        fragment_shader = open(path.join(GLSL_PATH, 'scl_visualizer_fragment.glsl'), 'r').read()
        self._render_program = gloo.Program(vertex_shader, fragment_shader)
        gloo.set_state(blend=True, blend_func=('src_alpha', 'one'))
        self._canvas.show()

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
        self._render_program['u_window_size'] = self._canvas.size
        self._render_program['u_particle_num'] = [col_num, row_num]

        self._canvas.update()
        app.process_events()

        #import time
        #time.sleep(0.5)
        #ipdb.set_trace()

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
    #v = SCLVisualizer(600, 600)
    v = SCLVisualizer(600, 600)
    while v:
        data = generate_random_data(32, 32)
        v.update(data)
