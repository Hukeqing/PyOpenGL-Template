#version 330 core

out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D texture0;
uniform sampler2D texture1;
uniform vec4 basecolor;
uniform float mix_value0;
// uniform vec4 lightColor=vec4(1, 1, 1, 1);

void main()
{
    FragColor = mix(texture(texture0, TexCoord), texture(texture1, TexCoord), mix_value0) * basecolor;
}