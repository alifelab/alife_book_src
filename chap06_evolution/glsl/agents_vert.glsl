#version 120
attribute vec2 a_position;
attribute vec2 a_orientation;
varying float v_theta;
uniform float u_radius;
uniform float u_linewidth;

void main (void)
{
    v_theta = atan(a_orientation.y, a_orientation.x);
    gl_Position = vec4(a_position, 0.0, 1.0);
    gl_PointSize = u_radius*2 + u_linewidth;
}
