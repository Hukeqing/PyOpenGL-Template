#version 330 core

out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;

uniform vec4 basecolor=vec4(1, 1, 1, 1);
uniform vec3 lightColor0=vec3(1, 1, 1);
uniform vec3 lightPos0=vec3(-10, 6, 10);

void main()
{
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor0;

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos0 - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor0;

    vec3 result = (ambient + diffuse) * vec3(basecolor.xyz);
    // vec3 result = ambient * vec3(basecolor.xyz);
    FragColor = vec4(result, basecolor.w);
    // FragColor = vec4(result, 1.0);
    // FragColor = texture(texture0, TexCoord) * basecolor;
}