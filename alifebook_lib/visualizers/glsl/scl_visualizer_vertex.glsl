/*
 a_position:
    position index of this particle_data
 a_particle_type:
    particle type
    0: HOLE
    1: SUBSTRATE
    2: CATALYST
    3: LINK
    4: LINK_SUBSTRATE
 a_bondding_positions:
    position of bonding target particles.
    negative means no bondding
 */
attribute vec2 a_position;
attribute float a_particle_type;
attribute vec4 a_bondding_positions;

uniform vec2 u_window_size;
uniform vec2 u_particle_num;

varying float v_particle_type;
varying vec2 v_is_bondding;
varying vec2 v_bondding_angles;
varying float v_size_scale;

float PI = 3.141592653589793;

float atan2(in float y, in float x)
{
    return x == 0.0 ? sign(y)*PI/2 : atan(y, x);
}

void main()
{
    vec2 grid_size = u_window_size / u_particle_num;
    vec2 xy = 2 * a_position / u_particle_num - 1 + 1 / u_particle_num;
    if (grid_size.x > grid_size.y) {
        gl_PointSize = grid_size.y;
        gl_Position = vec4(xy.x * grid_size.y / grid_size.x, xy.y, 0.0, 1.0);
    } else {
        gl_PointSize = grid_size.x;
        gl_Position = vec4(xy.x, xy.y * grid_size.x / grid_size.y, 0.0, 1.0);
    }
    v_size_scale = 1.1;
    gl_PointSize = gl_PointSize * v_size_scale; // make a little bigger for bond opperlap
    v_particle_type = a_particle_type;
    for(int i = 0; i < 2; i++) {
        vec2 bxy = vec2(a_bondding_positions[i*2+0], a_bondding_positions[i*2+1]);
        if (bxy.x < 0 && bxy.y < 0) {
            v_is_bondding[i] = -1;
        } else {
            vec2 dxy = bxy - a_position;
            // periodic boundary condition
            if(abs(dxy.x) > 1.5) {
                dxy.x += a_position.x > bxy.x ? u_particle_num.x : -u_particle_num.x;
            }
            if(abs(dxy.y) > 1.5) {
                dxy.y += a_position.y > bxy.y ? u_particle_num.y : -u_particle_num.y;
            }
            v_bondding_angles[i] = atan2(dxy.y, dxy.x);
            v_is_bondding[i] = 1;
        }
    }
}
