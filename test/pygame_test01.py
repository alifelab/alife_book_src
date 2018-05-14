#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"図形の描画")

while True:
    screen.fill((0,0,0))

    # 図形を描画
    # 黄の矩形
    pygame.draw.rect(screen, (255,255,0), Rect(10,10,300,200))
    # 赤の円
    pygame.draw.circle(screen, (255,0,0), (320,240), 100)
    # 紫の楕円
    pygame.draw.ellipse(screen, (255,0,255), (400,300,200,100))
    # 白い線
    pygame.draw.line(screen, (255,255,255), (0,0), (640,480))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
