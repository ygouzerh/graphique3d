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

class Cylinder(Node):
    """ Very simple cylinder based on practical 2 load function """
    def __init__(self):
        super().__init__()
        self.add(*load('cylinder.obj'))  # just load the cylinder from file

class ViewerRoboticArm(Viewer):
    """ Viewer for the robotic arm project """
    def __init__(self, width=640, height=480):
        super().__init__(None)
        self.multiple_color_shader = Shader(COLOR_VERT, COLOR_FRAG_MULTIPLE)

    def do_for_each_drawable(self, drawable, view, projection, model, **param):
        drawable.draw(projection, view, model, self.multiple_color_shader, win=self.win, **param)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """

    viewer = ViewerRoboticArm()
        # construct our robot arm hierarchy for drawing in viewer
    cylinder = Cylinder()             # re-use same cylinder instance
    base_node_y = 0.2
    limb_shape = Node(transform=translate(0, base_node_y, 0)@scale(0.05,1,0.05))  # make a thin cylinder
    limb_shape.add(cylinder)

    arm_node = RotationControlNode(glfw.KEY_LEFT, glfw.KEY_RIGHT, vec(0, 1, 0))
    arm_node.add(limb_shape)

    base_shape = Node(transform=scale(1.2,base_node_y,1.2), children=[cylinder])
    base_node = Node(transform=rotate(axis=(0, 1, 0), angle=90)@scale(0.5,0.5,0.5), children=[base_shape])

    base_node.add(arm_node)
    viewer.add(base_node)
    viewer.run()

if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
