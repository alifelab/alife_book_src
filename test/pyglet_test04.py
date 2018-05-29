import pyglet
import numpy as np

window = pyglet.window.Window()
#image = pyglet.resource.image('kitten.png')
img_data =  ( np.random.random((300,300)) * 255 ).astype('uint8')
image = pyglet.image.ImageData(300,300,'L',img_data)

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()
