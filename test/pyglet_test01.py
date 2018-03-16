from pyglet.gl import *
from pyglet import image
import numpy as np
#import time
# Direct OpenGL commands to this window.
#window = pyglet.window.Window()
width = 600
height = 600
display = None
window = pyglet.window.Window(width=width, height=height, display=display)

N = 1000

pos = np.random.random((N, 2)) + 2 - 1
ang = np.random.random(N) * np.pi * 2

#while True:
for i in range(100):
    #glClearColor(1,1,1,1)
    window.clear()
    window.switch_to()
    window.dispatch_events()


    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 0)
    glVertex2f(window.width, 0)
    glVertex2f(window.width, window.height)
    glEnd()

    d = np.random.random((300,300))
    i = image.ImageData(300,300,'Gray',d)
    i.blit(0, 0, 0)


    window.flip()

    #print("test")
    #ime.sleep(5)
    print(i)
