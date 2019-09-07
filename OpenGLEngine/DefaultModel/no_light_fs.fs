#version 330 core

in vec2 TexCoord;
in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

struct Texture {
    sampler2D texture_index;
    float mix_value;
};

struct Material {
    vec4 color;
    float shininess;
    sampler2D diffuse;
    sampler2D specular;
    int useSampler;

    int texture_number;
    Texture textures[14];
};

struct TestureMaterial {
	vec3 diffuseVec3;
	vec3 specularVec3;
};

uniform Material material;
TestureMaterial texture_material;

void main() {
    vec3 result = vec3(1, 1, 1);
    // texture mix
    vec4 texture_result = vec4(1.0);
    if (material.texture_number > 0) {
        texture_result = texture(material.textures[0].texture_index, TexCoord);
        for (int i = 1; i < material.texture_number; i++)
            texture_result = mix(texture_result, texture(material.textures[i].texture_index, TexCoord), material.textures[i].mix_value);
    }
    FragColor = vec4(result * vec3(material.color.xyz), material.color.w) * texture_result;
}
