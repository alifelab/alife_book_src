print("test")

class BinaryMatrixVisualizer(object):
    """docstring for BinaryMatrixVisualizer."""
    def __init__(self, matrix):
        super(BinaryMatrixVisualizer, self).__init__()
        self.matrix = matrix
        pygame.init()
        screen = pygame.display.set_mode(matrix.shape)

    def update(self):
        print(self.matrix[0,0])
