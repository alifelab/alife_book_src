from os import path
import numpy as np
from .matrix_visualizer import MatrixVisualizer

class ArrayVisualizer(MatrixVisualizer):
    """docstring for ArrayVisualizer."""
    def __init__(self, width=600, height=600, history_size=600, value_range_min=0, value_range_max=1):
        super(ArrayVisualizer, self).__init__(width, height, value_range_min=value_range_min, value_range_max=value_range_max)
        self.history_size = history_size
        self.time_index = 0
        self.matrix = None

    def update(self, array):
        if self.matrix is None:
            self.matrix = np.ones((self.history_size, len(array))) * self.value_range[0]
        assert len(array) == self.matrix.shape[1]
        self.matrix[self.time_index,:] = array
        self.time_index = (self.time_index + 1) % self.history_size
        super().update(self.matrix)

if __name__ == '__main__':
    v = ArrayVisualizer(600, 600)
    while v:
        data = np.random.random(600)
        v.update(data)
