#!/usr/bin/env python3
"""
GLSL Vertex and Fragment Shaders
"""

COLOR_VERT = """#version 330 core
uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

layout(location = 0) in vec3 position_in;
layout(location = 1) in vec3 colors_in;

out vec3 position_out;
out vec3 colors_out;
void main() {
    gl_Position = projection * view * model * vec4(position_in, 1);
    position_out = position_in;
    colors_out = colors_in;
}"""

COLOR_FRAG_MULTIPLE = """#version 330 core
uniform vec3 color;
out vec4 outColor;
in vec3 position_out;
in vec3 colors_out;
void main() {
    outColor = vec4(colors_out, 1);
}"""

COLOR_FRAG_UNIFORM = """#version 330 core
uniform vec3 color;
out vec4 outColor;
in vec3 position_out;
in vec3 colors_out;
void main() {
    outColor = vec4(color, 1);
}"""

LAMBERT_VERT = """#version 330 core
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
}"""

LAMBERT_FRAG = """#version 330 core
uniform vec3 color;
out vec4 outColor;
in vec3 colors_out;
in vec3 normals;
in vec3 light_out;
in mat3 model_out;
void main() {
    mat3 model_out_transformed = transpose(inverse(model_out));
    vec3 new_normals = model_out_transformed*normals;
    outColor = vec4(colors_out, 1)*max(dot(vec4(new_normals, 1), vec4(light_out, 1)), 0);
}"""
