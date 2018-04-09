#version 330 core
uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;
uniform vec3 color;
uniform vec3 light;

layout(location = 0) in vec3 position_in;
layout(location = 1) in vec3 normals_in;

out vec3 position_out;
out vec3 colors_out;
out vec3 normals;
out vec3 light_out;
out mat3 model_out;
void main() {
    model_out = mat3(model);
    gl_Position = projection * view * model * vec4(position_in, 1);
    colors_out = color;
    normals = normals_in;
    light_out = light;
}
