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
from opengl_tools.shaders_glsl import LAMBERT_VERT, LAMBERT_FRAG
from opengl_tools.loader import load
from opengl_tools.transform import identity, translate, rotate, scale, vec
from opengl_tools.color_mesh import ColorMesh
from opengl_tools.node import Node, RotationControlNode

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

class ViewerLambert(Viewer):
    """ Viewer for the robotic arm project """
    
    def do_for_each_drawable(self, drawable, view, projection, model, **param):
        drawable.draw(projection, view, model, self.shaders, color=(1, 0, 1), win=self.win, **param)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    shaders_repertory = "../shaders/"
    vert_name = "lambert_vert.glsl"
    frag_name = "lambert_frag.glsl"
    viewer = ViewerLambert(shaders_repertory+vert_name, shaders_repertory+frag_name)
    rotator_node = RotationControlNode(glfw.KEY_LEFT, glfw.KEY_RIGHT, vec(0, 1, 0))
    rotator_node.add(Suzanne(light_vector=(1, 1, 1)))
    viewer.add(rotator_node)
    viewer.run()

if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
