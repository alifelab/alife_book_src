import time
from vispy import app


for backend in ('pyglet', 'glfw', 'qt'):
    n_check = 3
    a = app.Application()
    a.use(backend)
    sz = (100, 100)
    c0, c1 = app.Canvas(app=a, size=sz), app.Canvas(app=a, size=sz)
    count = [0, 0]

    @c0.events.paint.connect
    def paint(event):
        global count1
        count[0] += 1
        print('  0 update')
        a.quit() if count[0] >= n_check else c0.update()

    @c1.events.paint.connect
    def paint(event):
        global count2
        count[1] += 1
        print('  1 update')
        a.quit() if count[1] >= n_check else c1.update()

    timeout = time.time() + 1.0
    print('start:')
    while count[0] < n_check and time.time() < timeout:
        a.process_events()
    print('stop: %s\n' % count)
    #assert counts[0] == n_check
    #assert counts[1] == -2 * n_check
    c0.close()
    c1.close()
