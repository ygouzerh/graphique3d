#!/usr/bin/env python3
"""
Python OpenGL - Hierarchical modeling
"""
# Python built-in modules
import os                           # os function, i.e. checking file status

# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL
from opengl_tools.pyramids import PyramidColored
from opengl_tools.viewer import Viewer
from opengl_tools.shader import Shader
from opengl_tools.shaders_glsl import COLOR_VERT, COLOR_FRAG_MULTIPLE, COLOR_FRAG_UNIFORM
from opengl_tools.loader import load
from opengl_tools.transform import identity, translate, rotate, scale

class Node:
    """ Scene graph transform and parameter broadcast node """
    def __init__(self, name='', children=(), transform=identity(), **param):
        self.transform, self.param, self.name = transform, param, name
        self.children = list(iter(children))

    def add(self, *drawables):
        """ Add drawables to this node, simply updating children list """
        self.children.extend(drawables)

    def draw(self, projection, view, model, color_shader, **param):
        """ Recursive draw, passing down named parameters & model matrix. """
        # merge named parameters given at initialization with those given here
        param = dict(param, **self.param)
        model = self.transform @ model
        for child in self.children:
            print("{} appel {}".format(self.name, child))
            child.draw(projection, view, model, color_shader, **param)

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
        print("ROOT")
        drawable.draw(projection, view, model, self.multiple_color_shader, **param)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """

    viewer = ViewerRoboticArm()
        # construct our robot arm hierarchy for drawing in viewer
    cylinder = Cylinder()             # re-use same cylinder instance
    limb_shape = Node(transform=scale(x=0.1, z=0.2))  # make a thin cylinder
    limb_shape.add(cylinder)
    viewer.add(limb_shape)
    # limb_shape.add(cylinder)          # common shape of arm and forearm
    #
    # arm_node = Node(transform=...)    # robot arm rotation with phi angle
    # arm_node.add(limb_shape)
    #
    # # make a flat cylinder
    # base_shape = Node(transform=..., children=[cylinder])
    # base_node = Node(transform=...)   # robot base rotation with theta angle
    # base_node.add(base_shape, arm_node)
    # viewer.add(base_node)
    viewer.run()

if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
