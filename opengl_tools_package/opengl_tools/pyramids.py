#!/usr/bin/env python3
"""
Pyramid as scene object
"""
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
from opengl_tools.color_mesh import ColorMesh

class Pyramid(ColorMesh):

    def __init__(self, position=None, index=None):
        if position is None:
            self.position = np.array(((0, 1, 0), (-0.5, 0, 0.5), (0.5, 0, 0.5), (0.5, 0, -0.5), (-0.5, 0, -0.5)), np.float32)
        else :
            self.position = position

        if index is None:
            self.index = np.array((0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 1), np.uint32)
        else:
            self.index = index

        super().__init__([self.position], self.index)

class PyramidColored(Pyramid):

    def __init__(self, color=None, position=None, index=None):
        super().__init__(position, index)
        if color is None:
            self.color = np.array(((1, 0, 0), (0, 0, 1), (0, 1, 0),(1, 1, 0), (0, 1, 1)), 'f')
        else :
            self.color = color
        super().addAttribut(self.color)
