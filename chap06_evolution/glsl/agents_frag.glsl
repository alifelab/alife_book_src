#version 120
varying float v_theta;
uniform float u_radius;
uniform float u_linewidth;
varying vec2 v_color;

vec2 rotate2d(vec2 v, float a) {
	float s = sin(a);
	float c = cos(a);
	mat2 m = mat2(c, -s, s, c);
	return m * v;
}

void main(){
    // vec2 xy = (gl_PointCoord.xy - vec2(0.5)) * 2 * (u_radius + u_linewidth/2);
    // float r = length(xy);
    //
    // if( r < u_radius - u_linewidth/2 ) {
    //     gl_FragColor = vec4(0, 0, 0, 0);
    // } else if( r < u_radius + u_linewidth/2 ) {
    //     gl_FragColor = vec4(1, 0, 0, 1);
    // } else {
    //     gl_FragColor = vec4(0, 0, 0, 0);
    // }
    //
    // vec2 xy_r = rotate2d(xy, -v_theta);
    // if(xy_r.x > 0 && xy_r.x < u_radius && abs(xy_r.y) < u_linewidth/2)
    // {
    //     gl_FragColor = vec4(1, 0, 0, 1);
    // }
	// gl_FragColor = vec4(1, 0, 0, 1);
	gl_FragColor = v_color;
}
