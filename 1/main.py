#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""
# Python built-in modules
import os                           # os function, i.e. checking file status

# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL
from pyramids import PyramidMultiColors, PyramidColored
from viewer import Viewer

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()

    # place instances of our basic objects
    # viewer.add(PyramideMultiColors())
            # one time initialization
    viewer.add(PyramidColored())

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
