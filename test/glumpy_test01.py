from glumpy import app, gloo, gl

window = app.Window()

vertex = """
         attribute vec2 position;
         void main()
         {
             gl_Position = vec4(position, 0.0, 1.0);
         } """

fragment = """
           uniform vec4 color;
           void main() {
               gl_FragColor = color;
           } """

quad = gloo.Program(vertex, fragment, count=4)

quad['position'] = [(-0.5, -0.5),
                    (-0.5, +0.5),
                    (+0.5, -0.5),
                    (+0.5, +0.5)]
quad['color'] = 1,0,0,1  # red

@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)

app.run()
