import numpy as np
import vispy
from vispy.scene import SceneCanvas
from vispy.scene import visuals

class SwarmVisualizer(object):
    """docstring for SwarmVisualizer."""
    ARROW_SIZE = 20

    def __init__(self, width=600, height=600):
        self._canvas = SceneCanvas(size=(width, height), position=(0,0), keys='interactive', title="ALife book "+self.__class__.__name__)
        self._view = self._canvas.central_widget.add_view()
        #self._view.camera = 'arcball'
        self._view.camera = 'turntable'
        self._axis = visuals.XYZAxis(parent=self._view.scene)
        self._arrows = None
        self._markers = None
        self._canvas.show()

    def update(self, position, direction):
        assert position.ndim is 2 and position.shape[1] in (2,3)
        assert direction.ndim is 2 and direction.shape[1] in (2,3)
        assert position.shape[0] == direction.shape[0]
        if self._arrows is None:
            self._arrows = visuals.Arrow(arrow_size=self.ARROW_SIZE, arrow_type='triangle_30', parent=self._view.scene)
        # arrow_coordinate[0::2] is position of arrow and
        # arrow_coordinate[1::2] is direction of tail (length is ignored)
        arrow_coordinate = np.repeat(position, 2, axis=0)
        arrow_coordinate[::2] -=  direction
        self._arrows.set_data(arrows=arrow_coordinate.reshape((-1, 6)))
        self._canvas.update()
        vispy.app.process_events()

    def set_markers(self, position):
        assert position.ndim is 2 and position.shape[-1] in (2,3)
        if self._markers is None:
            self._markers = visuals.Markers(parent=self._view.scene)
        self._markers.set_data(position, face_color=(1,0,0), size=20)
        self._canvas.update()
        vispy.app.process_events()

    def __bool__(self):
        return not self._canvas._closed


if __name__ == '__main__':
    N = 1000
    v = SwarmVisualizer()
    pos = np.random.normal(size=(N, 3), scale=0.2)
    vel = np.random.normal(size=(N, 3), scale=0.2) * 0.001
    v.set_markers(np.array([[0,0,0]]))
    while v:
        vel -= pos * 0.00001
        pos +=  vel
        v.update(pos, vel)
