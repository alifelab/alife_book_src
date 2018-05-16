import sys
import numpy as np
import pygame
from pygame.locals import *



class BinaryMatrixVisualizer(object):
    """docstring for BinaryMatrixVisualizer."""
    def __init__(self, size):
        super(BinaryMatrixVisualizer, self).__init__()
        pygame.init()
        self.width = size[0]
        self.height = size[1]
        self.screen = pygame.display.set_mode(size)
        #pygame.display.set_caption("title")

    def update(self, matrix):
        img = pygame.surfarray.make_surface(matrix.T*255)
        self.screen.blit(img, (0,0,400,400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
