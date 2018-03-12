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
from opengl_tools.transform import identity

class Node:
    """ Scene graph transform and parameter broadcast node """
    def __init__(self, name='', children=(), transform=identity(), **param):
        self.transform, self.param, self.name = transform, param, name
        self.children = list(iter(children))

    def add(self, *drawables):
        """ Add drawables to this node, simply updating children list """
        self.children.extend(drawables)

    def draw(self, projection, view, model, **param):
        """ Recursive draw, passing down named parameters & model matrix. """
        # merge named parameters given at initialization with those given here
        param = dict(param, **self.param)
        # model =
        for child in self.children:
            child.draw(projection, view, model, **param)

class ViewerRoboticArm(Viewer):
    """ Viewer for the robotic arm project """
    def __init__(self, width=640, height=480):
        super().__init__(None)
        self.multiple_color_shader = Shader(COLOR_VERT, COLOR_FRAG_MULTIPLE)

    def do_for_each_drawable(self, drawable, view, projection, model):
        drawable.draw(projection, view, model, self.multiple_color_shader)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = ViewerRoboticArm()

    # place instances of our basic objects
    viewer.add(load("suzanne.obj")[0])

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
