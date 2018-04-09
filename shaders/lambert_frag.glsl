#version 330 core
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
}
