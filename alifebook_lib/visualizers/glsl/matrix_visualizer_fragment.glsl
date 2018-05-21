uniform sampler2D u_texture;
varying vec2 v_texcoord;
void main()
{
    float r = texture2D(u_texture, v_texcoord).r;
    gl_FragColor = vec4(r,r,r,1);
}
