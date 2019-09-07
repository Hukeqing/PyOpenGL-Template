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
    Texture textures[___set_texture_number];
};

struct TestureMaterial {
	vec3 diffuseVec3;
	vec3 specularVec3;
};

struct DirLight {
    vec3 direction;

    float ambient;
    float diffuse;
    float specular;
    vec3 color;
};

struct PointLight {
    vec3 position;

    float constant;
    float linear;
    float quadratic;

    float ambient;
    float diffuse;
    float specular;
    vec3 color;
};

struct SpotLight {
    vec3 position;
    vec3 direction;
    float cutOff;
    float outerCutOff;

    float constant;
    float linear;
    float quadratic;

    float ambient;
    float diffuse;
    float specular;
    vec3 color;
};

uniform Material material;
uniform vec3 viewPos;
TestureMaterial texture_material;

uniform int dirLight_number;
uniform DirLight dirLights[___set_max_dir_light_number];

uniform int pointLight_number;
uniform PointLight pointLights[___set_max_point_light_number];

uniform int spotLight_number;
uniform SpotLight spotLights[___set_max_spot_lights];

// function prototypes
vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir);

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir);

vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir);

void main() {
    // properties
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);
    if (material.useSampler > 0) {
        texture_material.diffuseVec3 = vec3(texture(material.diffuse, TexCoord));
        texture_material.specularVec3 = vec3(texture(material.specular, TexCoord));
    } else {
        texture_material.diffuseVec3 = vec3(1.0);
        texture_material.specularVec3 = vec3(1.0);
    }
    // ========================================================
    // lighting is set up in 3 phases: directional, point lights and an optional flashlight
    // For each phase, a calculate function is defined that calculates the corresponding color
    // per lamp. In the main() function we take all the calculated colors and sum them up for
    // this fragment's final color.
    // ========================================================
    // phase 1: directional lighting
    vec3 result = vec3(0, 0, 0);
    for (int i = 0; i < dirLight_number; i++)
        result += CalcDirLight(dirLights[i], norm, viewDir) * dirLights[i].color;
    // phase 2: point lights
    for (int i = 0; i < pointLight_number; i++)
        result += CalcPointLight(pointLights[i], norm, FragPos, viewDir) * pointLights[i].color;
    // phase 3: spot light
    for (int i = 0; i < spotLight_number; i++)
        result += CalcSpotLight(spotLights[i], norm, FragPos, viewDir) * spotLights[i].color;

    // texture mix
    vec4 texture_result = vec4(1.0);
    if (material.texture_number > 0) {
        texture_result = texture(material.textures[0].texture_index, TexCoord);
        for (int i = 1; i < material.texture_number; i++)
            texture_result = mix(texture_result, texture(material.textures[i].texture_index, TexCoord), material.textures[i].mix_value);
    }
    FragColor = vec4(result * vec3(material.color.xyz), material.color.w) * texture_result;
}

// calculates the color when using a directional light.
vec3 CalcDirLight(DirLight light, vec3 normal, vec3 viewDir) {
    vec3 lightDir = normalize(-light.direction);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    // combine results
    vec3 ambient = light.ambient * texture_material.diffuseVec3;
    vec3 diffuse = light.diffuse * diff * texture_material.diffuseVec3;
    vec3 specular = light.specular * spec * texture_material.specularVec3;
    return (ambient + diffuse + specular);
}

// calculates the color when using a point light.
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir) {
    vec3 lightDir = normalize(light.position - fragPos);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    // attenuation
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));
    // combine results
    vec3 ambient = light.ambient * texture_material.diffuseVec3;
    vec3 diffuse = light.diffuse * diff * texture_material.diffuseVec3;
    vec3 specular = light.specular * spec * texture_material.specularVec3;
    ambient *= attenuation;
    diffuse *= attenuation;
    specular *= attenuation;
    return (ambient + diffuse + specular);
}

// calculates the color when using a spot light.
vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDir) {
    vec3 lightDir = normalize(light.position - fragPos);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    // attenuation
    float distance = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));
    // spotlight intensity
    float theta = dot(lightDir, normalize(-light.direction));
    float epsilon = light.cutOff - light.outerCutOff;
    float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0);
    // combine results
    vec3 ambient = light.ambient * texture_material.diffuseVec3;
    vec3 diffuse = light.diffuse * diff * texture_material.diffuseVec3;
    vec3 specular = light.specular * spec * texture_material.specularVec3;
    ambient *= attenuation * intensity;
    diffuse *= attenuation * intensity;
    specular *= attenuation * intensity;
    return (ambient + diffuse + specular);
}