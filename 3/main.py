#!/usr/bin/env python3
"""
Python OpenGL - Hierarchical modeling
"""
# Python built-in modules
import os                           # os function, i.e. checking file status

# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL
import numpy as np
import OpenGL.GL as GL              # standard Python OpenGL wrapper
from opengl_tools.pyramids import PyramidColored
from opengl_tools.viewer import Viewer
from opengl_tools.shader import Shader
from opengl_tools.shaders_glsl import COLOR_VERT, COLOR_FRAG_MULTIPLE, COLOR_FRAG_UNIFORM
from opengl_tools.loader import load
from opengl_tools.transform import identity, translate, rotate, scale, vec
from opengl_tools.color_mesh import ColorMesh
from opengl_tools.node import Node, RotationControlNode

PHONG_VERT = """#version 330 core
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
void main() {
    gl_Position = projection * view * model * vec4(position_in, 1);
    position_out = position_in;
    colors_out = color;
    normals = normals_in;
    light_out = light;
}"""

PHONG_FRAG = """#version 330 core
uniform vec3 color;
out vec4 outColor;
in vec3 position_out;
in vec3 colors_out;
in vec3 normals;
in vec3 light_out;
void main() {
    outColor = vec4(colors_out, 1)*dot(vec4(normals, 1), vec4(light_out, 1));
}"""

class Cylinder(Node):
    """ Very simple cylinder based on practical 2 load function """
    def __init__(self):
        super().__init__()
        self.add(*load('cylinder.obj'))  # just load the cylinder from file

class Suzanne(Node):
    """ Suzanne node """
    def __init__(self, light_vector):
        super().__init__()
        # Get the only ione suzanne color mesh
        objects = load("suzanne.obj")
        assert len(objects)
        self.color_mesh = objects[0]
        # Add the light
        self.color_mesh.addUniform3fv({"light" :light_vector})
        print(self.color_mesh)
        self.add(self.color_mesh)

class ViewerPhong(Viewer):
    """ Viewer for the robotic arm project """
    def __init__(self, width=640, height=480):
        super().__init__(None)
        self.phong_shader = Shader(PHONG_VERT, PHONG_FRAG)

    def do_for_each_drawable(self, drawable, view, projection, model, **param):
        drawable.draw(projection, view, model, self.phong_shader, color=(1, 0, 1), win=self.win, **param)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """

    viewer = ViewerPhong()
    rotator_node = RotationControlNode(glfw.KEY_LEFT, glfw.KEY_RIGHT, vec(0, 1, 0))
    rotator_node.add(Suzanne(light_vector=(1, 0, 1)))
    viewer.add(rotator_node)
    viewer.run()

if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
