#version 330 core

out vec4 FragColor;

in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D texture0;

void main()
{
    FragColor = texture(texture0, TexCoord) * vec4(ourColor, 1.0);
    // FragColor = texture(texture0, TexCoord);
}