#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""
# Python built-in modules
import os                           # os function, i.e. checking file status
import sys

sys.path.append("../opengl_tools_package/opengl_tools")

# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL
from pyramids import PyramidColored
from viewer import Viewer
from shader import Shader
from shaders_glsl import COLOR_VERT, COLOR_FRAG_MULTIPLE, COLOR_FRAG_UNIFORM
from loader import load

class ViewerPyramid(Viewer):
    """ Viewer for the pyramids project """
    def __init__(self, width=640, height=480):
        super().__init__(None)
        self.multiple_color_shader = Shader(COLOR_VERT, COLOR_FRAG_MULTIPLE)
        self.uniform_color_shader = Shader(COLOR_VERT, COLOR_FRAG_UNIFORM)

    def do_for_each_drawable(self, drawable, view, projection, model):
        if(type(drawable) is PyramidColored):
            drawable.draw(projection, view, model, self.multiple_color_shader)
        else :
            drawable.draw(projection, view, model, self.multiple_color_shader)

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = ViewerPyramid()

    # place instances of our basic objects
    # viewer.add(PyramideMultiColors())
            # one time initialization
    viewer.add(PyramidColored())
    # Charge cette suzanne
    viewer.add(load("suzanne.obj")[0])

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
