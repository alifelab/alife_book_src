import sys
import numpy as np
import pygame
from pygame.locals import *



class MatrixVisualizer(object):
    """docstring for MatrixVisualizer."""
    def __init__(self, size):
        super(MatrixVisualizer, self).__init__()
        pygame.init()
        self.width = size[0]
        self.height = size[1]
        self.screen = pygame.display.set_mode(size)
        #pygame.display.set_caption("title")

    def update(self, matrix):
        img = pygame.surfarray.make_surface(matrix.T)
        if self.screen.get_size() != img.get_size():
            img = pygame.transform.scale(img, self.screen.get_size())
        self.screen.blit(img, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
