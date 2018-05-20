from glumpy import app

window = app.Window()

@window.event
def on_draw(dt):
    window.clear()

app.run(interactive=True)
print("Try to type 'window.color = (1,1,1,1)' in the console")
