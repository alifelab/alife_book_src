from pyglet import window, text, app, resource, event, clock
from pyglet.gl import *

event_loop = app.EventLoop()

window = window.Window()
#image = resource.image("ball.png")

@window.event
def on_draw():
    window.clear()

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 0)
    glVertex2f(window.width, 0)
    glVertex2f(window.width, window.height)
    glEnd()


@event_loop.event
def on_window_close(window):
    event_loop.exit()
    return event.EVENT_HANDLED

def main():
    event_loop.run()

if __name__ == "__main__":
    main()
