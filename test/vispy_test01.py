# pylint: disable=invalid-name, no-member, unused-argument
""" basic demo using shaders
http://ipython-books.github.io/featured-06/
"""

import numpy as np
from vispy import app, gloo

# In order to display a window, we need to create a Canvas.
c = app.Canvas(size=(800, 400), keys='interactive')

# When using vispy.gloo, we need to write shaders.
# These programs, written in a C-like language called GLSL,
# run on the GPU and give us full flexibility for our visualizations.
# Here, we create a trivial vertex shader that directly displays
# 2D data points (stored in the a_position variable) in the canvas
vertex = """
attribute vec2 a_position;
void main(void)
{
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""

# The other shader we need to create is the fragment shader.
# It lets us control the pixels' color.
fragment = """
void main()
{
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
"""

# Next, we create an OpenGL Program. This object contains the shaders
# and allows us to link the shader variables to Python/NumPy data.
program = gloo.Program(vert=vertex, frag=fragment)

# 1000x2
N = 1000
data = np.c_[
    np.linspace(-1, 1, N),
    np.random.uniform(-0.5, +0.5, N)]
print(data.shape)

# gloo needs 32bit
program['a_position'] = data.astype('float32')


@c.connect
def on_resize(event):
    """
    We create a callback function called when the window is being resized.
    Updating the OpenGL viewport lets us ensure that
    Vispy uses the entire canvas.
    """
    gloo.set_viewport(0, 0, *event.physical_size)


@c.connect
def on_draw(event):
    """
    We create a callback function called when the canvas needs to be refreshed
    This on_draw function renders the entire scene.
    """
    # First, we clear the window in white
    # (it is necessary to do that at every frame)
    gloo.set_clear_color((1.0, 1.0, 1.0, 1.0))
    gloo.clear()
    program.draw('line_strip')

# Finally, we show the canvas and we run the application.
c.show()
app.run()
