#version 330 core

out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoord;

uniform sampler2D texture0;
uniform sampler2D texture1;
uniform float mix_value0;

uniform vec4 basecolor;

uniform vec4 lightColor0;
uniform vec3 lightPos0;

void main()
{
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * vec3(lightColor0.xyz);

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos0 - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * vec3(lightColor0.xyz);

    vec3 result = (ambient + diffuse) * vec3(basecolor.xyz);
    FragColor = mix(texture(texture0, TexCoord), texture(texture1, TexCoord), mix_value0) * vec4(result, basecolor.w);
}