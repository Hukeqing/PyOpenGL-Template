#version 330 core

out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D texture0;
uniform vec4 basecolor;
// uniform vec4 lightColor=vec4(1, 1, 1, 1);

void main()
{
    // FragColor = texture(texture0, TexCoord) * basecolor * lightColor;
    FragColor = texture(texture0, TexCoord) * basecolor;
    // FragColor = basecolor;
}