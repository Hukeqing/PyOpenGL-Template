#version 330 core

out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D texture0;
uniform vec4 basecolor;

void main()
{
    FragColor = texture(texture0, TexCoord) * basecolor;
}