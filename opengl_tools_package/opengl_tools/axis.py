#!/usr/bin/env python3
"""
Create Axis of differents colors
"""
from OpenGL.GL import GL_LINES
import numpy as np
from opengl_tools.color_mesh import ColorMesh

class Axis(ColorMesh):
    def __init__(self, x=0, y=0, z=0, color=(1, 1, 1, 1)):
        self.position = np.array(((0, 0, 0), (x, y, z)), np.float32)
        self.color = color
        super().__init__([self.position], primitive=GL_LINES)

    def draw(self, projection, view, model, color_shader, color=(1, 1, 1, 1), **param):
        super().draw(projection, view, model, color_shader, self.color, **param)

class xAxis(Axis):
    def __init__(self):
        super().__init__(x=1, color=(1, 0, 0, 1))

class yAxis(Axis):
    def __init__(self):
        super().__init__(y=1, color=(0, 1, 0, 1))

class zAxis(Axis):
    def __init__(self):
        super().__init__(z=1, color=(0, 0, 1, 1))
