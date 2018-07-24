const float CATALYST_RADIUS = 0.4;
const float SUBSTRATE_RADIUS = 0.25;
const float LINK_INNER_BORDER = 0.31;
const float LINK_OUTER_BORDER = 0.39;
const float BOND_WIDTH = LINK_OUTER_BORDER - LINK_INNER_BORDER;

varying float v_particle_type;
varying vec2 v_is_bondding;
varying vec2 v_bondding_angles;
varying float v_size_scale;

vec2 rotate2d(vec2 p, float th)
{
	float s = sin(th);
	float c = cos(th);
	mat2 m = mat2(c, -s, s, c);
	return m * p;
}

void main()
{
	// fix coordinate for [-0.5, 0.5] by considering overlap
    vec2 p = gl_PointCoord * v_size_scale - v_size_scale/2;

    // draw particle
    if (v_particle_type == 0) {
        discard;
    } else if (v_particle_type == 2){
        if (length(p) < CATALYST_RADIUS) gl_FragColor = vec4(0.8,0.25,0.8,1);
        else discard;
    } else {
		if ((v_particle_type == 1 || v_particle_type == 4) && (length(p) < SUBSTRATE_RADIUS)) {
			gl_FragColor = vec4(0,0.8,0.8,1);
		} else if (v_particle_type == 3 || v_particle_type == 4) {
			if ((abs(p.x) >= LINK_INNER_BORDER || abs(p.y) >= LINK_INNER_BORDER) &&
            	 abs(p.x) <= LINK_OUTER_BORDER && abs(p.y) <= LINK_OUTER_BORDER) {
				gl_FragColor = vec4(0,0.3,1,1);
            } else if (abs(p.x) > LINK_OUTER_BORDER || abs(p.y) > LINK_OUTER_BORDER){
                // draw bond
				bool draw_bond_frag = false;
				for(int i = 0; i < 2; i++) {
					if(v_is_bondding[i] > 0) {
						vec2 line_xy = rotate2d(p, -v_bondding_angles[i]);
	                	if (line_xy.x > 0 && abs(line_xy.y) < BOND_WIDTH/2) {
	                    	gl_FragColor = vec4(0,0.3,1,1);
							draw_bond_frag = true;
						}
					}
				}
				if (!draw_bond_frag) {
					discard;
				}
            } else {
				discard;
			}
        } else {
			discard;
		}
    }
}
